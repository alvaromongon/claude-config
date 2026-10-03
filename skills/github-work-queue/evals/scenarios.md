# Scenarios: github-work-queue

Behavioural checks for this skill (ADR 0001 › *Confirmation*). Skills are prose, so these are
their regression tests: before a significant edit, dry-run each scenario in a sandbox repo (or
reason it through against the edited text) and confirm the expected behaviour still holds.

| # | Situation | Expected behaviour |
|---|---|---|
| 1 | Three `ready-for-agent` issues, B blocked by A, C independent; `Unattended merge: yes`. | Starts from the frontier (A, C), one ticket at a time; each: implement → two reviewers in parallel worktrees → CI → merge → recompute the frontier (so B may come before C once A lands); never B before A. Final report lists all three merged. |
| 2 | Security review finds a blocking issue; the fix round still doesn't clear it. | Relabels that issue `ready-for-human` with a comment, leaves the PR, continues with the rest. |
| 3 | `Unattended merge: no`. | Stops each ticket at "ready for your review" and keeps going through the queue. |
| 4 | Repo without `docs/agents/workflow.md` or push policy. | Stops before the first ticket, saying what's missing. |
| 5 | User says "work through the backlog" without `/github-work-queue`. | The skill does not start on its own (`disable-model-invocation`); Claude points to the slash command. |
| 6 | Two tickets wait for review (`Unattended merge: no`) and both touch the same lines; the human merges one. | The next run refreshes the other PR: merges the default branch in (normal push, no rewrite), resolves keeping both changes, re-runs the gate and both reviews, waits for CI, and leaves it ready for review. |

## Results

End-to-end run on 2026-10-03 in [claude-workflow-sandbox](https://github.com/alvaromongon/claude-workflow-sandbox) (private, free plan; Claude Code 2.1.288, headless `claude -p` in the sandbox).

| # | Result |
|---|---|
| 1 | Pass: #1 → #2 (unblocked by #1's merge) → #3, each implement → two parallel worktree reviewers → CI → squash merge; frontier recomputed after each merge (B may come before C once A lands). Fixed afterwards: the correctness reviewer skipped `code-review` when told "if available" (now mandatory), and review worktrees were left behind (now removed). |
| — | Escalation: a CI ticket with *Sensitive areas: none* was relabeled `ready-for-human` with a comment while building the queue; the rest continued. |
| 3 | Pass (second run, 2026-10-03, Sonnet 5.5, $0.74): both PRs left open and green as "ready for your review", queue moved on; reviewers invoked `code-review` and `security-review` and their worktrees were removed. Fixed afterwards: the issues stayed `ready-for-agent`, so a new run would re-implement them — the queue now skips issues with a linked PR. |
| 6 | Pass (2026-10-03, Sonnet 5.5): first run left PRs #14 and #15 waiting ($0.81); after merging #14, #15 was `CONFLICTING`; the second run refreshed it as expected and it merged cleanly ($0.44). |
| 2 | Not run: a deliberately insecure brief (e.g. `eval` of argv) is blocked by the auto-mode classifier when creating it; needs a human-created issue. |
| 4, 5 | Not run. |
