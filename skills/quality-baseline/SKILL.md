---
name: quality-baseline
description: Set up or audit a repository against my personal engineering quality baseline — tests (unit, component, load/SLO), CI gates, pre-push hook, branch protection, coverage, dependency audit, CodeQL, Docker, folder structure, editorconfig and centralized build config — following each language's official conventions (C#/.NET Microsoft, TypeScript, others). Use when creating a new repo/project, scaffolding a solution, or when asked to check/raise the quality of an existing repo.
---

# Quality baseline

Set up (new repo) or audit (existing repo) against the baseline in `~/.claude/CLAUDE.md`.
Items are defaults: honour overrides recorded in the repo's `CLAUDE.md`/README, and adapt the SLO and
load test to the kind of project (HTTP service, batch job/CLI, library).

## Procedure
1. **Detect** language(s), framework, package manager and what already exists. For an audit, report
   a checklist of present / missing / deviating items and agree the plan before changing anything.
2. **Discuss** the design and choices with the user before implementing (alternatives + recommendation).
3. **Scaffold** using the language reference:
   - C#/.NET → `references/csharp.md` + proven templates in `templates/csharp/`.
   - TypeScript/Node → `references/typescript.md`.
   - Other languages → apply `references/common.md` with that language's official conventions.
4. **Verify locally**: run the full local gate (pre-push hook), build the container and smoke-test it.
5. **Document**: README as single source of truth (At a glance, run, test, structure, design, SLO,
   assumptions, quality gates, enhancements), `docs/implementation-plan.md`, a short repo
   `CLAUDE.md` pointing to the README plus Claude-only rules and baseline overrides, and a
   versioned `.claude/settings.json` (`ask` for `git push`).
6. **Commit** as the user (no Co-Authored-By). Push / open PRs / change GitHub settings only with
   explicit confirmation.

## Adapting templates
Templates come from a real, CI-verified repo (HackerNews.BestStories.Api). Replace project names,
paths, endpoints and SLO numbers; re-check latest versions of packages, actions and images
(NuGet API, `gh api repos/<owner>/<action>/releases/latest`) instead of copying versions blindly.
Always read `references/common.md` for the cross-language pieces and known pitfalls.
