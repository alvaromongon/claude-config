# Autonomy: push and merge policy

The personal baseline has no global push rule: each repo decides what agents may push or merge
without asking (ADR 0002). A repo with no policy means "ask before every push", which stops
`github-implement` at a local commit and makes `github-work-queue` unusable there. This skill
writes the policy, after asking the user, in three places that must agree.

## 1. Repo `CLAUDE.md` — the rule, in words

```markdown
## Push and merge policy
Agents may push `issue-*` branches, open PRs, and merge PRs of `ready-for-agent` issues once both
reviews and CI are green (see docs/agents/workflow.md). Ask before any other push.
```

For a supervised repo, write "Ask before every `git push`." instead and set `Unattended merge: no`.

## 2. Repo `.claude/settings.json` — the enforcement

Claude Code applies these to subagents too: anything not in `allow` is prompted for, which an
unattended run can't answer. Merge into the existing `permissions` (never drop entries the repo
already has), replacing `main` with the repo's default branch:

```json
"allow": [
  "Read(~/.claude/skills/**)",
  "Bash(git worktree remove --force .claude/worktrees/*)",
  "Bash(git branch -D worktree-agent-*)",
  "Bash(git checkout -b issue-*)",
  "Bash(git checkout main)",
  "Bash(git pull:*)",
  "Bash(git add:*)",
  "Bash(git commit:*)",
  "Bash(git push -u origin issue-*)",
  "Bash(git push origin issue-*)",
  "Bash(gh issue view:*)",
  "Bash(gh issue list:*)",
  "Bash(gh issue edit:*)",
  "Bash(gh issue comment:*)",
  "Bash(gh pr create:*)",
  "Bash(gh pr view:*)",
  "Bash(gh pr diff:*)",
  "Bash(gh pr checks:*)",
  "Bash(gh pr checkout:*)",
  "Bash(gh pr merge:*)",
  "Bash(gh api repos/*/dependencies/blocked_by --jq *)"
],
"deny": [
  "Bash(git push*--force*)",
  "Bash(git push*-f *)",
  "Bash(git push*+*)",
  "Bash(git push*:main*)",
  "Bash(git push*:refs/*)",
  "Bash(git push*--delete*)",
  "Bash(git push*-d *)",
  "Bash(git push*--mirror*)",
  "Bash(git push*--all*)"
]
```

Verified against Claude Code (see `../evals/scenarios.md`):

- **No `ask` rule for `git push`**: `ask` wins over `allow`, so a generic `Bash(git push:*)` in
  `ask` blocks the `issue-*` pushes too. Other pushes stay unapproved because nothing allows them.
- **`deny` closes the gaps of the `issue-*` wildcard**, which would otherwise also match
  `git push origin issue-1:main` or `--force`. Write deny patterns without a final `:*` — Claude
  Code reads a trailing `:*` as the legacy prefix syntax, so `git push*:*` matches nothing.
- **The dependency check keeps its `--jq` suffix** in the pattern; the command is never run bare.
- **Skill files live outside the repo**: without `Read(~/.claude/skills/**)` the work queue can't
  read its own `references/`.
- **Review worktrees** need the cleanup rules above, and `.claude/worktrees/` in `.gitignore`.
- Leave a generic `gh api` out of `allow` — it can do anything the token can.
- **Trust the workspace**: Claude Code ignores a project's `allow` rules until the folder has
  been trusted once (run `claude` there interactively and accept the dialog). Say so at the end of
  setup.
- An unattended run (e.g. `claude -p "/github-work-queue"`) also needs file edits approved: use
  `--permission-mode acceptEdits` (or auto mode in an interactive session).

## 3. `docs/agents/workflow.md` — the switch the work queue reads

`Unattended merge: yes` (default) lets `github-work-queue` merge once reviews and CI are green;
`no` makes it stop at "ready for your review" and move on. The per-issue consent is the
`ready-for-agent` label itself.

## Safety net that stays in GitHub

The default-branch ruleset (required checks, linear history, no force-push) still applies to agent
merges — the policy above never bypasses it. Without a ruleset (private repo on a free plan), say
so during setup: green CI is then enforced only by the work queue's own check.
