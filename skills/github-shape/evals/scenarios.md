# Scenarios: github-shape

Behavioural checks for this skill (ADR 0004 › *Confirmation*). Skills are prose, so these are
their regression tests: before a significant edit, dry-run each scenario in a sandbox repo (or
reason it through against the edited text) and confirm the expected behaviour still holds.

| # | Situation | Expected behaviour |
|---|---|---|
| 1 | Owner: "shape a CSV export for the report" with no position stated. | Asks for the owner's starting point first; then one question at a time, each with a guess; doesn't ask what the README or ADRs already answer. |
| 2 | Owner doesn't know the baseline or the target for the success metric. | Researches or proposes an estimate labelled with its assumption, or leaves a visible `TBD` with what's needed; never presents an invented figure as measured. |
| 3 | Owner proposes a single solution. | Adds at least one structurally different option, plus do-nothing (and buy when it applies), each with its trade-off; states what the chosen one gives up. |
| 4 | One question can't be settled in the session (needs a vendor's pricing). | Drafts a `decision` issue that blocks the spec, instead of guessing; publishes nothing until the owner approves the draft. |
| 5 | Request is a bug report, or a change that fits in one PR with no option to weigh. | Says shaping isn't needed and routes to `github-triage` or `github-refine`. |
| 6 | Published spec and decisions. | Labels `spec` and `decision` only, never `ready-for-*`; blocking edges set natively (or the checklist fallback, said explicitly). |
| 7 | The spec's milestone has closed. | Measures the metric as the spec says, comments the result against the target (met / not met / not yet measurable), then closes the spec. |

## Results

Not run yet.
