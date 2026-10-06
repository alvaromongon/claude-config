---
status: Accepted
date: 2026-10-06
decision-makers: Alvaro Montero
consulted: "N/A"
---

# 0003. Assign a model per skill by role, using family aliases

- **Issue**: N/A (design conversation about which model each skill should use)
- **Supersedes**: N/A

## Context and problem statement

No skill set `model:`, and the work queue's `Agent` calls passed none, so every skill and
subagent inherited the session model — Opus 5.5 by default. Most of the volume (implementing
tickets, orchestrating the queue, auditing repos) doesn't need the most capable model, while a few
decisions (design analysis, ticket decomposition, the review gate before an unattended merge) do.
Models also change every few months, so whatever we pick must not go stale silently.

## Decision drivers

- Spend the strongest model where an error is expensive or hard to catch, not everywhere.
- Independence of the review gate: reviewers should not be weaker than the implementer.
- No maintenance on every model release; a deliberate review when the trade-offs shift.
- Prices at decision time (API, $/MTok in/out): Opus 5.5 4/20, Sonnet 5.5 2/10, Haiku 4.5 1/5,
  Fable 5.1 10/50.

## Considered options

- A. Keep inheriting the session model everywhere.
- B. Pin concrete model IDs per skill (e.g. `claude-sonnet-5-5`).
- C. Assign a family alias per skill by the role it plays (`opus` for judgment, `sonnet` for
  implementation and mechanical work), plus a periodic review recorded in `docs/model-watch.md`.

## Decision outcome

Chosen option: "C", because aliases follow each family's latest model with no edits, and tying
the choice to the skill's role means a new release only raises one question — has the balance
between families moved? The assignment:

| Role | Alias | Skills / subagents |
|---|---|---|
| Judgment: design, decomposition, review gate | `opus` | `adr`, `github-refine` (`effort: high`), work-queue reviewers |
| Implementation and rule-following work | `sonnet` | `github-implement`, `github-triage`, `github-work-queue` (orchestrator and implementer subagents), `github-workflow-setup`, `quality-baseline` |
| Manual, interactive | inherit | `check-upstream-skills` |

Haiku and Fable get no skill: every skill is an agent working over a codebase, where Haiku's 200K
context and lack of adaptive thinking weigh against it, and nothing here justifies Fable's price
by default. `effortLevel` stays at the session default (`medium`) elsewhere.

**Confidence**: medium. The split reflects each family's documented positioning, not a measured
comparison on our own scenarios. Revisit after the first work-queue runs on `sonnet`, or when a
review in `docs/model-watch.md` finds the balance has moved.

### Consequences

- Good: the high-volume path (implement, orchestrate) costs about half of what it did on Opus.
- Good: no edits needed when a family gets a new model; a release that misbehaves can be pinned
  temporarily with `ANTHROPIC_DEFAULT_SONNET_MODEL` / `ANTHROPIC_DEFAULT_OPUS_MODEL` without
  touching the skills.
- Bad: an alias upgrade changes behaviour without a commit here; mitigated by the review in
  `docs/model-watch.md` and the behavioural scenarios in `skills/*/evals/`.
- Bad: the `Agent` tool has no effort parameter, so the reviewers run at the session effort.
- Bad: not verified yet whether a skill's `model:` reverts to the session model after an inline
  (non-forked) skill finishes; until verified, an unattended run can also pass `--model sonnet`.

### Confirmation

`github-work-queue` runs in the workflow sandbox on `sonnet` and its result is recorded in
`docs/model-watch.md`. `check-upstream-skills` compares the current model line-up and prices with
this table on every run.

## Pros and cons of the options

### A. Inherit the session model

- Good: nothing to maintain; the user picks with `/model`.
- Bad: everything runs on the most expensive model in use, including mechanical work, or
  everything on a cheaper one, including the review gate.

### B. Pin model IDs

- Good: fully reproducible behaviour.
- Bad: goes stale with every release and needs edits across every skill; an outdated pin is
  silent.

### C. Role-based aliases with a periodic review (chosen)

- Good/Bad: see *Consequences*.

## More information

- Claude Code model configuration, aliases and `ANTHROPIC_DEFAULT_*_MODEL`:
  <https://code.claude.com/docs/en/model-config>
- Skill frontmatter (`model`, `effort`): <https://code.claude.com/docs/en/skills>
- Related: [0001](0001-github-driven-triage-refinement-and-autonomous-implementation.md) (the work
  queue and its review gate).
