# Model watch

Tracks reviews of the per-skill model assignment from
[ADR 0003](decisions/0003-assign-models-per-skill-by-role.md). Skills use family aliases
(`opus`, `sonnet`), so a new model in a family is picked up automatically; what needs a review is
whether the **balance between families** has moved.

## When to review

- A new model family or tier appears, or an existing family gets a major release.
- Prices change noticeably between families.
- A skill shows a quality problem that a different family might fix (or a cost that a cheaper
  family might cut).
- Otherwise, at least every three months — `check-upstream-skills` checks this on every run.

## How to review

1. Compare the current line-up and prices (Claude Code `/model`, the `claude-api` skill's model
   table) with the assignment in ADR 0003.
2. For each role whose best fit may have changed, run the affected skills' `evals/scenarios.md` in
   the workflow sandbox with the candidate alias, and compare against the current one.
3. If the assignment should change, write a new ADR superseding 0003; then edit the skills'
   `model:` frontmatter and `queue-policy.md`.
4. Append a row below, even when nothing changes.

To pin one family temporarily (e.g. a release that misbehaves), set
`ANTHROPIC_DEFAULT_SONNET_MODEL` or `ANTHROPIC_DEFAULT_OPUS_MODEL` instead of editing skills.

| Date | Line-up reviewed | Outcome |
|---|---|---|
| 2026-10-06 | Fable 5.1, Opus 5.5, Sonnet 5.5, Haiku 4.5 | Initial assignment (ADR 0003). Pending: first `github-work-queue` run on `sonnet` in the sandbox. |
