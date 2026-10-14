# Scenarios: adr

Behavioural checks for this skill (ADR 0004 › *Decision outcome*, decisions layer). Skills are
prose, so these are their regression tests: before a significant edit, dry-run each scenario in a
sandbox repo (or reason it through against the edited text) and confirm the expected behaviour
still holds.

| # | Situation | Expected behaviour |
|---|---|---|
| 1 | User asks for an ADR to rename a module, easy to revert, no alternative weighed. | Says it fails the three tests (not hard to reverse, no real trade-off) and suggests a comment on the issue or PR instead of an ADR. |
| 2 | User brings one design and two variants of it (same shape, different parameters). | Asks for or proposes at least one structurally different alternative, plus do-nothing or buy when they apply, before recommending. |
| 3 | The user's position isn't given. | Asks for it (leaning, hypothesis or open questions) before presenting its own analysis. |
| 4 | A driver cites "p95 drops to 80 ms" from a single local run. | Labels it an estimate, or asks for runs, spread and the limiter before calling it measured. |
| 5 | Decision to replace the primary datastore (hard to reverse). | Runs the doubt step: a fresh-context subagent gets only the decision and its drivers, asked to disprove it; each finding is addressed, accepted as a *Bad* consequence, or rejected with a reason; the review is noted in *More information*. |
| 6 | No figure is available for the success measure. | Leaves a visible `TBD` with what's needed to fill it; never invents a number. |

## Results

End-to-end run on 2026-10-14 in [claude-workflow-sandbox](https://github.com/alvaromongon/claude-workflow-sandbox) (Claude Code 2.1.289; one fresh headless `claude -p` session per scenario, init model Opus 5.5 — the skill's own `model: opus`; fixtures in throwaway clones with push disabled; multi-turn scenarios continued with `--resume`, the owner's answers given as the next prompt).

| # | Result |
|---|---|
| 1 | Pass: said the rename fails all three tests; recommended a PR with the reason in its description instead of an ADR. |
| 2 | Pass: called 100 vs 1000 entries variants of one shape; added disk cache, daemon, buy (`lru-cache`) and do-nothing, with measured figures (runs, range), before recommending do-nothing. |
| 3 | Pass: asked for the owner's leaning before any options or recommendation. |
| 4 | Pass: labelled the single-run 300 → 80 ms an estimate; re-measured (30 runs, p50/p95, limiter stated) and asked whether the owner's run measured the same thing. |
| 5 | Pass (2 turns): fresh-context Opus subagent got only the decision and drivers, asked to disprove it; after the owner kept SQLite, every finding is classified addressed/accepted/rejected in *More information*. |
| 6 | Pass: target left `TBD` with what's needed (named consumers), baseline from documented facts, confidence low; no invented number. |
