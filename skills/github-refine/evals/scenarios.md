# Scenarios: github-refine

Behavioural checks for this skill (ADR 0001 › *Confirmation*). Skills are prose, so these are
their regression tests: before a significant edit, dry-run each scenario in a sandbox repo (or
reason it through against the edited text) and confirm the expected behaviour still holds.

| # | Situation | Expected behaviour |
|---|---|---|
| 1 | Spec (with a success metric) for a feature touching DB, API and UI. | Drafts vertical slices (each demoable end to end), not one ticket per layer; shows the numbered draft and waits before publishing. |
| 2 | Spec (with a success metric) for a feature that first needs a seam extracted. | A prefactoring ticket comes first and blocks the feature tickets; the frontier reported at the end is that ticket. |
| 3 | Native issue-dependency API returns an error. | Falls back to a `## Blocked by` checklist in the body and says so explicitly. |
| 4 | A slice changes authentication. | On the frontier: labels it `ready-for-human` (or `ready-for-agent` only with the area listed in *Sensitive areas* after the user approves it). As an outline: its *Notes* flag the area, and the checkpoint later labels it `ready-for-human`. |
| 5 | Spec with no success metric, or a `spec` issue with an open `decision` blocker. | Stops before decomposing and offers `github-shape`; never invents the metric. |
| 6 | Spec issue approved for refinement, milestone doesn't exist yet. | Creates nothing on GitHub before the quiz step's approval; creates the milestone at *Publish*, and records any refinement-time decision in the spec's *Decisions*. |
| 7 | Spec that decomposes into five slices, one with no blockers. | Publishes all five with their blocking edges; only the frontier slice gets a brief and a `ready-*` label, the other four are `## Outline` issues with no `ready-*` label. |
| 8 | Spec whose metric can only be measured once all slices land (a dogfood run). | Says so in the draft, adds "measurable only at close-out" to the spec's *Risks* at *Publish*, and orders first the slice that tests the riskiest assumption. |
| 9 | Re-refine after a pivot: one pending outline, one briefed ticket with a linked PR, one closed ticket. | Drafts changes only for the outline; never touches the ticket with a PR or the closed one; publishes after approval, or routes to `github-shape` if the spec's metric, *not doing* or appetite would move. |

## Results

End-to-end run on 2026-10-03 in [claude-workflow-sandbox](https://github.com/alvaromongon/claude-workflow-sandbox) (private, free plan; Claude Code 2.1.288, headless `claude -p` in the sandbox).

| # | Result |
|---|---|
| 1 | Pass (CLI-only spec): three vertical slices plus a CI ticket, numbered draft shown and approved before publishing. |
| 3 | Not triggered: the native dependency endpoints (add, check, remove) all work on a private free-plan repo. |
| 2 | Pass (2026-10-03, stop/validation batch: one fresh headless Sonnet 5.5 session per scenario, fixtures in throwaway clones with push disabled): prefactoring ticket first, blocking the feature slices; draft shown, nothing published, frontier = the prefactoring ticket. |
| 4 | Partial: proposed `ready-for-agent` with *Sensitive areas: none* for the auth slices, but raised it as an explicit open question. Consistent with that repo's `workflow.md`, whose sensitive areas don't include auth — list auth there when it matters. |
| 5 | Pass (2026-10-14, Claude Code 2.1.289, fresh headless session, init model Opus 5.5, throwaway clone): `spec` issue without a success metric — stopped before decomposing, created nothing, asked for the metric and offered `github-shape`. |

Scenarios 6 added on 2026-10-16 from the first use on a real repo: not run yet.
