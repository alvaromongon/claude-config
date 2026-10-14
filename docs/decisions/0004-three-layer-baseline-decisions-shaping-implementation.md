---
status: Accepted
date: 2026-10-14
decision-makers: Alvaro Montero
consulted: "N/A"
---

# 0004. A three-layer baseline: decisions, shaping and implementation, with a new `github-shape`

- **Issue**: N/A (design conversation comparing three public skill sets with this repository)
- **Supersedes**: N/A (extends [0001](0001-github-driven-triage-refinement-and-autonomous-implementation.md))

**Decision**: the personal standards cover three layers, each with a quality bar: **decisions**
(the method in `CLAUDE.md` › *Decisions* plus `adr`), **shaping** (a new `github-shape` skill that
turns an idea into an agreed spec issue with a success metric) and **implementation** (the existing
`github-refine` → `github-implement` chain and `quality-baseline`). Every milestone refined from now
on starts from a shaped spec that names its success metric.

## Context and problem statement

[0001](0001-github-driven-triage-refinement-and-autonomous-implementation.md) built the GitHub
workflow from triage onwards: `github-refine` takes an **agreed** spec and slices it into tickets.
Nothing covers how a spec gets agreed. That step happens in loose conversations, so the problem,
why it matters, the options weighed, what is left out and how success will be measured are not
recorded anywhere `github-refine` can read. The decision method added to `CLAUDE.md` (and the
decision ↔ check traceability in `quality-baseline`) has no place to land before the tickets exist.

**Why it matters**: the owner works alone across several repos and wants every piece of work to be
traceable from its business reason to the check that proves it. Today 0 of the specs that
`github-refine` receives carry a success metric (measured: no skill or template asks for one), so
implemented work can only be checked against its tickets, never against the outcome it was for.

## Decision drivers

- Decisions are led by the owner and reasoned with Claude's help (`CLAUDE.md` › *Decisions*): the
  owner sets the direction, Claude brings data, options and the draft.
- A measurable outcome must flow down: spec metric → ticket acceptance criteria → executable check.
- Fit a single maintainer on GitHub: no concurrency or multi-team machinery.
- Keep context lean and the set small: add a skill only where a whole phase is missing; otherwise
  enrich an existing one.
- Learn from prior art without adopting it wholesale ([0001](0001-github-driven-triage-refinement-and-autonomous-implementation.md)'s
  reasoning on vendor lock-in still holds).

## Considered options

