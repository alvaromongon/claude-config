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

## Results

End-to-end run on 2026-10-03 in [claude-workflow-sandbox](https://github.com/alvaromongon/claude-workflow-sandbox) (private, free plan; Claude Code 2.1.288, headless `claude -p` in the sandbox).

| # | Result |
|---|---|
| 1 | Pass (CLI-only spec): three vertical slices plus a CI ticket, numbered draft shown and approved before publishing. |
| 3 | Not triggered: the native dependency endpoints (add, check, remove) all work on a private free-plan repo. |
| 2 | Pass (2026-10-03, stop/validation batch: one fresh headless Sonnet 5.5 session per scenario, fixtures in throwaway clones with push disabled): prefactoring ticket first, blocking the feature slices; draft shown, nothing published, frontier = the prefactoring ticket. |
| 4 | Partial: proposed `ready-for-agent` with *Sensitive areas: none* for the auth slices, but raised it as an explicit open question. Consistent with that repo's `workflow.md`, whose sensitive areas don't include auth — list auth there when it matters. |
