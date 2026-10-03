---
status: Accepted
date: 2026-10-03
decision-makers: Alvaro Montero
consulted: "N/A"
---

# 0001. GitHub-driven workflow for triage, refinement, and autonomous ticket implementation

- **Issue**: N/A (design conversation)
- **Supersedes**: N/A

## Context and problem statement

This repository already covers code quality (`quality-baseline`) and decision records (`adr`), plus
a reusable `code-review` skill. What's missing is the layer that turns GitHub issues/milestones into
a repeatable triage → refinement → implementation loop, with enough autonomy that the agent can work
through a queue of ready tickets without requiring a review request after every single one — while
staying easy to understand, modify, and extend over time (no vendor lock to any third-party skill
set), and with honest attribution where the design draws on prior art.

## Decision drivers

- Avoid vendor lock-in: understand and be able to modify every piece; no opaque dependency on a
  third-party skill package.
- Honest attribution to the prior art that inspired the design ([mattpocock/skills](https://github.com/mattpocock/skills)).
- Stay in sync with upstream improvements without re-adopting them blindly.
- Reuse existing baseline pieces (`adr`, `code-review`, `quality-baseline`) rather than duplicating them.
- Per-issue (not per-repo) control over how much autonomy the agent gets.
- Predictable, inspectable escalation behavior when the agent should stop and ask.
- Keep session context lean — skills/agents should load only when needed.

## Considered options

- A. Adopt Matt Pocock's `mattpocock/skills` plugin as-is (e.g. via his `setup-matt-pocock-skills`).
- B. Build a bespoke set of skills from scratch, unrelated to any prior art.
- C. Build our own skills, one per phase, modeled on Matt Pocock's proven structure, with explicit
  attribution and an upstream-review mechanism; integrate with the existing `adr`/`code-review`; use
  subagents (via the `Agent` tool) for implementation and review isolation; sequential (not parallel)
  autonomous execution in v1; per-issue autonomy via GitHub labels.

## Decision outcome

Chosen option: "C", because it gives full understanding and control over every piece (no vendor
lock), integrates cleanly with what already exists in this baseline, and lets us track and
selectively absorb improvements from a well-tested prior-art design instead of reinventing or
blindly copying it.

**Confidence**: medium. Revisit if the sequential work-queue proves too slow in practice (motivating
the deferred parallel/worktree model sooner), or if GitHub's native blocking-issue relations prove
unreliable or unavailable on the plan used, forcing a fallback to checklist-based blocking in issue
bodies.

### Consequences

- Good: each skill is small, independently understandable, and maps roughly 1:1 to a Matt Pocock
  skill, making upstream diffs easy to evaluate and selectively apply.
- Good: per-issue autonomy (labels) is more flexible than an all-or-nothing repo flag — this repo
  (the baseline) can stay supervised while downstream repos run autonomously, issue by issue.
- Good: skills only load their full body into context when invoked, so splitting into five skills
  costs close to nothing in sessions that only use one of them.
- Bad: more moving parts to set up per repo (`github-workflow-setup`) than a single monolithic skill.
- Bad: sequential work-queue in v1 is slower than parallel worktrees; large backlogs process one
  ticket at a time until the deferred parallel model is built.
- Bad: relies on GitHub-native issues/milestones; unlike Matt Pocock's design, this one does not
  support other trackers (Linear, GitLab, local markdown).

### Confirmation

Each new skill is validated against 2-3 concrete scenarios defined before writing it (spec-first),
by dry-running it against a sandbox repo and checking its behavior matches. Strict TDD (red/green
over code) does not apply to prose-based skills. Delivered as one incremental PR per skill, in the
order listed under *More information*, so each piece is reviewed and understood before the next is
built on top of it.

## Pros and cons of the options

### A. Adopt mattpocock/skills as-is

- Good: fastest to get running; battle-tested in production by its author.
- Neutral: already supports multiple trackers (GitHub, GitLab, local markdown) and multiple agent
  platforms (its `agents/openai.yaml` adapters).
- Bad: direct vendor lock — upstream changes or removals propagate without us understanding why;
  harder to align with this repo's existing `adr`/`code-review`/`quality-baseline` conventions.
- Bad: no control over naming, scope, or pacing of the rollout.

### B. Build bespoke, unrelated to any prior art

- Good: no attribution overhead; fully free-form design.
- Bad: reinvents a design that already has known failure modes and fixes documented by someone who
  iterated on it publicly; higher risk of repeating mistakes already solved (e.g. horizontal vs.
  tracer-bullet ticket slicing, false-failure review timing on parallel runs).

### C. Own skills modeled on Matt Pocock's structure (chosen)

- Good: see *Decision outcome* and *Consequences* above.
- Bad: requires an explicit attribution and upstream-review process to stay honest and current,
  which is extra process overhead beyond just writing the skills.

## More information

- Prior art: [mattpocock/skills](https://github.com/mattpocock/skills) — in particular `triage`,
  `to-tickets`, `implement`, `implement-spec`, `pr`, `code-review`, `setup-matt-pocock-skills`, and
  the `grilling` interview primitive. Credited centrally in a future credits note and referenced
  per-`SKILL.md`.

- Architecture agreed in the design conversation that produced this ADR:
  - **Concept mapping**: GitHub Milestone = spec/epic; GitHub Issue = tracer-bullet ticket; blocking
    dependencies = GitHub's native issue-blocking relations.
  - **Per-issue autonomy** via labels: `ready-for-agent` (agent may work it without per-step
    approval) vs. `ready-for-human` (requires supervision); issues missing `ready-for-agent` are
    never auto-picked by the work queue.
  - **New skills**, one per phase, each referencing its Matt Pocock equivalent as inspiration:
    - `github-workflow-setup` — creates/audits required labels and writes the workflow
      documentation into the child repo (analogous to `setup-matt-pocock-skills`); also serves as an
      on-demand reminder of the process.
    - `github-triage` — classifies incoming issues (analogous to `triage`).
    - `github-refine` — turns a spec/milestone into tracer-bullet issues with blocking edges
      (analogous to `to-tickets`).
    - `github-implement` — executes one `ready-for-agent` issue with TDD, run as an isolated
      subagent per ticket (analogous to `implement`).
    - `github-work-queue` — sequentially processes the `ready-for-agent` queue: for each issue,
      spawns an implementer subagent, then a separate reviewer subagent (reusing the existing
      `code-review` skill, fresh context, "report only, don't edit" prompt — the same pattern Matt
      Pocock uses), waits for CI/merge, then moves to the next issue; escalates to the user on:
      unstable tests after N attempts, acceptance criteria that turn out ambiguous mid-
      implementation, changes touching sensitive areas (auth/payments/infra/CI), or an issue lacking
      the `ready-for-agent` label.
    - `check-upstream-skills` — on-demand skill that diffs Matt Pocock's repo since the last
      reviewed point and proposes applicable improvements to our skills.
  - **Deferred** to a future ADR/iteration: parallel ticket execution across isolated git worktrees
    (analogous to `implement-spec`), which `github-work-queue` deliberately does not attempt yet.
  - **Delivery plan**: one PR per skill, in this order — `github-workflow-setup` (+ labels) →
    `github-triage` → `github-refine` → `github-implement` → `github-work-queue` (+ `code-review`
    integration) → `check-upstream-skills`.
