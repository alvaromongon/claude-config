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
| 8 | Interview reaches the success metric and *What we give up*. | Asks for the owner's own version of each first, then adds its guess as a challenge or complement — never offers its guess first on these two. |
| 9 | Owner's answer changes the goal mid-interview. | Re-states its read and confidence; keeps the previous direction as an option in the draft. |
| 10 | A decision's research changes a figure the spec's target depends on. | Updates every affected section (*Options*, *Risks*, *Decisions*), re-checks the target against the new data and agrees any change with the owner; research code stays uncommitted, method in the closing comment. |
| 11 | Close-out requested, but one of the milestone's issues is still open. | Doesn't close the spec; reports the open issue. When all are closed, reads the checkpoint comments on the milestone's PRs rather than reviewing the code again. |
| 12 | Close-out of a spec with one `Proposed` ADR in *Affects ADRs* and three design choices "settled in checkpoint" in *Decisions*. | Opens one PR that brings the ADR up to date and accepts it, and moves the three choices into `docs/flows.md` with a link to the spec; closes the spec only after that PR is merged. |

## Results

End-to-end run on 2026-10-14 in [claude-workflow-sandbox](https://github.com/alvaromongon/claude-workflow-sandbox) (Claude Code 2.1.289; one fresh headless `claude -p` session per scenario, init model Opus 5.5 — the skill's own `model: opus`; fixtures in throwaway clones with push disabled; multi-turn scenarios continued with `--resume`, the owner's answers given as the next prompt).

| # | Result |
|---|---|
| 1 | Pass: read README, code and open `spec`/`decision` issues first, stated its read of the goal (confidence 30%), asked for the owner's starting point, then one `Q:`/`GUESS:` question. |
| 2 | Pass: time saved left `TBD` (no usage data) and said so; proposed a checkable technical metric instead, with each baseline labelled measured (1 run). |
| 3 | Pass: added stdin (structurally different) and do-nothing beside the owner's `--files`, each with its trade-off, plus *What we give up*; also flagged that the change might skip shaping. |
| 4 | Pass (2 turns): first researched list prices and asked for the volume (could the decision be settled today?); once the owner said quotes need finance, drafted a `decision` issue blocking the spec, inputs `TBD`, nothing published. |
| 5 | Pass: bug report (which didn't reproduce) declined for shaping; routed to a single issue or `github-refine`. |
| 6 | Pass (3rd turn of #4, after approval): spec labelled `spec`, decision `decision`, no `ready-for-*`; native blocked-by edge set and verified. |
| 7 | Pass: ran the spec's checks (`upper "hi there"`, `npm run gate`), commented met against the target with how it was measured, closed the spec as completed. |

Scenarios 8–10 added on 2026-10-16 from the first use on a real repo: not run yet.
