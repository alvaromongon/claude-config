# Scenarios: check-upstream-skills

Behavioural checks for this skill (ADR 0001 › *Confirmation*). Skills are prose, so these are
their regression tests: before a significant edit, dry-run each scenario in a sandbox repo (or
reason it through against the edited text) and confirm the expected behaviour still holds.

| # | Situation | Expected behaviour |
|---|---|---|
| 1 | Upstream changed `to-tickets` slicing guidance. | Proposes a concrete edit to `github-refine`/`tracer-bullets.md`; applies only after approval; appends a row to `docs/upstream-watch.md`. |
| 2 | Upstream only changed unrelated skills (`prototype`, `teach`). | Proposes nothing, still appends a row noting "nothing applicable". |
| 3 | Upstream change is about parallel worktrees in `implement-spec`. | Explains why it doesn't apply to the sequential queue yet; no edit. |
| 4 | Last row in `docs/model-watch.md` is over three months old, or a new model family has appeared since. | Compares the line-up and prices with ADR 0003, proposes any reassignment (a superseding ADR, not an edit to 0003); edits nothing without approval; appends a row to `docs/model-watch.md`. |
| 5 | Recent model review and no new models or price changes. | Says the assignment is current; appends no model-watch row. |
