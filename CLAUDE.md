# Personal engineering baseline (applies to every repository)

Everything I build must meet this quality baseline. When starting a new repo, or when a repo is
missing parts of it, use the `quality-baseline` skill (`~/.claude/skills/quality-baseline`) to set up
or audit it. Always follow the **official conventions of the language/platform** (C#/.NET →
Microsoft; TypeScript → TypeScript/ESLint community standards; others → their official style guide).

**These are defaults.** A repository may override any item in its own `CLAUDE.md` (or README); the
repo-level rule wins, and the override should state why.

## Baseline
- **Tests**: unit + component (in-process, external dependencies stubbed, never call real third-party
  services) + load tests validating the SLO. Apply **TDD**. Test folders/namespaces mirror the source;
  shared hand-written fakes/stubs live in a `TestDoubles/` folder per test project.
- **SLO**: every repo defines one in the README, adapted to the kind of project (e.g. an HTTP service:
  latency percentiles at a sustained load and error rate; a batch job/CLI: duration per run at a
  given volume), always including protection of downstream dependencies. Its numbers are the
  load-test thresholds. The load-test pipeline publishes a report to the run summary and runs at
  least on demand (after relevant changes); a schedule is optional, per project.
- **Quality gates** (same checks locally and in CI): formatting, build with analyzers and warnings as
  errors, tests, coverage threshold (≥ 80% lines), dependency vulnerability audit, locked/pinned
  dependency restore, static analysis (CodeQL), container build + image scan.
- **Cross-platform**: when a project claims to support several OSes, CI runs the tests on each of
  them (OS matrix).
- **Local gate**: versioned git `pre-push` hook mirroring CI, enabled automatically.
- **Branch protection**: ruleset on the default branch (PRs, required checks, up-to-date branch,
  linear history, no force-push/deletion); secret scanning + push protection; Dependabot.
- **CI efficiency**: job-level path filters so unrelated changes skip jobs while required checks still report.
- **Folder structure and naming** per the platform's official conventions, documented in the README.
- **Editor/format config** (`.editorconfig`, formatter config) and centralized build/dependency config.
- **Dockerfile**: multi-stage, minimal non-root runtime image.
- **README is the single source of truth**: an *At a glance* summary first (what it does, how to run
  it, measured SLO, quality), then requirements, how to run and test, structure and conventions,
  design, SLO, assumptions, quality gates, future enhancements, and a note on the AI-assisted
  development process.
- **Repo CLAUDE.md**: short; points to the README sections instead of duplicating them, and holds
  only the rules specific to Claude (and any overrides of this baseline).
- **Repo `.claude/settings.json`** (versioned): `allow` the build/test/format/local-gate commands and
  read-only git; `ask` for `git push`.
- **Language**: code, identifiers and code comments in English; README and docs may use the
  project's language.

## Working agreements
- Commits are authored as me (my git identity), without `Co-Authored-By` trailers.
- Never `git push` without my explicit confirmation for that push.
- Discuss the analysis and alternatives with me before implementing non-trivial designs.
- Deliver one pull request per step, each built with TDD.
