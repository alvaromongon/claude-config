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

Claude Code applies these to subagents too: anything left in `ask` blocks an unattended run.
Merge into the existing `permissions` (never drop entries the repo already has):

```json
"allow": [
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
  "Bash(gh api repos/*/dependencies/blocked_by)"
],
"ask": [
  "Bash(git push:*)"
]
```

Keep the generic `git push` in `ask`: only `issue-*` branches are pre-approved. Leave a generic
`gh api` out of `allow` — it can do anything the token can.

## 3. `docs/agents/workflow.md` — the switch the work queue reads

`Unattended merge: yes` (default) lets `github-work-queue` merge once reviews and CI are green;
`no` makes it stop at "ready for your review" and move on. The per-issue consent is the
`ready-for-agent` label itself.

## Safety net that stays in GitHub

The default-branch ruleset (required checks, linear history, no force-push) still applies to agent
merges — the policy above never bypasses it. Without a ruleset (private repo on a free plan), say
so during setup: green CI is then enforced only by the work queue's own check.
