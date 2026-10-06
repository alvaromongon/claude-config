---
name: quality-baseline
description: Set up or audit a repository against my personal engineering quality baseline — tests (unit, component, load/SLO), CI gates, pre-push hook, branch protection, coverage, dependency audit, CodeQL, Docker, ADR decision log, folder structure, editorconfig and centralized build config — following each language's official conventions (C#/.NET Microsoft, TypeScript, others). Use when creating a new repo/project, scaffolding a solution, or when asked to check/raise the quality of an existing repo.
model: sonnet
---

# Quality baseline

Set up (new repo) or audit (existing repo) against the baseline defined in `references/common.md`.
Items are defaults: honour overrides recorded in the repo's `CLAUDE.md`/README, and adapt the SLO and
load test to the kind of project (HTTP service, batch job/CLI, library).

## Procedure
1. **Detect** language(s), framework, package manager and what already exists. For an audit, report
   a checklist of present / missing / deviating items and agree the plan before changing anything;
   follow `references/common.md` › *Adopting the baseline in an existing repository*.
2. **Discuss** the design and choices with the user before implementing (alternatives + recommendation).
3. **Scaffold** using the language reference:
   - C#/.NET → `references/csharp.md` + proven templates in `templates/csharp/`.
   - TypeScript/Node → `references/typescript.md`.
   - Other languages → apply `references/common.md` with that language's official conventions.
4. **Verify locally**: run the full local gate (pre-push hook), build the container and smoke-test it.
5. **Document**: README, `docs/decisions/` (`adr` skill), repo `CLAUDE.md` and versioned
   `.claude/settings.json`, per `references/common.md` › *Repository docs and Claude settings*.
6. **Commit** as the user. Push / open PRs per the repo's push policy (ask when it has none);
   change GitHub settings only with explicit confirmation.

## Adapting templates
Templates come from a real, CI-verified repo (HackerNews.BestStories.Api). Re-check latest
versions of packages, actions and images (NuGet API, `gh api repos/<owner>/<action>/releases/latest`)
instead of copying versions blindly. Always read `references/common.md` for the cross-language
pieces and known pitfalls.

Replace every example-specific value (`grep -rni "hackernews\|best-\?stories" .` must come back
empty afterwards):
- `HackerNews.BestStories.Api` — project, assembly, folder and test-project names (`Directory.Build.props`
  `ConfigureGitHooks` condition, `Dockerfile`, `.github/path-filters.yml`, workflows, compose).
- `hackernews-beststories` — image tag (`ci.yml`) and compose project name.
- `hackernews-stub` + `hackernews-stub/mappings/` — the stubbed dependency and its WireMock mappings.
- `HackerNews__*` environment variables, `ENDPOINT` (`/api/stories/best`), `REQUESTS_PER_REFRESH`
  and the `hackernews_upstream_requests` metric in the k6 script.
- SLO numbers (k6 `SLO` object, `RATE` defaults) and the required check names in
  `.github/rulesets/main.json` (must match the job `name:`s).
- `README.md`, `CLAUDE.md` and `docs/decisions/README.md` are skeletons: fill in every `<...>`.
