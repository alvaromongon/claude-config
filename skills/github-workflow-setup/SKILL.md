---
name: github-workflow-setup
description: Set up or audit a repository's GitHub-native issue workflow (triage/autonomy labels, docs/agents/workflow.md, per-issue autonomy via labels) that github-triage, github-refine, github-implement and github-work-queue rely on. Use when configuring a new repo for this workflow, auditing an existing one, or when you want a reminder of how the cycle works in this repo.
---

# GitHub workflow setup

Set up (new repo) or audit (existing repo) the GitHub issue workflow defined in
[ADR 0001](../../docs/decisions/0001-github-driven-triage-refinement-and-autonomous-implementation.md).
Also works as an on-demand reminder: re-run it just to see the current state and the cycle
explained, without changing anything.

Modeled on `setup-matt-pocock-skills` from [mattpocock/skills](https://github.com/mattpocock/skills)
— see `docs/credits.md`. Unlike it, this skill assumes GitHub as the tracker and does not support
alternative trackers.

## Procedure

1. **Detect**: `gh label list` for existing labels; whether `docs/agents/workflow.md`,
   `.github/ISSUE_TEMPLATE/` and `.github/workflows/needs-info-reply.yml` exist; the push/merge
   policy in the repo's `CLAUDE.md` and `.claude/settings.json`; and whether a default-branch
   ruleset exists (`gh api repos/{owner}/{repo}/rulesets`). For an audit, report present /
   missing / deviating items and agree the plan before changing anything.
2. **Labels**: create any missing label from `references/labels.md` with
   `gh label create <name> --color <hex> --description "<description>"`. Never delete or repurpose
   a label that has open issues on it without checking with the user first.
3. **Workflow doc**: copy `templates/workflow.md` to `docs/agents/workflow.md` in the target repo,
   filling in the escalation triggers, `Unattended merge` and overrides for that repo (ask the
   user for anything repo-specific: sensitive areas, retry count, etc.). Link it from the repo's
   `CLAUDE.md`.
4. **Autonomy**: ask the user whether agents may push and merge in this repo, then write the
   matching policy in `CLAUDE.md`, `.claude/settings.json` and `workflow.md` per
   `references/autonomy.md`. Never widen permissions without that explicit answer.
5. **Intake**: copy `templates/ISSUE_TEMPLATE/` to `.github/ISSUE_TEMPLATE/` (issue forms that
   apply `needs-triage`) and `templates/workflows/needs-info-reply.yml` to `.github/workflows/`
   (sends a reporter's reply on a `needs-info` issue back to `needs-triage`).
6. **Existing backlog** (repo with open issues): list open issues carrying none of the state
   labels (`gh issue list --state open --json number,title,author,labels`) and propose, in one
   table for approval, `needs-triage` for external reports and `github-refine`/a brief for the
   owner's own issues. Nothing is relabeled in bulk without that approval; closed issues are left
   alone.
7. **Reminder mode**: if everything already exists and nothing needs changing, just summarize
   the cycle from `docs/agents/workflow.md` back to the user instead of editing anything.
8. **Commit** as the user. Push per the repo's push policy (ask when it has none); change GitHub
   repo settings (labels, rulesets) only with explicit confirmation.

Existing files (`CLAUDE.md`, `.claude/settings.json`, issue templates, labels) are merged into,
never overwritten: keep what the repo already has and add only what's missing, showing the diff.

## Reference

- `references/labels.md` — the labels this workflow needs and what creates/consumes them.
- `references/dependencies.md` — how blocking edges are written and checked (shared by the
  `github-*` skills).
- `references/autonomy.md` — the push/merge policy and the permissions that enforce it.
- `templates/workflow.md` — the per-repo doc this skill writes to `docs/agents/workflow.md`.
- `templates/ISSUE_TEMPLATE/`, `templates/workflows/needs-info-reply.yml` — issue intake.
