import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "TestDoubles"))
sys.path.insert(0, str(HERE.parent / "scripts"))

import session_metrics as sm  # noqa: E402
from transcripts import (assistant, human, limit_hit, notification, tool_result, tool_use,  # noqa: E402
                         write_session)

PRICES = {"opus": (4.0, 20.0), "sonnet": (2.0, 10.0)}


class TempProject(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._tmp.name) / "-Users-me-Code-repo"

    def tearDown(self):
        self._tmp.cleanup()

    def measure(self, **kwargs):
        return sm.measure([self.project], prices=PRICES, **kwargs)


class CostTests(TempProject):
    def test_prices_every_token_type_and_counts_a_streamed_message_once(self):
        msg = assistant("2026-10-20T10:00:00Z", model="claude-opus-5-5", msg_id="m1", input_tokens=1_000_000,
                        cache_write_5m=1_000_000, cache_write_1h=1_000_000, cache_read=1_000_000,
                        output_tokens=1_000_000)
        write_session(self.project, "s1", [msg, msg])

        m = self.measure()

        # input 4 + 5m write 4*1.25 + 1h write 4*2 + read 4*0.1 + output 20
        self.assertAlmostEqual(m["cost"]["total"], 4 + 5 + 8 + 0.4 + 20)
        self.assertEqual(m["calls"], 1)

    def test_splits_main_session_cost_by_model(self):
        write_session(self.project, "s1", [
            assistant("2026-10-20T10:00:00Z", model="claude-sonnet-5-5", output_tokens=1_000_000),
            assistant("2026-10-20T10:01:00Z", model="claude-opus-5-5", output_tokens=1_000_000),
        ])

        m = self.measure()

        self.assertEqual(m["cost"]["by_role"]["main"], {"sonnet": 10.0, "opus": 20.0})


class RoleTests(TempProject):
    def test_classifies_subagents_by_description_and_nested_ones_by_their_parent(self):
        out = {"output_tokens": 1_000_000}
        write_session(self.project, "s1", [assistant("2026-10-20T10:00:00Z")], subagents=[
            ("a1", {"description": "Implement issue #40"}, [assistant("2026-10-20T10:01:00Z", "claude-sonnet-5-5", **out)]),
            ("a2", {"description": "Code review PR #46"}, [assistant("2026-10-20T10:02:00Z", **out)]),
            ("a3", {"description": "Security review PR #46"}, [assistant("2026-10-20T10:02:00Z", **out)]),
            ("a4", {"description": "Fix review findings PR #46"}, [assistant("2026-10-20T10:03:00Z", "claude-sonnet-5-5", **out)]),
            ("a5", {"description": "Re-review corrección PR #46"}, [assistant("2026-10-20T10:04:00Z", **out)]),
            ("a6", {"description": "Checkpoint tras PR #46"}, [assistant("2026-10-20T10:05:00Z", "claude-sonnet-5-5", **out)]),
            ("a7", {"parentAgentId": "a2", "spawnDepth": 2}, [assistant("2026-10-20T10:02:30Z", **out)]),
        ])

        roles = self.measure()["cost"]["by_role"]

        self.assertEqual(roles["implement"], {"sonnet": 10.0})
        self.assertEqual(roles["code-review"], {"opus": 60.0})
        self.assertEqual(roles["security-review"], {"opus": 20.0})
        self.assertEqual(roles["fix"], {"sonnet": 10.0})
        self.assertEqual(roles["checkpoint"], {"sonnet": 10.0})


class OutcomeTests(TempProject):
    def merge(self, ts, pr, result):
        call = tool_use("Bash", command=f'gh pr merge {pr} --squash --body "Closes #1."')
        return [assistant(ts, content=[call]), tool_result(ts, call["id"], result)]

    def test_counts_only_merges_that_succeeded(self):
        write_session(self.project, "s1", [
            *self.merge("2026-10-20T10:00:00Z", 73, "X Pull request o/r#73 is not mergeable: the base branch policy prohibits the merge."),
            *self.merge("2026-10-20T10:05:00Z", 73, "MERGED 2099bb5"),
            *self.merge("2026-10-20T10:10:00Z", 75, "✓ Squashed and merged pull request o/r#75"),
            *self.merge("2026-10-20T10:15:00Z", 76, "2a5b7da portfolio.md v2 carries the open lots (#76) | CLOSED"),
            *self.merge("2026-10-20T10:20:00Z", 77, "GraphQL: Pull Request is not mergeable (mergePullRequest)"),
        ])

        self.assertEqual(self.measure()["outcomes"]["merged_prs"], [73, 75, 76])

    def test_counts_review_rounds_per_pr_and_prs_clean_at_first_review(self):
        write_session(self.project, "s1", [assistant("2026-10-20T10:00:00Z")], subagents=[
            ("a1", {"description": "Code review PR #46"}, []),
            ("a2", {"description": "Security review PR #46"}, []),
            ("a3", {"description": "Fix review findings PR #46"}, []),
            ("a4", {"description": "Re-review code PR #46"}, []),
            ("a5", {"description": "Third-round code review PR #46"}, []),
            ("a6", {"description": "Code review PR #50"}, []),
            ("a7", {"description": "Security review PR #50"}, []),
        ])

        outcomes = self.measure()["outcomes"]

        self.assertEqual(outcomes["review_rounds"], {46: 3, 50: 1})
        self.assertEqual(outcomes["clean_first_review"], [50])


