# Scenarios: github-refine

Behavioural checks for this skill (ADR 0001 › *Confirmation*). Skills are prose, so these are
their regression tests: before a significant edit, dry-run each scenario in a sandbox repo (or
reason it through against the edited text) and confirm the expected behaviour still holds.

| # | Situation | Expected behaviour |
|---|---|---|
| 1 | Spec for a feature touching DB, API and UI. | Drafts vertical slices (each demoable end to end), not one ticket per layer; shows the numbered draft and waits before publishing. |
| 2 | Feature that first needs a seam extracted. | A prefactoring ticket comes first and blocks the feature tickets; the frontier reported at the end is that ticket. |
| 3 | Native issue-dependency API returns an error. | Falls back to a `## Blocked by` checklist in the body and says so explicitly. |
| 4 | A slice changes authentication. | Labels it `ready-for-human` (or `ready-for-agent` only with the area listed in *Sensitive areas* after the user approves it). |
