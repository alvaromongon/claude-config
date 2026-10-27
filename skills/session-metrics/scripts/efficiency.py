#!/usr/bin/env python3
"""The repo's efficiency log: one CSV row per measured window, rendered into the README and docs.

Rows are appended by `session_metrics.py --record`; this module renders them between
`<!-- efficiency:<block>:start -->` / `<!-- efficiency:<block>:end -->` markers, and
`.github/scripts/validate.py` fails when a page no longer matches the CSV.

Usage: efficiency.py [--check]   (rewrites the blocks; with --check only reports stale pages)
"""
import csv
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CSV = Path("docs/efficiency.csv")
PAGES = {Path("README.md"): "snapshot", Path("docs/efficiency.md"): "history"}
FIELDS = ["change", "repo", "since", "until", "merged_prs", "cost_per_pr_usd_est", "human_msgs_per_pr",
          "first_review_clean_pct", "review_rounds_mean", "active_min_per_pr", "tokens_per_pr",
          "usage_limit_hits", "main_context", "subagent_context"]


def row_from(metrics: dict, repo: str, change: str, since: str | None, until: str | None) -> dict:
    merged = len(metrics["outcomes"]["merged_prs"])
    if not merged:
        raise ValueError("no merged PRs in the window: nothing to compare per PR")
    rounds = list(metrics["outcomes"]["review_rounds"].values())
    reviewed = len(rounds)
    return {
        "change": change, "repo": repo, "since": since or "", "until": until or "",
        "merged_prs": str(merged),
        "cost_per_pr_usd_est": f"{metrics['cost']['total'] / merged:.2f}",
        "human_msgs_per_pr": f"{metrics['human']['messages'] / merged:.2f}",
        "first_review_clean_pct":
            f"{100 * len(metrics['outcomes']['clean_first_review']) / reviewed:.0f}" if reviewed else "",
        "review_rounds_mean": f"{statistics.mean(rounds):.2f}" if rounds else "",
        "active_min_per_pr": f"{metrics['time']['active_minutes'] / merged:.0f}",
        "tokens_per_pr": str(sum(metrics["tokens"].values()) // merged),
        "usage_limit_hits": str(metrics["time"]["usage_limit_hits"]),
        "main_context": str(metrics["context"]["main_first_call_median"] or ""),
        "subagent_context": str(metrics["context"]["subagent_first_call_median"] or ""),
    }


def read_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def append_row(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    new = not path.exists()
    with path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        if new:
            writer.writeheader()
        writer.writerow(row)


def _delta(latest: str, baseline: str) -> str:
    if not latest or not baseline or float(baseline) == 0:
        return "—"
    change = round(100 * (float(latest) - float(baseline)) / float(baseline))
    return "=" if change == 0 else f"{'−' if change < 0 else '+'}{abs(change)}%"


def _chart(rows: list[dict], title: str, field: str) -> list[str]:
    labels = ", ".join(f'"{r["change"]}"' for r in rows)
    values = [r[field] for r in rows]
    top = max(float(v) for v in values) * 1.25
    return ["```mermaid", "---", "config:", "  xyChart:", "    showDataLabel: true", "---", "xychart-beta",
            f'    title "{title}"', f"    x-axis [{labels}]",
            f'    y-axis 0 --> {top:.0f}', f"    bar [{', '.join(values)}]", "```"]


def render_snapshot(rows: list[dict]) -> str:
    baseline, latest = rows[0], rows[-1]
    since_baseline = "since the baseline" if len(rows) > 1 else "baseline, no change measured yet"
    metric_rows = [
        ("Cost per merged PR (estimated, list prices)", f"${latest['cost_per_pr_usd_est']}", "cost_per_pr_usd_est"),
        ("Owner messages per merged PR", latest["human_msgs_per_pr"], "human_msgs_per_pr"),
        ("PRs clean at first review", f"{latest['first_review_clean_pct']}%", "first_review_clean_pct"),
        ("Active agent minutes per merged PR", latest["active_min_per_pr"], "active_min_per_pr"),
    ]
    lines = [
        f"Latest window: **{latest['change']}** on `{latest['repo']}`, {latest['since']} → {latest['until']}, "
        f"{latest['merged_prs']} merged PRs ({since_baseline}).",
        "",
        "| Metric | Latest | vs baseline |",
        "|---|---|---|",
        *(f"| {name} | {value} | {_delta(latest[field], baseline[field])} |" for name, value, field in metric_rows),
        "",
        *_chart(rows, "Cost per merged PR (USD, estimated)", "cost_per_pr_usd_est"),
        "",
        *_chart(rows, "Owner messages per merged PR", "human_msgs_per_pr"),
    ]
    return "\n".join(lines) + "\n"


def render_history(rows: list[dict]) -> str:
    lines = ["| Change | Repo | Window | Merged PRs | $/PR (est.) | Owner msgs/PR | Clean 1st review | "
             "Review rounds | Active min/PR | Tokens/PR | Limit hits | Fixed context main / subagent |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['change']} | {r['repo']} | {r['since']} → {r['until']} | {r['merged_prs']} | "
                     f"{r['cost_per_pr_usd_est']} | {r['human_msgs_per_pr']} | {r['first_review_clean_pct']}% | "
                     f"{r['review_rounds_mean']} | {r['active_min_per_pr']} | {int(r['tokens_per_pr']):,} | "
                     f"{r['usage_limit_hits']} | {r['main_context']} / {r['subagent_context']} |")
    return "\n".join(lines) + "\n"


RENDERERS = {"snapshot": render_snapshot, "history": render_history}


def replace_block(text: str, block: str, content: str) -> str:
    pattern = re.compile(rf"(<!-- efficiency:{block}:start -->\n).*?(<!-- efficiency:{block}:end -->)", re.DOTALL)
    if not pattern.search(text):
        raise ValueError(f"markers for the '{block}' block not found")
    return pattern.sub(lambda m: m.group(1) + content + m.group(2), text)


def _expected(root: Path) -> dict[Path, str]:
    rows = read_rows(root / CSV)
    if not rows:
        return {}
    expected = {}
    for page, block in PAGES.items():
        text = (root / page).read_text(encoding="utf-8")
        expected[page] = replace_block(text, block, RENDERERS[block](rows))
    return expected


def stale_pages(root: Path = ROOT) -> list[Path]:
    return [page for page, text in _expected(root).items()
            if (root / page).read_text(encoding="utf-8") != text]


def sync(root: Path = ROOT) -> None:
    for page, text in _expected(root).items():
        (root / page).write_text(text, encoding="utf-8")


def main(argv: list[str]) -> int:
    if "--check" in argv:
        stale = stale_pages()
        for page in stale:
            print(f"{page}: efficiency block out of date — run efficiency.py")
        return 1 if stale else 0
    sync()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
