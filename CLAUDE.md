# Personal engineering baseline (applies to every repository)

Everything I build must meet this quality baseline. When starting a new repo, or when a repo is
missing parts of it, use the `quality-baseline` skill (`~/.claude/skills/quality-baseline`) to set up
or audit it. Always follow the **official conventions of the language/platform** (C#/.NET →
Microsoft; TypeScript → TypeScript/ESLint community standards; others → their official style guide).

## Baseline
- **Tests**: unit + component (in-process, external dependencies stubbed, never call real third-party
  services) + load tests validating the SLO. Apply **TDD**. Test folders/namespaces mirror the source.
- **SLO** defined in the README (latency percentiles at a sustained load, error rate, and protection
  of downstream dependencies) and enforced as load-test thresholds; scheduled load-test pipeline
  publishing a report to the run summary.
- **Quality gates** (same checks locally and in CI): formatting, build with analyzers and warnings as
  errors, tests, coverage threshold (≥ 80% lines), dependency vulnerability audit, locked/pinned
  dependency restore, static analysis (CodeQL), container build + image scan.
- **Local gate**: versioned git `pre-push` hook mirroring CI, enabled automatically.
- **Branch protection**: ruleset on the default branch (PRs, required checks, up-to-date branch,
  linear history, no force-push/deletion); secret scanning + push protection; Dependabot.
- **CI efficiency**: job-level path filters so unrelated changes skip jobs while required checks still report.
- **Folder structure and naming** per the platform's official conventions, documented in the README
  and the repo's CLAUDE.md.
- **Editor/format config** (`.editorconfig`, formatter config) and centralized build/dependency config.
- **Dockerfile**: multi-stage, minimal non-root runtime image.
- **README**: how to run and test, structure, design, SLO, assumptions, quality gates, future enhancements.
- **Repo CLAUDE.md**: layout, commands and rules for the repo.

## Working agreements
- Commits are authored as me (my git identity), without `Co-Authored-By` trailers.
- Never `git push` without my explicit confirmation for that push.
- Discuss the analysis and alternatives with me before implementing non-trivial designs.
