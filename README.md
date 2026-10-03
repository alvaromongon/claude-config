# Claude Code personal configuration

Versioned subset of `~/.claude` (the repo lives in place so Claude Code loads it directly):

- `CLAUDE.md` – personal engineering baseline applied to every repository.
- `skills/quality-baseline/` – skill to set up or audit a repo against that baseline, with
  language references (C#, TypeScript, common) and CI-verified C# templates.
- `skills/adr/` – skill to write, propose, supersede or list Architecture Decision Records.
- `skills/github-workflow-setup/` – skill to set up or audit a repo's GitHub issue workflow
  (labels, per-issue autonomy, workflow doc) used by the `github-*` skills (see ADR 0001).
- `docs/decisions/` – decision log for this repository, written with the `adr` skill.
- `docs/credits.md` – attribution for prior art the GitHub workflow skills are modeled on.

Everything else in `~/.claude` (history, sessions, caches, settings) is ignored on purpose.

## New machine

```bash
git clone https://github.com/alvaromongon/claude-config.git /tmp/claude-config
cp -R /tmp/claude-config/. ~/.claude/
```
