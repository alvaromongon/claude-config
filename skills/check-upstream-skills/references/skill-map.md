# Skill map

Which upstream `mattpocock/skills` skill informs which of ours, for scoping the diff in step 3 of
`../SKILL.md`. Changes to anything not listed here are out of scope for this skill.

| Ours | Theirs | Notes |
|---|---|---|
| `github-workflow-setup` | `setup-matt-pocock-skills` | We're GitHub-only; skip anything about alternative trackers (Linear, GitLab, local markdown). |
| `github-triage` | `triage` | Same state-machine spirit; we don't have `needs-triage` auto-applied by a bot, so onboarding changes may not apply. |
| `github-refine` | `to-tickets` | Tracer-bullet principle and pitfalls are directly portable. |
| `github-implement` | `implement` | TDD/seam/autonomy-level changes are directly portable. |
| `github-work-queue` | `implement-spec` | We're sequential, not parallel-worktree; only the non-parallel-specific parts (review timing, escalation, merge policy) port over. |
| `github-triage`, `github-refine` (interactive style) | `grilling` | The frontier/rounds question format is worth re-checking if they change it. |
| (none yet — not built) | `pr`, `code-review` | We reuse the existing `code-review` skill as-is and don't have a dedicated `pr` skill; flag upstream changes here for a future decision, don't adapt them unprompted. |
