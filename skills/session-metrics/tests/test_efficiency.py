import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))

import efficiency as ef  # noqa: E402

METRICS = {
    "sessions": 9, "calls": 5088,
    "tokens": {"input_tokens": 100, "cache_creation_input_tokens": 200, "cache_read_input_tokens": 300,
               "output_tokens": 400},
    "cost": {"total": 377.19, "by_role": {}},
    "outcomes": {"merged_prs": list(range(31)), "review_rounds": {1: 1, 2: 2, 3: 3, 4: 1},
                 "clean_first_review": [1, 4]},
    "human": {"messages": 124},
    "time": {"active_minutes": 1085, "paused_minutes": 9, "usage_limit_hits": 5},
    "context": {"main_first_call_median": 72696, "subagent_first_call_median": 54713},
}


def row(change, cost_per_pr, human_per_pr, **extra):
    base = {"change": change, "repo": "o/r", "since": "2026-10-16", "until": "2026-10-26", "merged_prs": "31",
            "cost_per_pr_usd_est": cost_per_pr, "human_msgs_per_pr": human_per_pr,
            "first_review_clean_pct": "50", "review_rounds_mean": "1.75", "active_min_per_pr": "35",
            "tokens_per_pr": "32", "usage_limit_hits": "5", "main_context": "72696", "subagent_context": "54713"}
    return {**base, **extra}


class RowTests(unittest.TestCase):
    def test_turns_metrics_into_per_pr_figures(self):
        r = ef.row_from(METRICS, repo="o/r", change="Baseline", since="2026-10-16", until="2026-10-26")

        self.assertEqual(r["cost_per_pr_usd_est"], "12.17")
        self.assertEqual(r["human_msgs_per_pr"], "4.00")
        self.assertEqual(r["first_review_clean_pct"], "50")
        self.assertEqual(r["review_rounds_mean"], "1.75")
        self.assertEqual(r["active_min_per_pr"], "35")
        self.assertEqual(r["tokens_per_pr"], "32")
        self.assertEqual(r["merged_prs"], "31")

    def test_refuses_a_window_with_no_merged_prs(self):
        empty = {**METRICS, "outcomes": {**METRICS["outcomes"], "merged_prs": []}}

        with self.assertRaises(ValueError):
            ef.row_from(empty, repo="o/r", change="x", since=None, until=None)


class CsvTests(unittest.TestCase):
    def test_appends_rows_under_a_single_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "docs" / "efficiency.csv"
            ef.append_row(path, row("Baseline", "12.17", "4.00"))
            ef.append_row(path, row("Sonnet orchestrator", "10.00", "3.50"))

            rows = ef.read_rows(path)

        self.assertEqual([r["change"] for r in rows], ["Baseline", "Sonnet orchestrator"])
        self.assertEqual(rows[1]["cost_per_pr_usd_est"], "10.00")


class RenderTests(unittest.TestCase):
    rows = [row("Baseline", "12.17", "4.00"), row("Sonnet orchestrator", "10.00", "3.00")]

    def test_snapshot_compares_the_latest_window_with_the_baseline(self):
        snapshot = ef.render_snapshot(self.rows)

        self.assertIn("$10.00", snapshot)
        self.assertIn("−18%", snapshot)  # 10.00 vs 12.17
        self.assertIn("−25%", snapshot)  # 3.00 vs 4.00
        self.assertIn("estimated", snapshot)

    def test_snapshot_charts_each_change_on_the_x_axis(self):
        snapshot = ef.render_snapshot(self.rows)

        self.assertIn("xychart-beta", snapshot)
        self.assertIn('x-axis ["Baseline", "Sonnet orchestrator"]', snapshot)
        self.assertIn("bar [12.17, 10.00]", snapshot)

    def test_history_lists_every_window(self):
        history = ef.render_history(self.rows)

        self.assertIn("| Baseline | o/r | 2026-10-16 → 2026-10-26 | 31 | 12.17 |", history)
        self.assertIn("| Sonnet orchestrator |", history)


class SyncTests(unittest.TestCase):
    def test_replaces_only_the_marked_block(self):
        text = "intro\n<!-- efficiency:snapshot:start -->\nold\n<!-- efficiency:snapshot:end -->\noutro\n"

        synced = ef.replace_block(text, "snapshot", "new\n")

        self.assertEqual(synced, "intro\n<!-- efficiency:snapshot:start -->\nnew\n"
                                 "<!-- efficiency:snapshot:end -->\noutro\n")

    def test_reports_a_block_that_no_longer_matches_the_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ef.append_row(root / ef.CSV, row("Baseline", "12.17", "4.00"))
            for page, block in ef.PAGES.items():
                (root / page).parent.mkdir(parents=True, exist_ok=True)
                (root / page).write_text(f"<!-- efficiency:{block}:start -->\nstale\n<!-- efficiency:{block}:end -->\n")

            self.assertEqual(len(ef.stale_pages(root)), 2)
            ef.sync(root)
            self.assertEqual(ef.stale_pages(root), [])


if __name__ == "__main__":
    unittest.main()
