---
name: adr
description: Write, propose, supersede or list Architecture Decision Records (ADRs, MADR 4.0 format) in a repository's docs/decisions/ folder. Use when a decision is hard to reverse, surprising without context and a real trade-off — typically structure, deployment shape, state/persistence, non-functional requirements (security, compliance, availability), dependencies or libraries, interfaces/contracts — when an issue needs a design analysis with options, when a past decision is being revisited, or when the user asks for an ADR or a decision record.
model: opus
---

# Architecture Decision Records

One ADR per decision, stored with the code. The decision log is how the system came to have its
current shape; the issue tracks the work, the ADR holds the reasoning.

## When to write one
- Write an ADR when all three hold: the decision is **hard to reverse** (changing course later is
  costly), **surprising without context** (a future reader would ask "why this way?"), and the
  result of a **real trade-off** (genuine alternatives, one chosen for specific reasons). Typical
  areas: structure, deployment/state, non-functional requirements, dependencies, interfaces. If any
  of the three is missing, a comment on the issue or PR is enough; not for implementation details.
- Brownfield: when revisiting a decision that was never recorded, first write it retroactively
  (status `Accepted`, date and source link of the original decision), then the new one that
  supersedes it.
- If one decision has phases (short/mid/long term), write one ADR per phase.

## Where and how
- Folder `docs/decisions/`, files `NNNN-title-with-dashes.md` (next sequential number, 4 digits),
  plus `docs/decisions/README.md` with an index table (number, title, status). Link that folder from
  the repo README.
- Template: `template.md` in this skill (MADR 4.0 plus a confidence level), in English. Write ADRs in
  the repo's documentation language (see its CLAUDE.md/README): English by default; if the docs are in
  another language, translate headings and statuses and keep that translation consistent across ADRs.
- Link domain terms to the repo's glossary (`quality-baseline` › *Glossary*) instead of redefining
  them; if the ADR introduces a term, add it to the glossary in the same PR.
- Keep it pithy and factual. Cite sources (regulation, vendor docs, library issues) with links. Put
  long research in *More information* or a linked document; the decision must stand on its own.
- Follow the decision method in the global `CLAUDE.md` › *Decisions*: the conclusion up front, the
  business impact, options including buy and do-nothing when they apply, the accepted trade-off,
  the sequence by impact, and a measurable outcome with its scope. Label every figure as measured (source) or estimated (assumption); never
  invent one — ask, or leave a visible `TBD` with what's needed to fill it.
- A **measured** figure carries its evidence: how many runs, the spread, and what limits it (why
  isn't it twice as good — a core, a lock, the network, the load generator itself). Without that
  it's an estimate; label it so.
- Link the success measure to what proves it: an executable check for a technical promise, a named
  metric and source for a business one (`quality-baseline` › *Decision ↔ check traceability*).
- Never hide negative consequences. State the confidence level and what would make us revisit it.

## Process
1. **Analyse** with the user before writing. Start from the user's position (leaning, hypothesis or
   open questions) — ask for it if not given — then add the data and options missing, and challenge
   the weak pieces of the method. Options, drivers, pros/cons, recommendation. The decision is the
   user's.
   - **Design it twice**: at least two **structurally different** options — whole alternatives,
     not variants or point fixes inside one shape — plus do-nothing and buy when they apply.
2. **Doubt** (when the decision is hard to reverse, or confidence is low): before proposing, hand a
   fresh-context subagent (`Agent`, `model: opus`) only the decision in three to five sentences
   and its drivers — not the conversation — and ask it to **disprove** it: failure modes,
   unstated assumptions, a missed option, a number that doesn't hold. Classify each finding as
   addressed (change the ADR), accepted (record it under *Bad* consequences) or rejected (say why),
   and note the review in *More information*. One round; a second only if the first changed the
   decision. If you're already inside a subagent, say the review couldn't run instead of
   faking it.
3. **Propose**: open a PR adding the ADR with status `Proposed` and linking the issue (the issue links
   back). The PR review is the discussion.
4. **Accept**: once the user decides, set the chosen option, status `Accepted` and date, update the
   index, and merge. Implementation goes in separate PRs that link the ADR.
5. **Reject**: keep the file with status `Rejected` and the reason, so the debate isn't reopened.
6. **Immutable once accepted**: never rewrite an accepted ADR's decision. To change it, write a new ADR;
   when it's accepted, set the old one to `Superseded by [NNNN](NNNN-...md)` (the only edit allowed,
   plus fixing typos/links) and link the new one back with `Supersedes`.
7. Code reviews check changes against accepted ADRs.
