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
