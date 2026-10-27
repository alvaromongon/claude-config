#!/usr/bin/env python3
"""Measure Claude Code sessions of one project from its local transcripts.

Reads ~/.claude/projects/<project>/<session>.jsonl and each session's subagents/, and reports the
before/after metrics for a configuration change: estimated cost and tokens per merged PR (by role
and model), review rounds per PR, human messages, active and paused time, usage-limit hits and the
fixed context every call pays before doing any work.

Usage: session_metrics.py PROJECT_DIR [PROJECT_DIR...] [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--json]
       [--record docs/efficiency.csv --repo OWNER/NAME --change LABEL [--issue N]]
"""
import argparse
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import efficiency

# (input $/MTok, output $/MTok, cache-read multiplier of input) at list price — source: Anthropic's
# pricing page, read 2026-10-27 (Haiku 5.5: prompts up to 100k tokens; longer ones cost 5x).
# Cost is an estimate: a subscription is billed by plan, and these prices only make runs comparable.
PRICES = {"opus": (4.0, 20.0, 0.05), "sonnet": (2.0, 10.0, 0.05), "haiku": (0.10, 0.50, 0.1),
          "fable": (10.0, 50.0, 0.025)}
CACHE_WRITE_5M, CACHE_WRITE_1H = 1.25, 2.0
PAUSE = timedelta(minutes=15)  # a longer gap between events counts as paused, not active

ROLES = [  # first match wins; matched against the Agent call's description
    ("fix", re.compile(r"\bfix\b|ronda|rework|rehacer|apply|owner-authorized", re.I)),
    ("security-review", re.compile(r"secur|segurid|vulnerab|vulns", re.I)),
    ("code-review", re.compile(r"review|revisi[oó]n", re.I)),
    ("checkpoint", re.compile(r"checkpoint", re.I)),
    ("implement", re.compile(r"implement", re.I)),
]
PR_IN_DESCRIPTION = re.compile(r"PR\s*#?(\d+)")
MERGE_COMMAND = re.compile(r"gh pr merge (\d+)")
MERGE_FAILED = re.compile(r"not mergeable|prohibits the merge|could not merge|merge failed", re.I)
LIMIT_HIT = re.compile(r"hit your (session|usage) limit", re.I)


def model_family(model: str) -> str:
    return next((family for family in PRICES if family in (model or "")), "opus")


def call_cost(usage: dict, family: str, prices: dict) -> float:
    price_in, price_out, cache_read = prices[family]
    write_1h = (usage.get("cache_creation") or {}).get("ephemeral_1h_input_tokens", 0)
    write_5m = usage.get("cache_creation_input_tokens", 0) - write_1h
    return (usage.get("input_tokens", 0) * price_in
            + write_5m * price_in * CACHE_WRITE_5M
            + write_1h * price_in * CACHE_WRITE_1H
            + usage.get("cache_read_input_tokens", 0) * price_in * cache_read
            + usage.get("output_tokens", 0) * price_out) / 1e6


def role_of(description: str) -> str:
    return next((role for role, pattern in ROLES if pattern.search(description or "")), "other")


