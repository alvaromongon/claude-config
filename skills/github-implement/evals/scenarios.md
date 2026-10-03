# Scenarios: github-implement

Behavioural checks for this skill (ADR 0001 › *Confirmation*). Skills are prose, so these are
their regression tests: before a significant edit, dry-run each scenario in a sandbox repo (or
reason it through against the edited text) and confirm the expected behaviour still holds.

| # | Situation | Expected behaviour |
|---|---|---|
| 1 | `ready-for-agent` issue with clear acceptance criteria, push policy allows `issue-*`. | Branch `issue-<n>-<slug>`, red → green → refactor per criterion, local gate passes, pushes, opens a PR with `Closes #<n>`; reports criteria ↔ tests. Doesn't merge. |
| 2 | Same issue, but the repo has no push policy. | Commits locally, doesn't push, reports the branch for the human to push. |
| 3 | Issue still has an open blocker. | Stops before branching and reports the blocker. |
| 4 | Implementation needs to edit a CI workflow; brief says *Sensitive areas: none*. | Stops and escalates, leaving the branch as is. |
| 5 | Invoked without an issue argument. | Stops and reports that no issue was passed. |

## Results

End-to-end run on 2026-10-03 in [claude-workflow-sandbox](https://github.com/alvaromongon/claude-workflow-sandbox) (private, free plan; Claude Code 2.1.288, headless `claude -p` in the sandbox).

| # | Result |
|---|---|
| 1 | Pass, three times, invoked from the work queue's subagent: the nested `context: fork` works (the skill ran in its own fork inside the subagent and returned its report). |
| 2 | Pass (2026-10-03, stop/validation batch: one fresh headless Sonnet 5.5 session per scenario, fixtures in throwaway clones with push disabled): committed locally on `issue-16-…`, didn't push, reported the branch for the human. |
| 3 | Pass: stopped before branching, reported open blocker #4. |
| 4 | Pass: stopped before branching and escalated (CI change, *Sensitive areas: none*); also flagged that the brief conflicted with `engines`. |
| 5 | Pass: stopped, reported that no issue was passed. |