class HumanAndTimeTests(TempProject):
    def test_counts_human_messages_but_not_notifications(self):
        write_session(self.project, "s1", [
            human("2026-10-20T10:00:00Z", "/github-work-queue Milestone 3"),
            notification("2026-10-20T10:01:00Z", "<task-notification>done</task-notification>"),
            human("2026-10-20T10:02:00Z", "apruebo"),
        ])

        self.assertEqual(self.measure()["human"]["messages"], 2)

    def test_separates_active_time_from_pauses_and_counts_usage_limit_hits(self):
        write_session(self.project, "s1", [
            human("2026-10-20T10:00:00Z", "go"),
            assistant("2026-10-20T10:10:00Z"),
            limit_hit("2026-10-20T10:12:00Z"),
            assistant("2026-10-20T14:00:00Z"),
            assistant("2026-10-20T14:05:00Z"),
        ])

        time = self.measure()["time"]

        self.assertEqual(time["active_minutes"], 17)
        self.assertEqual(time["paused_minutes"], 228)
        self.assertEqual(time["usage_limit_hits"], 1)

    def test_counts_a_limit_hit_once_when_subagents_hit_it_too(self):
        write_session(self.project, "s1", [limit_hit("2026-10-20T10:12:00Z")], subagents=[
            ("a1", {"description": "Code review PR #1"}, [limit_hit("2026-10-20T10:12:30Z")]),
            ("a2", {"description": "Security review PR #1"}, [limit_hit("2026-10-20T10:13:00Z")]),
        ])

        self.assertEqual(self.measure()["time"]["usage_limit_hits"], 1)


class ContextTests(TempProject):
    def test_reports_the_context_of_each_transcripts_first_call(self):
        write_session(self.project, "s1", [
            assistant("2026-10-20T10:00:00Z", cache_write_1h=70_000, cache_read=2_000),
            assistant("2026-10-20T10:01:00Z", cache_read=300_000),
        ], subagents=[
            ("a1", {"description": "Implement issue #1"}, [assistant("2026-10-20T10:02:00Z", cache_read=50_000)]),
            ("a2", {"description": "Implement issue #2"}, [assistant("2026-10-20T10:03:00Z", cache_read=60_000)]),
        ])

        context = self.measure()["context"]

        self.assertEqual(context["main_first_call_median"], 72_000)
        self.assertEqual(context["subagent_first_call_median"], 55_000)


class WindowTests(TempProject):
    def test_keeps_only_sessions_that_start_inside_the_window(self):
        write_session(self.project, "old", [human("2026-10-01T10:00:00Z", "a")])
        write_session(self.project, "new", [human("2026-10-20T10:00:00Z", "b")])

        m = self.measure(since="2026-10-15", until="2026-10-31")

        self.assertEqual(m["sessions"], 1)


class ReportTests(TempProject):
    def test_markdown_report_states_cost_per_merged_pr_and_labels_it_estimated(self):
        call = tool_use("Bash", command="gh pr merge 7 --squash")
        write_session(self.project, "s1", [
            assistant("2026-10-20T10:00:00Z", output_tokens=1_000_000, content=[call]),
            tool_result("2026-10-20T10:00:01Z", call["id"], "MERGED abc"),
        ])

        report = sm.render_markdown(self.measure())

        self.assertIn("Cost per merged PR", report)
        self.assertIn("$20.00", report)
        self.assertIn("estimated", report)


class RecordTests(TempProject):
    def test_record_appends_the_window_to_the_efficiency_log(self):
        call = tool_use("Bash", command="gh pr merge 7 --squash")
        write_session(self.project, "s1", [
            assistant("2026-10-20T10:00:00Z", output_tokens=1_000_000, content=[call]),
            tool_result("2026-10-20T10:00:01Z", call["id"], "MERGED abc"),
        ])
        log = Path(self._tmp.name) / "efficiency.csv"

        with contextlib.redirect_stdout(io.StringIO()):
            sm.main([str(self.project), "--since", "2026-10-16", "--until", "2026-10-26", "--record", str(log),
                     "--repo", "o/r", "--change", "Baseline"])

        self.assertIn("Baseline,o/r,2026-10-16,2026-10-26,1,", log.read_text())


if __name__ == "__main__":
    unittest.main()
