# Upstream watch: mattpocock/skills

Tracks how far `check-upstream-skills` has reviewed
[mattpocock/skills](https://github.com/mattpocock/skills) for improvements applicable to the
`github-*` skills in this repo (see [ADR 0001](decisions/0001-github-driven-triage-refinement-and-autonomous-implementation.md)
and `credits.md`). Updated by that skill at the end of each review, whether or not anything was
applied — so the next run knows where to start.

| Reviewed up to commit | Date reviewed | Notes |
|---|---|---|
| [`d81f3a1`](https://github.com/mattpocock/skills/commit/d81f3a183412e71a5b1e84ca21bc1a35eea03a60) | 2026-10-03 | Baseline: commit `mattpocock/skills` was at when ADR 0001 and the `github-*` skills were first written. Nothing to diff yet. |
| [`5beb35b`](https://github.com/mattpocock/skills/commit/5beb35b) | 2026-10-27 | 53 commits. Applied: `grilling` — questions worded so "yes" accepts the recommendation, in `github-shape`, `github-refine` and `github-triage`. Not applied: `to-tickets` sub-issues of the source issue (owner declined for now); already covered: `implement` ticket fetch and Skill-tool calls, `setup` label creation, `Blocked by` only as fallback. Flagged for the efficiency work: `implement-spec` advises focused checks of the fixed findings instead of a second broad review, and a deterministic loop for unattended runs; `code-review` now runs its sub-agents in the foreground. |
