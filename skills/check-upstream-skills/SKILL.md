---
name: check-upstream-skills
description: Diff mattpocock/skills since the last reviewed commit and propose applicable improvements to our github-* skills. Use on demand when the user wants to check for upstream improvements, not automatically — this is a manual, occasional review, not a background sync.
disable-model-invocation: true
---

# Check upstream skills

On-demand review of [mattpocock/skills](https://github.com/mattpocock/skills) for improvements
applicable to the `github-*` skills modeled on it (see `docs/credits.md`,
[ADR 0001](../../docs/decisions/0001-github-driven-triage-refinement-and-autonomous-implementation.md)).
Proposes changes; never applies anything without approval.

## Procedure

1. **Read the marker**: last reviewed commit from `docs/upstream-watch.md`.
2. **Diff**: `gh api repos/mattpocock/skills/compare/<marker>...main` for the file/commit list,
   plus any new entries under `.changeset/` (that repo uses changesets, which summarize each
   change in plain English — cheaper to read than raw diffs).
3. **Filter** to changes touching anything in `references/skill-map.md`'s mapping, or the shared
   `grilling`/`writing-for-agents` primitives that inform `github-triage`/`github-refine`'s
   interactive style. Ignore unrelated skills (e.g. `prototype`, `teach`) — they have no
   equivalent here.
4. **Assess** each relevant change: what it does upstream, and whether it applies given our
   constraints (GitHub-only tracker, own naming, no vendor lock, sequential-only work queue for
   now). Some won't translate — say why, don't force a fit.
5. **Propose**: list candidate edits (file + what would change) to the user; apply only the ones
   approved, as normal edits to the relevant `SKILL.md`/`references/*.md`.
6. **Update the marker**: append a row to `docs/upstream-watch.md` with the new commit reviewed,
   today's date, and a one-line note of what was found/applied — even if nothing was applicable,
   so the next run doesn't re-review the same range.

## Reference

- `references/skill-map.md` — which of our skills maps to which of theirs.
- `../../docs/upstream-watch.md` — the last-reviewed marker this skill reads and updates.
