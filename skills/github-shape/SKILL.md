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
weighed → straight to `github-refine` (or a single issue), with its success metric stated in one
line — refine requires one either way. Shaping a one-PR change is overhead.

## Procedure: shape

1. **Starting point**: ask for the owner's position — the outcome they lean towards, their
   hypothesis, or what they don't know yet — unless they already gave it in this conversation. A
   direction recorded in an ADR or an issue counts as a guess to confirm, not as given. Read the
   repo's README, `docs/decisions/` and open `spec`/`decision` issues touching the area, so you
   never ask what you can read.
2. **Interview**: one question at a time, each with your guess and the reasoning behind it
   (`Q: … / GUESS: …`). Before the first question, state your one-sentence read of the goal and a
   confidence (0–100%) with what is missing; stop asking once you can predict the answers. Cover
   the pieces of the spec format; don't ask for what you can look up.
   - **Owner first on two pieces**: for the **success metric** (metric, target, how it's measured)
     and for **what we give up**, ask for the owner's own version *before* showing yours — then
     add your guess as a challenge or a complement. These are the pieces where reacting to a
     guess replaces the owner's judgment; everywhere else a guess to react to is fine.
   - **Pivots**: if an answer changes the goal, re-state your read and confidence, and keep the
     previous direction as an option in the draft.
   - **Appetite** may be proposed in the draft when the other answers make it predictable; the
     owner confirms it there. Size it in agent execution time, and list the human steps
     (reviews, merges, secrets, manual checks) separately.
3. **Fill the gaps**: when the owner lacks data or ideas, research them (repo, docs, primary
   sources) and propose. Label every figure **measured** (source) or **estimated** (assumption);
   never invent one — leave a visible `TBD` with what's needed to fill it. An estimate that drives
   a target gets a "measure by <date or milestone>" line in *Risks*. Propose at least two options
   with different shapes, including do-nothing and buy when they apply.
4. **Open decisions**: a question that can't be answered in this session (needs research, a
   prototype, someone else's input) becomes a **decision issue** (format in
   `references/spec-format.md`) that blocks the spec. Don't open one for what can be settled now.
5. **Draft and approve**: show the full spec draft and the list of decision issues. Publish
   nothing until the owner approves.
6. **Publish**, in this order (the spec and its decisions link each other): create the spec
   (`gh issue create --label spec`) with a placeholder in *Decisions*; create each decision issue
   (`--label decision`) linking the spec; edit the spec's *Decisions* with the decision links; then
   add the blocking edges (decision blocks spec, and another spec blocks this one when this
   spec needs what it delivers — `dependencies.md` › *Between milestones*) per
   `../github-workflow-setup/references/dependencies.md`. Never a `ready-for-*` label: specs and
   decisions are not implementation work, so `github-work-queue` never picks them up.
7. **Report**: the spec's link, its open decisions, and the next step — resolve the decisions
   (`/github-shape <decision>`), or, with none open, `github-refine` on the spec.

## Procedure: resolve a decision

Work the decision issue with the owner the same way (starting point, options, data). Code written
only to research the answer (a replay, a benchmark, a spike) stays in the scratchpad, uncommitted;
the closing comment states the method so it can be reproduced. Record the answer as a comment —
the conclusion first, then options weighed and what we give up — and update **every** section of
the spec whose figures or choices the answer changes (*Options*, *Risks*, *Decisions*, …). Then
check the spec's targets still hold with the new data; if they don't, say so and agree the change
with the owner. Close the issue. If the decision is architecture (`adr` › *Architecture only*) and
hard to reverse, surprising without context **and** a real trade-off, also record it as an ADR
with the `adr` skill, `Proposed` until this spec's close-out, and link it from the spec's
*Affects ADRs*. Design detail stays in the spec's *Decisions*.

## Procedure: close out

When the spec's milestone is closed:

1. **Done check**: none of its issues is open (a milestone is done only then —
   `../github-workflow-setup/references/findings.md` › *Invariant*). If one is, stop and report it.
2. **What was learned**: read the work queue's checkpoint comments on its PRs and the spec's
   *Decisions*, instead of reviewing the code again.
3. **Measure**: the success metric the way the spec says (run the check, read the metric); comment
   the result against the target — met, not met, or not measurable yet and when it will be. A
   missed target is a finding, not a failure to hide: say what would explain it and whether it
   calls for a new spec.
4. **Design records**, in one PR the owner reviews (push per the repo's policy): bring each
   `Proposed` ADR in *Affects ADRs* up to date with the milestone's data and accept it, or reject it
   if the milestone showed it wrong (`adr` skill); and move the design detail settled in
   *Decisions* into the flow document (`docs/flows.md`), each flow linking this spec for the *why*.
   With nothing to record, say so.
5. **Close** the spec once the design-records PR is merged, or right after step 3 when there was
   nothing to record.

## Reference

- `references/spec-format.md` — the spec and decision issue formats.
- `../github-workflow-setup/references/labels.md` — the `spec` and `decision` labels.
- `../github-workflow-setup/references/dependencies.md` — how blocking edges are written.
- `../github-refine/SKILL.md` — the next step, which requires the spec's success metric.
