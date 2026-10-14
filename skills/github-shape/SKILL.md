---
name: github-shape
description: Shape a loose idea into an agreed spec issue on GitHub — problem, why it matters, success metric, appetite, options, not doing — with open questions tracked as blocking decision issues, ready for github-refine. Also closes a shaped spec once its milestone is done, checking the metric. Use when the owner brings an idea, feature or change that isn't bounded yet, asks to shape/define/scope something, or a spec issue's milestone has closed. Not for bugs or already-bounded work — that goes to github-triage or github-refine.
model: opus
---

# GitHub shape

The step before `github-refine`: decides **what and why**, so refinement only decides **how to
slice**. The output is one issue labeled `spec` (format in `references/spec-format.md`) that
`github-refine` takes as its input. Design: ADR 0004 in `claude-config`.

Follows the global `CLAUDE.md` › *Decisions*: **the owner leads, Claude supports**. The owner sets
the direction; Claude brings the data, options and draft, and challenges the weak pieces.

Draws on `wayfinder` from [mattpocock/skills](https://github.com/mattpocock/skills), `interview-me`
from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) and shaping from
[Shape Up](https://basecamp.com/shapeup) — see `docs/credits.md`.

## When to skip

Say so and route elsewhere when the work is already bounded: a bug or an external report →
`github-triage`; a change whose problem, outcome and scope fit in two sentences and need no option
weighed → straight to `github-refine` (or a single issue). Shaping a one-PR change is overhead.

## Procedure: shape

1. **Starting point**: ask for the owner's position — the outcome they lean towards, their
   hypothesis, or what they don't know yet — unless they already gave it. Read the repo's README,
   `docs/decisions/` and open `spec`/`decision` issues touching the area, so you never ask what
   you can read.
2. **Interview**: one question at a time, each with your guess and the reasoning behind it
   (`Q: … / GUESS: …`). Before the first question, state your one-sentence read of the goal and a
   confidence (0–100%) with what is missing; stop asking once you can predict the answers. Cover
   the pieces of the spec format; don't ask for what you can look up.
3. **Fill the gaps**: when the owner lacks data or ideas, research them (repo, docs, primary
   sources) and propose. Label every figure **measured** (source) or **estimated** (assumption);
   never invent one — leave a visible `TBD` with what's needed to fill it. Propose at least two
   options with different shapes, including do-nothing and buy when they apply.
4. **Open decisions**: a question that can't be answered in this session (needs research, a
   prototype, someone else's input) becomes a **decision issue** (format in
   `references/spec-format.md`) that blocks the spec. Don't open one for what can be settled now.
5. **Draft and approve**: show the full spec draft and the list of decision issues. Publish
   nothing until the owner approves.
6. **Publish**: `gh issue create --label spec` for the spec and `--label decision` for each decision
   issue, then the blocking edges (decision blocks spec) per
   `../github-workflow-setup/references/dependencies.md`. Never a `ready-for-*` label: specs and
   decisions are not implementation work, so `github-work-queue` never picks them up.
7. **Report**: the spec's link, its open decisions, and the next step — resolve the decisions
   (`/github-shape <decision>`), or, with none open, `github-refine` on the spec.

## Procedure: resolve a decision

Work the decision issue with the owner the same way (starting point, options, data). Record the
answer as a comment — the conclusion first, then options weighed and what we give up — update the
spec's *Options* or *Decisions* section if it changes, and close the issue. If the decision is
hard to reverse, surprising without context **and** a real trade-off, also record it as an ADR
with the `adr` skill and link it.

## Procedure: close out

When the spec's milestone is closed: measure the success metric the way the spec says (run the
check, read the metric), comment the result against the target — met, not met, or not measurable
yet and when it will be — and close the spec. A missed target is a finding, not a failure to hide:
say what would explain it and whether it calls for a new spec.

## Reference

- `references/spec-format.md` — the spec and decision issue formats.
- `../github-workflow-setup/references/labels.md` — the `spec` and `decision` labels.
- `../github-workflow-setup/references/dependencies.md` — how blocking edges are written.
- `../github-refine/SKILL.md` — the next step, which requires the spec's success metric.
