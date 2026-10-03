# Scenarios: github-workflow-setup

Behavioural checks for this skill (ADR 0001 › *Confirmation*). Skills are prose, so these are
their regression tests: before a significant edit, dry-run each scenario in a sandbox repo (or
reason it through against the edited text) and confirm the expected behaviour still holds.

| # | Situation | Expected behaviour |
|---|---|---|
| 1 | Fresh repo: no workflow labels, no `docs/agents/workflow.md`, no push policy. | Reports what's missing, agrees the plan, asks whether agents may push/merge; then creates the labels, workflow doc, issue forms, `needs-info-reply` workflow and the policy in `CLAUDE.md` + `settings.json` + `workflow.md`. Commits; doesn't push without the policy allowing it. |
| 2 | Fully set-up repo, nothing changed. | Reminder mode: summarizes the cycle from `docs/agents/workflow.md`; edits nothing. |
| 3 | `workflow.md` says `Unattended merge: yes` but `settings.json` keeps `gh pr merge` in `ask`. | Audit flags the mismatch between the three policy places and proposes aligning them; doesn't widen permissions without an explicit answer. |
| 4 | A label `ready-for-agent` exists with a different colour and open issues on it. | Updates colour/description only with `--force` after confirming; never deletes it. |
