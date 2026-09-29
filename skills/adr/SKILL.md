---
name: adr
description: Write, propose, supersede or list Architecture Decision Records (ADRs, MADR 4.0 format) in a repository's docs/decisions/ folder. Use when a decision is architecturally significant — structure, deployment shape, state/persistence, non-functional requirements (security, compliance, availability), dependencies or libraries, interfaces/contracts, anything hard to reverse — when an issue needs a design analysis with options, when a past decision is being revisited, or when the user asks for an ADR or a decision record.
---

# Architecture Decision Records

One ADR per decision, stored with the code. The decision log is how the system came to have its
current shape; the issue tracks the work, the ADR holds the reasoning.

## When to write one
- Write an ADR for decisions that affect structure, deployment/state, non-functional requirements,
  dependencies, interfaces, or that are **hard to reverse**. Not for implementation details.
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
- Keep it pithy and factual. Cite sources (regulation, vendor docs, library issues) with links. Put
  long research in *More information* or a linked document; the decision must stand on its own.
- Never hide negative consequences. State the confidence level and what would make us revisit it.

## Process
1. **Analyse** with the user before writing: options, drivers, pros/cons, recommendation. The decision
   is the user's.
2. **Propose**: open a PR adding the ADR with status `Proposed` and linking the issue (the issue links
   back). The PR review is the discussion.
3. **Accept**: once the user decides, set the chosen option, status `Accepted` and date, update the
   index, and merge. Implementation goes in separate PRs that link the ADR.
4. **Reject**: keep the file with status `Rejected` and the reason, so the debate isn't reopened.
5. **Immutable once accepted**: never rewrite an accepted ADR's decision. To change it, write a new ADR;
   when it's accepted, set the old one to `Superseded by [NNNN](NNNN-...md)` (the only edit allowed,
   plus fixing typos/links) and link the new one back with `Supersedes`.
6. Code reviews check changes against accepted ADRs.
