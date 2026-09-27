# Claude Code personal configuration

Versioned subset of `~/.claude` (the repo lives in place so Claude Code loads it directly):

- `CLAUDE.md` – personal engineering baseline applied to every repository.
- `skills/quality-baseline/` – skill to set up or audit a repo against that baseline, with
  language references (C#, TypeScript, common) and CI-verified C# templates.

Everything else in `~/.claude` (history, sessions, caches, settings) is ignored on purpose.

## New machine

```bash
git clone https://github.com/alvaromongon/claude-config.git /tmp/claude-config
cp -R /tmp/claude-config/. ~/.claude/
```
