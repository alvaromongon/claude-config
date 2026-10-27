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
   table) with the assignment in ADR 0003, plus `github-shape` (`opus`, judgment role — added by
   ADR 0004 after 0003 was accepted).
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
| 2026-10-27 | Fable 5.1, Opus 5.5, Sonnet 5.5, Haiku 5.5 | Trigger fired: Haiku 5.5 is new (1M context, adaptive thinking, $0.10/$0.50 per MTok for prompts up to 100k tokens), so ADR 0003's reasons for giving Haiku no skill no longer hold; the owner deferred evaluating it — no change. Cache reads cost 0.05× of input on Opus and Sonnet 5.5 (0.025× on Fable 5.1); `session-metrics` corrected. First real queue runs (finance-agent, 4 runs, 2026-10-17 to 2026-10-26), measured from transcripts: the orchestrator's `model: sonnet` holds only for the first turn — in 3 of 4 runs the session went back to `opus` once the first subagent returned, so 40% of the estimated cost was the orchestrator on `opus`. Subagent models held as assigned. Assignment unchanged; making the orchestrator stay on `sonnet` is the next change to measure ([efficiency](efficiency.md)). |
| 2026-10-27 | Fable 5.1, Opus 5.5, Sonnet 5.5, Haiku 5.5 | Keeping the work-queue orchestrator on `sonnet` ([#11](https://github.com/alvaromongon/claude-config/issues/11)), measured in the workflow sandbox (Claude Code 2.1.289, headless, one ticket per run, models read per main-session call from the transcripts): **baseline** (session on Opus, skill `model: sonnet`) — 5 calls on `sonnet`, then 7 on `opus` from the first subagent's notification on, i.e. the skill's model covers only the turn it is invoked in; **`context: fork`** — fails: the fork launched the implementer and returned, and the main session orchestrated on `opus` (47 of 47 calls); **session started with `--model sonnet`** — holds: 11 of 11 calls on `sonnet`, reviewers still on `opus`. Applied: the skill now says before its first ticket to start the session on Sonnet (`queue-policy.md` › *Session model*); `model: sonnet` stays for the first turn. Estimated orchestrator cost (list prices, main-session calls only): $0.50 baseline ($0.40 of it `opus`) vs $0.16 — different one-ticket runs, so indicative only. |
