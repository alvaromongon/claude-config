---
name: github-refine
description: Turn a spec, design doc, or conversation into a GitHub milestone of tracer-bullet issues with blocking dependencies — the frontier briefed and labeled ready-for-agent or ready-for-human, the rest published as outlines briefed just in time. Also re-refines a milestone's pending outlines when the work queue flags a pivot. Use when a plan or spec is agreed and needs to become actionable tickets, when the user asks to break a milestone/epic down into issues, or when a checkpoint reports that pending slices no longer fit.
model: opus
effort: high
---

# GitHub refine

Decomposes an agreed spec into independently-deliverable **tracer-bullet** tickets (see
`references/tracer-bullets.md`), published as GitHub issues under a milestone, with blocking
dependencies. Refinement is **just in time**
([ADR 0005](../../docs/decisions/0005-adaptive-milestones-findings-rule-and-two-level-design-records.md)):
the whole plan is decided and published, but only the frontier gets a full brief and an autonomy
label; the other slices are **outlines** that the work queue's checkpoint briefs once they reach
the frontier, with what the earlier tickets taught.

Modeled on `to-tickets` from [mattpocock/skills](https://github.com/mattpocock/skills) — see
`docs/credits.md`.

## Procedure

1. **Anchor**: identify the spec (a `spec` issue from `github-shape`, another issue, a doc, or the
   preceding conversation) and the milestone it belongs to. The spec must name a **success
   metric** (what is measured, the target, how); if it doesn't, stop and offer `github-shape`
   rather than inventing one. A `spec` issue must have no open `decision` blockers. Write nothing
   to GitHub yet: the milestone is created at *Publish*.
2. **Decompose**: draft the ticket list per `references/tracer-bullets.md` — prefactoring first,
   then vertical feature slices, each with its blocking edges. Order them so the success metric
   becomes **measurable as early as possible** (e.g. its check written first and failing). If it
   can only be measured once everything has landed, say so in the draft — it goes into the spec's
   *Risks* as "measurable only at close-out" — and put the slice that tests the riskiest
   assumption first.
3. **Quiz step**: present the numbered draft (title, one-line demoable outcome, blockers, and
   which slices form the frontier, and any blocker in another milestone) to the user before
   publishing anything. Ask about granularity,
   blocking edges, and invite merges/splits — same spirit as `grilling`: surface the open calls,
   don't just publish a guess. A design decision taken here goes back into the spec's *Decisions*
   as "settled in refinement (date)" when you publish, so the spec stays the single record of what
   and why.
4. **Brief + autonomy, frontier only**: for the frontier — the slices with no blockers, at most
   two — draft the brief (`../github-triage/references/brief-format.md`) and decide
   `ready-for-agent` vs `ready-for-human` — same judgment call as `github-triage`: human judgment,
   manual/visual testing, or a sensitive area you wouldn't pre-approve means `ready-for-human`.
   Fill the brief's *Sensitive areas* field either way. Every other slice gets an **outline**
   (`references/tracer-bullets.md` › *Outline issues*) and no `ready-*` label.
5. **Publish**, only after approval: create the milestone if it doesn't exist yet
   (`gh api repos/{owner}/{repo}/milestones -f title=... -f description=...`, linking the spec
   issue in its description), then `gh issue create --title ... --body <brief or outline>
   --milestone ...` for each slice, with `--label <ready-for-agent|ready-for-human>` on the
   briefed ones only. Set every slice's blocking edges, outlines included, per
   `../github-workflow-setup/references/dependencies.md` (native relations, or the checklist
   fallback — say explicitly if you had to fall back). When a blocking edge crosses milestones,
   also add the edge between the two specs if it isn't there (`dependencies.md` › *Between
   milestones*).
6. **Report the frontier**: tell the user which ticket(s) have zero blockers and are immediately
   workable by `github-work-queue` or `github-implement`, and which slices are outlines waiting to
   be briefed.

## Procedure: re-refine after a pivot

When the work queue's checkpoint reports that a pending outline no longer fits (what was learned
changes its outcome, its blockers or the order of the slices), the owner runs this skill on the
milestone:

1. Read the spec (including its *Decisions*), the milestone's issues, and the checkpoint comments
   and *Learned* sections of its merged PRs.
2. Draft the changes to the slices **not started yet** (outlines, or briefed tickets with no linked
   PR): edit an outline, add a slice, or close one as not planned with a comment saying why.
   Tickets with a linked PR and closed issues are never touched.
3. Quiz, then publish only after approval, as in the main procedure. If the change moves the
   spec's metric, *not doing* or appetite, stop and route it to `github-shape` instead.

## Reference

- `references/tracer-bullets.md` — the vertical-slice principle, pitfalls, prefactoring and the
  outline format.
- `../github-triage/references/brief-format.md` — the brief format each briefed ticket gets.
- `../github-workflow-setup/references/dependencies.md` — how blocking edges are written.
- `../github-work-queue/references/queue-policy.md` › *Checkpoint* — who briefs the outlines.