def parse_time(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


class Transcript:
    """One JSONL file: its API calls (deduplicated by message id) and the events the metrics need."""

    def __init__(self, path: Path):
        self.calls: dict[str, dict] = {}
        self.timestamps: list[str] = []
        self.human_messages = 0
        self.limit_hits: set[tuple[str, str]] = set()  # (date, message): one event, however many agents hit it
        self.merged_prs: list[int] = []
        merges: dict[str, int] = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("timestamp"):
                self.timestamps.append(event["timestamp"])
            message = event.get("message") or {}
            content = message.get("content")
            blocks = content if isinstance(content, list) else []
            if event.get("type") == "assistant":
                if message.get("model") == "<synthetic>":
                    text = " ".join(b.get("text", "") for b in blocks if b.get("type") == "text")
                    if LIMIT_HIT.search(text):
                        self.limit_hits.add((event.get("timestamp", "")[:10], text.strip()))
                else:
                    self.calls[message.get("id")] = message
                for block in blocks:
                    if block.get("type") == "tool_use" and block.get("name") == "Bash":
                        found = MERGE_COMMAND.search(block["input"].get("command", ""))
                        if found:
                            merges[block["id"]] = int(found.group(1))
            elif event.get("type") == "user":
                if (event.get("origin") or {}).get("kind") == "human":
                    self.human_messages += 1
                for block in blocks:
                    if block.get("type") == "tool_result" and block.get("tool_use_id") in merges \
                            and not block.get("is_error") and not MERGE_FAILED.search(_text(block.get("content"))):
                        self.merged_prs.append(merges[block["tool_use_id"]])

    def first_call_context(self) -> int | None:
        for message in self.calls.values():
            usage = message.get("usage") or {}
            return (usage.get("input_tokens", 0) + usage.get("cache_creation_input_tokens", 0)
                    + usage.get("cache_read_input_tokens", 0))
        return None


def _text(content) -> str:
    if isinstance(content, str):
        return content
    return " ".join(b.get("text", "") for b in content or [] if isinstance(b, dict))


def load_subagents(folder: Path) -> list[tuple[str, dict, Transcript]]:
    """Each subagent as (role, meta, transcript); a nested one takes its top-level ancestor's role."""
    metas = {}
    for meta_path in folder.glob("agent-*.meta.json"):
        agent_id = meta_path.name[len("agent-"):-len(".meta.json")]
        metas[agent_id] = json.loads(meta_path.read_text(encoding="utf-8"))

    def resolve_role(agent_id: str, seen=()) -> str:
        meta = metas.get(agent_id, {})
        parent = meta.get("parentAgentId")
        if not meta.get("description") and parent in metas and parent not in seen:
            return resolve_role(parent, (*seen, agent_id))
        return role_of(meta.get("description", ""))

    agents = []
    for agent_id, meta in metas.items():
        transcript_path = folder / f"agent-{agent_id}.jsonl"
        if transcript_path.exists():
            agents.append((resolve_role(agent_id), meta, Transcript(transcript_path)))
    return agents


def measure(project_dirs: list[Path], prices: dict = PRICES, since: str | None = None,
            until: str | None = None) -> dict:
    by_role: dict[str, Counter] = defaultdict(Counter)
    tokens: Counter = Counter()
    merged, rounds, fixed = set(), Counter(), set()
    main_contexts, sub_contexts = [], []
    calls = humans = sessions = 0
    limit_hits: set[tuple[str, str]] = set()
    active = paused = timedelta()

    for project in project_dirs:
        for main_path in sorted(Path(project).glob("*.jsonl")):
            main = Transcript(main_path)
            if not main.timestamps:
                continue
            start = min(main.timestamps)[:10]
            if (since and start < since) or (until and start > until):
                continue
            sessions += 1
            agents = load_subagents(main_path.with_suffix("") / "subagents")
            for role, meta, transcript in [("main", {}, main), *agents]:
                for message in transcript.calls.values():
                    family = model_family(message.get("model"))
                    usage = message.get("usage") or {}
                    by_role[role][family] += call_cost(usage, family, prices)
                    for key in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens",
                                "output_tokens"):
                        tokens[key] += usage.get(key, 0)
                calls += len(transcript.calls)
                limit_hits |= transcript.limit_hits
                merged.update(transcript.merged_prs)
                context = transcript.first_call_context()
                if context is not None:
                    (main_contexts if role == "main" else sub_contexts).append(context)
                pr = PR_IN_DESCRIPTION.search(meta.get("description", ""))
                if pr and role == "code-review" and meta.get("spawnDepth", 1) == 1:
                    rounds[int(pr.group(1))] += 1
                if pr and role == "fix":
                    fixed.add(int(pr.group(1)))
            humans += main.human_messages
            times = sorted(parse_time(t) for t in main.timestamps)
            for earlier, later in zip(times, times[1:]):
                gap = later - earlier
                if gap > PAUSE:
                    paused += gap
                else:
                    active += gap

    roles = {role: {family: round(cost, 6) for family, cost in families.items()}
             for role, families in by_role.items()}
    total = sum(sum(families.values()) for families in by_role.values())
    return {
        "sessions": sessions,
        "calls": calls,
        "tokens": dict(tokens),
        "cost": {"total": round(total, 6), "by_role": roles},
        "outcomes": {
            "merged_prs": sorted(merged),
            "review_rounds": dict(sorted(rounds.items())),
            "clean_first_review": sorted(pr for pr, n in rounds.items() if n == 1 and pr not in fixed),
        },
        "human": {"messages": humans},
        "time": {"active_minutes": round(active.total_seconds() / 60),
                 "paused_minutes": round(paused.total_seconds() / 60),
                 "usage_limit_hits": len(limit_hits)},
        "context": {"main_first_call_median": _median(main_contexts),
                    "subagent_first_call_median": _median(sub_contexts)},
    }


