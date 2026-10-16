---
name: github-refine
description: Turn a spec, design doc, or conversation into a GitHub milestone of tracer-bullet issues with blocking dependencies, each labeled ready-for-agent or ready-for-human. Use when a plan or spec is agreed and needs to become actionable tickets, or when the user asks to break a milestone/epic down into issues.
model: opus
effort: high
---

# GitHub refine

Decomposes an agreed spec into independently-deliverable **tracer-bullet** tickets (see
`references/tracer-bullets.md`), published as GitHub issues under a milestone, with blocking
dependencies and an autonomy label on each.

Modeled on `to-tickets` from [mattpocock/skills](https://github.com/mattpocock/skills) — see
`docs/credits.md`.

## Procedure

1. **Anchor**: identify the spec (a `spec` issue from `github-shape`, another issue, a doc, or the
   preceding conversation) and the milestone it belongs to. The spec must name a **success
   metric** (what is measured, the target, how); if it doesn't, stop and offer `github-shape`
   rather than inventing one. A `spec` issue must have no open `decision` blockers. Write nothing
   to GitHub yet: the milestone is created at *Publish*.
2. **Decompose**: draft the ticket list per `references/tracer-bullets.md` — prefactoring first,
   then vertical feature slices, each with its blocking edges.
3. **Quiz step**: present the numbered draft (title, one-line demoable outcome, blockers) to the
   user before publishing anything. Ask about granularity, blocking edges, and invite merges/
   splits — same spirit as `grilling`: surface the open calls, don't just publish a guess. A
   design decision taken here goes back into the spec's *Decisions* as "settled in refinement
   (date)" when you publish, so the spec stays the single record of what and why.
4. **Brief + autonomy**: for each ticket, draft the brief (`../github-triage/references/brief-
   format.md`) and decide `ready-for-agent` vs `ready-for-human` — same judgment call as
   `github-triage`: human judgment, manual/visual testing, or a sensitive area you wouldn't
   pre-approve means `ready-for-human`. Fill the brief's *Sensitive areas* field either way.
5. **Publish**, only after approval: create the milestone if it doesn't exist yet
   (`gh api repos/{owner}/{repo}/milestones -f title=... -f description=...`, linking the spec
   issue in its description), then `gh issue create --title ... --body <brief> --milestone ...
   --label <ready-for-agent|ready-for-human>` for each ticket — the brief is the issue body. Set blocking edges per
   `../github-workflow-setup/references/dependencies.md` (native relations, or the checklist
   fallback — say explicitly if you had to fall back).
6. **Report the frontier**: tell the user which ticket(s) have zero blockers and are immediately
   workable by `github-work-queue` or `github-implement`.

## Reference

- `references/tracer-bullets.md` — the vertical-slice principle, pitfalls, and prefactoring.
- `../github-triage/references/brief-format.md` — the brief format each published ticket gets.
- `../github-workflow-setup/references/dependencies.md` — how blocking edges are written.
