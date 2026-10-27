# Maintaining this repository

## Changing this repository

- **Conventions**: skills in English, one folder each, `SKILL.md` kept short with detail in
  `references/`. Architecturally significant changes get an ADR (`adr` skill).
- **Checks**: `python3 .github/scripts/validate.py` (skill frontmatter, relative links, YAML/JSON,
  efficiency blocks in sync with [`efficiency.csv`](efficiency.csv)), `shellcheck` on template scripts and `python3 -m unittest discover -s skills/session-metrics/tests`
  — the same as the [Docs workflow](../.github/workflows/docs.yml).
- **Behaviour**: before a significant edit to a workflow skill, walk through its
  `evals/scenarios.md` and confirm each expected behaviour still holds.
- **Efficiency**: after a configuration change has run for at least 10 merged PRs in a public
  repo, record its window and re-render the pages — [method](efficiency.md#method).
- **Upstream and models**: `/check-upstream-skills` now and then — it also checks the model
  assignment against [model-watch.md](model-watch.md); credits in [credits.md](credits.md).

## Overrides of the baseline

This repo holds documentation and templates, not an application, so:

| Baseline item | Here | Why |
|---|---|---|
| Unit/component/load tests, SLO, coverage | Behavioural scenarios (`evals/`) | Skills are prose; templates are verified in the repos they come from. |
| Build, CodeQL, Docker | Docs CI (frontmatter, links, YAML/JSON, shellcheck) | No executable product. |
| One PR per step, review via PR | Direct commits to `main` by the owner (ruleset bypass); PRs for everyone else | Single maintainer, nothing for PR CI to gate beyond the docs checks. |
| Flow document (`docs/flows.md`) | [How the GitHub workflow works](workflow.md) | The repo's only "flow" is the workflow cycle, already described there. |
| Pre-push hook | Run the checks above manually | A hook needs `core.hooksPath` in `.git/config`, which isn't versioned. |
| Push policy | Ask before every push | Default from [ADR 0002](decisions/0002-per-repository-push-and-merge-policy.md). |

## Repository protection

The repo is public; the versioned files contain no personal data beyond my name and GitHub
username, and commits use the GitHub noreply email. `main` is protected by the ruleset in
`.github/rulesets/main.json` (applied with
`gh api -X POST repos/{owner}/{repo}/rulesets --input .github/rulesets/main.json`): no deletion or
force-push; everyone else goes through a PR with the docs check green, while the repo admin
bypasses it to commit directly. Secret scanning with push protection is enabled.

## Next steps

Open work on this repository, in order. Remove an item when it lands; the reasoning lives in the
linked ADR.

1. **Measure [ADR 0004](decisions/0004-three-layer-baseline-decisions-shaping-implementation.md)**:
   its success measure is that the next three milestones start from a `spec` issue naming a
   success metric (baseline 0 on 2026-10-14). Close each spec with `github-shape`'s close-out and
   record the count here; if most work needed no shaping, revisit the ADR (option C).
2. **Widen `check-upstream-skills`** to watch [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
   and the pstack port [michael-denyer/pstack-claude](https://github.com/michael-denyer/pstack-claude)
   besides mattpocock/skills, with a marker per source in `docs/upstream-watch.md` (ADR 0004).
3. **After a couple of milestones on the new flow**: a `retro` skill that turns mechanical lessons
   into checks rather than instructions, and review flags for a lowered bar — thresholds edited
   down, skipped or deleted tests, new suppressions (ADR 0004, implementation layer).