def _median(values: list[int]) -> int | None:
    return round(statistics.median(values)) if values else None


def render_markdown(m: dict) -> str:
    merged = len(m["outcomes"]["merged_prs"])
    reviewed = len(m["outcomes"]["review_rounds"])
    per_pr = lambda value: f"{value / merged:,.2f}" if merged else "n/a"  # noqa: E731
    total_tokens = sum(m["tokens"].values())
    rounds = list(m["outcomes"]["review_rounds"].values())
    lines = [
        f"# Session metrics ({m['sessions']} sessions, {m['calls']} API calls)",
        "",
        "## Cost (estimated: list prices per model, cache writes x1.25/x2, reads x0.05 on Opus/Sonnet 5.5)",
        "",
        f"- Total: ${m['cost']['total']:,.2f}",
        f"- Cost per merged PR: ${per_pr(m['cost']['total'])} ({merged} merged)",
        f"- Tokens per merged PR (measured): {total_tokens // merged:,}" if merged else "- Tokens per merged PR: n/a",
        "",
        "| Role | Model | $ | % |",
        "|---|---|---|---|",
    ]
    for role, families in sorted(m["cost"]["by_role"].items(), key=lambda kv: -sum(kv[1].values())):
        for family, cost in sorted(families.items(), key=lambda kv: -kv[1]):
            share = 100 * cost / m["cost"]["total"] if m["cost"]["total"] else 0
            lines.append(f"| {role} | {family} | {cost:,.2f} | {share:.0f}% |")
    lines += [
        "",
        "## Quality (measured)",
        "",
        f"- PRs reviewed: {reviewed}; clean at first review: {len(m['outcomes']['clean_first_review'])}",
        f"- Review rounds per PR: mean {statistics.mean(rounds):.2f}, max {max(rounds)}" if rounds
        else "- Review rounds per PR: n/a",
        "",
        "## Human and time (measured)",
        "",
        f"- Human messages: {m['human']['messages']}"
        + (f" ({m['human']['messages'] / merged:.2f} per merged PR)" if merged else ""),
        f"- Active time: {m['time']['active_minutes']} min"
        + (f" ({m['time']['active_minutes'] / merged:.0f} min per merged PR)" if merged else "")
        + f"; paused: {m['time']['paused_minutes']} min; usage-limit hits: {m['time']['usage_limit_hits']}",
        "",
        "## Fixed context (measured: tokens of each transcript's first call)",
        "",
        f"- Main session median: {m['context']['main_first_call_median']}",
        f"- Subagent median: {m['context']['subagent_first_call_median']}",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("projects", nargs="+", type=Path, help="folders under ~/.claude/projects")
    parser.add_argument("--since", help="first session start date to include (YYYY-MM-DD)")
    parser.add_argument("--until", help="last session start date to include (YYYY-MM-DD)")
    parser.add_argument("--json", action="store_true", help="print the raw metrics as JSON")
    parser.add_argument("--record", type=Path, metavar="CSV",
                        help="append the window to this efficiency log (e.g. docs/efficiency.csv)")
    parser.add_argument("--repo", help="with --record: the public repo measured, as owner/name")
    parser.add_argument("--change", help="with --record: the configuration change this window measures")
    parser.add_argument("--issue", help="with --record: number of the claude-config issue that tracks the change")
    args = parser.parse_args(argv)
    if args.record and not (args.repo and args.change):
        parser.error("--record needs --repo and --change")
    metrics = measure(args.projects, since=args.since, until=args.until)
    print(json.dumps(metrics, indent=2) if args.json else render_markdown(metrics), end="")
    if args.record:
        efficiency.append_row(args.record, efficiency.row_from(metrics, repo=args.repo, change=args.change,
                                                               since=args.since, until=args.until,
                                                               issue=args.issue))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
