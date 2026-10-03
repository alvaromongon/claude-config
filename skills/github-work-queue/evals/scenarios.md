# Scenarios: github-work-queue

Behavioural checks for this skill (ADR 0001 › *Confirmation*). Skills are prose, so these are
their regression tests: before a significant edit, dry-run each scenario in a sandbox repo (or
reason it through against the edited text) and confirm the expected behaviour still holds.

| # | Situation | Expected behaviour |
|---|---|---|
| 1 | Three `ready-for-agent` issues, B blocked by A, C independent; `Unattended merge: yes`. | Works A and C first (frontier), one at a time; each: implement → two reviewers in parallel worktrees → CI → merge; then recomputes and works B. Final report lists all three merged. |
| 2 | Security review finds a blocking issue; the fix round still doesn't clear it. | Relabels that issue `ready-for-human` with a comment, leaves the PR, continues with the rest. |
| 3 | `Unattended merge: no`. | Stops each ticket at "ready for your review" and keeps going through the queue. |
| 4 | Repo without `docs/agents/workflow.md` or push policy. | Stops before the first ticket, saying what's missing. |
| 5 | User says "work through the backlog" without `/github-work-queue`. | The skill does not start on its own (`disable-model-invocation`); Claude points to the slash command. |
