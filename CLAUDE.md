# Global instructions (apply to every repository)

**These are defaults.** A repository may override any item in its own `CLAUDE.md` (or README); the
repo-level rule wins, and the override should state why.

## Engineering baseline
Every repo I build meets my engineering baseline: tests (unit, component, load against the SLI/SLO),
CI quality gates mirrored by a pre-push hook, branch protection, ADR decision log, Docker and
centralized build/format config. Its full definition is the `quality-baseline` skill
(`~/.claude/skills/quality-baseline`, canonical list in `references/common.md`); use it to set up
a new repo or audit one that is missing parts of it.

Rules that apply in every session, with or without that skill:
- Follow the **official conventions of the language/platform** (C#/.NET → Microsoft;
  TypeScript → TypeScript/ESLint community standards; others → their official style guide).
- **TDD**: failing test → minimal code → refactor. Unit + component tests (in-process, external
  dependencies stubbed, never call real third-party services). Test folders/namespaces mirror the
  source; shared hand-written fakes/stubs live in a `TestDoubles/` folder per test project.
- Before finishing a change, run the repo's local quality gate (the same checks as CI).
- The **README is the single source of truth**; other docs (including the repo `CLAUDE.md`) point
  to it instead of duplicating it. Domain terms are defined once in a glossary (`docs/glossary.md`)
  and linked on first use, never redefined in place.
- **Language**: code, identifiers and code comments in English; README and docs may use the
  project's language.

## Working agreements
- Commits are authored as me (my git identity).
- Push and merge policy is per repository: its `CLAUDE.md` (enforced by its `.claude/settings.json`)
  says what may be pushed or merged without asking — e.g. repos running the autonomous GitHub
  workflow set up by `github-workflow-setup`. If a repo defines no policy, ask before every
  `git push`.
- Discuss the analysis and alternatives with me before implementing non-trivial designs, following
  *Decisions* below.
- Record decisions that are hard to reverse, surprising without context and a real trade-off as
  ADRs (MADR) in `docs/decisions/`, proposed via PR; use the `adr` skill.
- Deliver one pull request per step, each built with TDD.

## Decisions

Non-trivial decisions (designs, ADRs, proposals, PR descriptions, messages asking someone to
decide) are reasoned and written decision-first, backed by data that can be measured and checked.

**I lead, you support.** Before your own analysis, ask for my starting point — the conclusion I
lean towards, my hypothesis, or what I don't know yet — unless I've already given it. Then build on
it: bring the data and options I'm missing, point out which piece of the method below is still
weak, and draft the final version. The direction is mine; the research and the write-up can be yours.

**The method**, in this order:
1. **Conclusion** in one sentence: the decision, the answer, or what is being asked.
2. **Why it matters**: the customer, money, risk or date it affects.
3. **Options weighed**: at least two, including buy and do-nothing when they apply, each with its
   trade-off and risk.
4. **Decision and what we give up**: the accepted trade-off and what would change our mind. If it
   adds complexity, why the simple option isn't enough and how it behaves as it grows.
5. **Sequence by impact**: what goes first and why.
6. **Measurable outcome and scope**: a number (time, cost, risk, customers) with how it will be
   measured, and which teams or people it affects.

Every figure is labelled as **measured** (with its source, and for a measurement its runs, spread
and what limits it) or **estimated** (with its assumption);
a rough estimate beats no number, an invented one is never acceptable. An estimate that drives a
target gets a date or milestone by which it will be measured. Size effort in agent execution time,
with the human steps (reviews, merges, approvals) listed separately. Pick the pattern or example
the problem asks for, not the most familiar one.

## When working inside ~/.claude (this repository)

This folder mixes versioned personal standards (README.md, CLAUDE.md, skills/) with private,
non-versioned runtime state (settings.json, sessions/, cache/, history.jsonl...). I may read any
file freely, but I must only create/edit/delete files that are versioned in the repo (check with
`git check-ignore -v <path>` if in doubt). Touching any non-versioned file requires your explicit
permission.

This repo's own conventions and its overrides of the baseline are in the README › *Changing this
repository*.
