# Claude Code personal configuration

Versioned subset of `~/.claude` (the repo lives in place so Claude Code loads it directly):

- `CLAUDE.md` – personal engineering baseline applied to every repository.
- `skills/quality-baseline/` – skill to set up or audit a repo against that baseline, with
  language references (C#, TypeScript, common) and CI-verified C# templates.
- `skills/adr/` – skill to write, propose, supersede or list Architecture Decision Records.
- `skills/github-workflow-setup/` – skill to set up or audit a repo's GitHub issue workflow
  (labels, per-issue autonomy, workflow doc) used by the `github-*` skills (see ADR 0001).
- `skills/github-triage/` – skill to classify incoming external GitHub issues and route them to
  `needs-info` / `ready-for-agent` / `ready-for-human` / closed `wontfix`.
- `skills/github-refine/` – skill to turn an agreed spec into a GitHub milestone of tracer-bullet
  issues with blocking dependencies.
- `skills/github-implement/` – skill to implement one ready-for-agent issue end to end with TDD,
  as an isolated subagent per ticket.
- `skills/github-work-queue/` – skill to sequentially work through the ready-for-agent backlog
  (implement, independently review, merge or hand off) without per-ticket approval.
- `skills/check-upstream-skills/` – on-demand skill to review mattpocock/skills for improvements
  applicable to the `github-*` skills.
- `docs/decisions/` – decision log for this repository, written with the `adr` skill.
- `docs/credits.md` – attribution for prior art the GitHub workflow skills are modeled on.
- `docs/upstream-watch.md` – marker of how far `check-upstream-skills` has reviewed upstream.

Everything else in `~/.claude` (history, sessions, caches, settings) is ignored on purpose.

## New machine

```bash
git clone https://github.com/alvaromongon/claude-config.git /tmp/claude-config
cp -R /tmp/claude-config/. ~/.claude/
```