- A. Do nothing: keep the agreement step as free conversation before `github-refine`.
- B. Adopt one external set as-is: [mattpocock/skills](https://github.com/mattpocock/skills),
  [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) or pstack (Lauren Tan's
  Cursor stack; read through the [michael-denyer/pstack-claude](https://github.com/michael-denyer/pstack-claude) port).
- C. Add shaping as a first phase inside `github-refine`.
- D. Three layers with one new skill, `github-shape`, and selected ideas from each set folded into
  the existing skills.

## Decision outcome

Chosen option: "D", because shaping (what and why) and refinement (how to slice) answer different
questions at different times, and only shaping is missing; the other two layers need enrichment,
not new skills.

| Layer | Skills | What changes |
|---|---|---|
| Decisions | `adr` + `CLAUDE.md` › *Decisions* | Enriched: write an ADR only when hard to reverse, surprising without context **and** a real trade-off (Pocock); at least two structurally distinct designs (pstack *design it twice*); a measured number carries its runs, spread and limiter (pstack *explain the number*); optional fresh-context adversarial review for hard-to-reverse decisions (Addy *doubt-driven*) |
| Shaping | **`github-shape`** (new) | From the owner's starting point to a spec issue: problem, why it matters, success metric, options, appetite, *not doing*. Open questions become decision issues blocking the spec (a light version of Pocock's `wayfinder`). One question at a time, each with Claude's hypothesis attached (Addy `interview-me`). Its output is `github-refine`'s input |
| Implementation | `github-refine`, `github-implement`, `github-work-queue`, `quality-baseline` | Unchanged now. Later: a `retro` skill (mechanical lessons become checks, Pocock `retro` / pstack *encode lessons in structure*) and review flags for a lowered bar (thresholds edited down, skipped tests; Addy `constraint-driven`) |

Naming: *shape* comes from Shape Up (Basecamp), where shaping defines problem, appetite, rough
solution and no-gos before work is committed — this phase exactly, and built for small teams.
*Groom* was rejected: Scrum replaced it with *refinement*, which `github-refine` already uses. The
`github-` prefix is kept because the output lives in GitHub issues and feeds `github-refine`;
the coupling is the one [0001](0001-github-driven-triage-refinement-and-autonomous-implementation.md)
accepted.

Delivery, one PR each: (1) `github-shape`; (2) `adr` enrichments; (3) later, `retro` and the
lowered-bar review flags. `docs/credits.md` and `check-upstream-skills` gain the two new sources.

**Confidence**: medium. The gap is clear, but how often work arrives vague enough to need shaping is
not measured. Revisit if, after three milestones, most were refined without a shaped spec because
the work was already well bounded — then fold shaping into `github-refine` (option C).

### Consequences

- Good: the method in `CLAUDE.md` gets a recorded artefact before any ticket exists, and the spec's
  metric gives `quality-baseline`'s traceability something to trace to.
- Good: each external idea is taken for a specific gap, with its source credited.
- Bad: one more skill to maintain, and `check-upstream-skills` watches three sources instead of one.
- Bad: shaping adds a step before refinement; for small, well-bounded work it is overhead (the skill
  should say when to skip it).

### Confirmation

`github-shape` ships with behavioural scenarios in `skills/github-shape/evals/scenarios.md`
(starts from the owner's position, refuses to invent a metric, publishes the spec only after
approval). `github-refine`'s procedure checks that its input spec names a success metric.

**Success measure**: share of new milestones whose spec issue names a success metric — target: all
of the next three milestones. Read from the milestones' spec issues with `gh`; baseline 0 (measured,
2026-10-14).

## Pros and cons of the options

### A. Do nothing

- Good: no work, no new skill.
- Bad: the decision method stays prose with no artefact; specs keep arriving without a metric.

### B. Adopt one external set as-is

- Good: fastest; each is maintained and widely used (GitHub stars on 2026-10-14, measured:
  mattpocock/skills 290,986; addyosmani/agent-skills 106,612; pstack-claude 1,992).
- Neutral: Pocock's set already covers several trackers; Addy's covers the whole SDLC in 25 skills.
- Bad: each fits a different case — Addy's is broad and web-oriented, pstack relies on multi-model
  arenas built for Cursor, Pocock's `wayfinder` carries concurrency machinery a single maintainer
  doesn't need — and adopting any one brings back the lock-in [0001](0001-github-driven-triage-refinement-and-autonomous-implementation.md) rejected.

### C. Shaping as a first phase of `github-refine`

- Good: no new skill; one entry point.
- Bad: mixes two questions (what and why vs how to slice) that happen at different times, often
  sessions apart; makes `github-refine` heavier on every run, including when the spec is already
  agreed.

### D. Three layers, one new skill (chosen)

- Good/Bad: see *Consequences*.

## More information

- Prior art read for this decision: Pocock's `wayfinder`, `grilling`/`grill-with-docs`, `to-spec`,
  `domain-modeling`, `retro`; Addy's `interview-me`, `idea-refine`, `doubt-driven-development`,
  `constraint-driven-development`; pstack's `architect`, `interrogate` and its principles
  (*explain the number*, *exhaust the design space*, *attack the premise*, *encode lessons in
  structure*).
- Shape Up, chapters on shaping: <https://basecamp.com/shapeup>
- Related: [0001](0001-github-driven-triage-refinement-and-autonomous-implementation.md) (the
  workflow this extends), [0003](0003-assign-models-per-skill-by-role.md) (`github-shape` is a
  judgment role → `opus`).
