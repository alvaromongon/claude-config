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

1. **Detect**: `gh label list` for existing labels, and whether `docs/agents/workflow.md` already
   exists. For an audit, report present / missing / deviating items (labels, doc, any `CLAUDE.md`
   override) and agree the plan before changing anything.
2. **Labels**: create any missing label from `references/labels.md` with
   `gh label create <name> --color <hex> --description "<description>"`. Never delete or repurpose
   a label that has open issues on it without checking with the user first.
3. **Workflow doc**: copy `templates/workflow.md` to `docs/agents/workflow.md` in the target repo,
   filling in the escalation triggers and overrides for that repo (ask the user for anything
   repo-specific: sensitive areas, retry count, etc.). Link it from the repo's `CLAUDE.md`.
4. **Reminder mode**: if labels and doc already exist and nothing needs changing, just summarize
   the cycle from `docs/agents/workflow.md` back to the user instead of editing anything.
5. **Commit** as the user. Push / change GitHub repo settings only with explicit confirmation —
   this is the default baseline rule unless the repo's own `CLAUDE.md` relaxes it.

## Reference

- `references/labels.md` — the labels this workflow needs and what creates/consumes them.
- `references/dependencies.md` — how blocking edges are written and checked (shared by the
  `github-*` skills).
- `templates/workflow.md` — the per-repo doc this skill writes to `docs/agents/workflow.md`.
