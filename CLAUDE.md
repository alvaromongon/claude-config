# Global instructions (apply to every repository)

**These are defaults.** A repository may override any item in its own `CLAUDE.md` (or README); the
repo-level rule wins, and the override should state why.

## Engineering baseline
Every repo I build meets my engineering baseline: tests (unit, component, load against an SLO),
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
  to it instead of duplicating it.
- **Language**: code, identifiers and code comments in English; README and docs may use the
  project's language.

## Working agreements
- Commits are authored as me (my git identity).
- Push and merge policy is per repository: its `CLAUDE.md` (enforced by its `.claude/settings.json`)
  says what may be pushed or merged without asking — e.g. repos running the autonomous GitHub
  workflow set up by `github-workflow-setup`. If a repo defines no policy, ask before every
  `git push`.
- Discuss the analysis and alternatives with me before implementing non-trivial designs.
- Record architecturally significant decisions as ADRs (MADR) in `docs/decisions/`, proposed via
  PR; use the `adr` skill.
- Deliver one pull request per step, each built with TDD.

## When working inside ~/.claude (this repository)

This folder mixes versioned personal standards (README.md, CLAUDE.md, skills/) with private,
non-versioned runtime state (settings.json, sessions/, cache/, history.jsonl...). I may read any
file freely, but I must only create/edit/delete files that are versioned in the repo (check with
`git check-ignore -v <path>` if in doubt). Touching any non-versioned file requires your explicit
permission.

This repo's own conventions and its overrides of the baseline are in the README › *Changing this
repository*.
