---
name: github-implement
description: Implement one ready-for-agent GitHub issue end to end with TDD — branch, red-green-refactor at the brief's acceptance criteria, local quality gate, push, open PR. Run as an isolated subagent per ticket, one ticket per invocation. Use when a single issue needs implementing, or when github-work-queue dispatches one ticket from the backlog.
context: fork
---

# GitHub implement

Executes a single `ready-for-agent` issue's brief, end to end, with TDD. No re-planning: the
brief already settled scope — this skill implements it, it doesn't re-interview or propose a
different approach. One ticket per invocation, context cleared between tickets, so the next
ticket starts clean.

Modeled on `implement` from [mattpocock/skills](https://github.com/mattpocock/skills) — see
`docs/credits.md`.

## Preconditions

- Target issue: `$ARGUMENTS` (number or URL). This skill runs in a forked context and does not see
  the caller's conversation: if no issue was passed, stop and report that instead of guessing.
- The issue carries `ready-for-agent`. If not, or if any issue it's blocked by is still open
  (check per `../github-workflow-setup/references/dependencies.md`), stop and say so instead of
  proceeding.
- Read the brief (`../github-triage/references/brief-format.md` format) from the issue body/
  comments. If it's missing acceptance criteria, stop — that's a triage/refine gap, not something
  to guess around here.

## Procedure

1. **Branch**: per `references/delivery.md`.
2. **TDD**: for each acceptance criterion, red (failing test) → green (minimal code to pass) →
   refactor, per this repo's testing conventions (`~/.claude/CLAUDE.md` baseline, `quality-
   baseline` skill). Unit/component tests as appropriate; never production code ahead of a
   failing test for it.
3. **Local gate**: run the repo's full local quality gate (the same checks as its pre-push hook —
   format, build, tests, coverage) before considering the ticket done.
4. **Commit, push, open PR**: per `references/delivery.md` (push only if the repo's push policy
   allows it). Does not merge, does not self-review.
5. **Report back**: branch name, PR link, which acceptance criteria are covered by which test,
   and anything intentionally left out of scope per the brief.

Stop and escalate instead of continuing on any condition in `references/delivery.md`'s stop list.

## Reference

- `references/delivery.md` — branch/commit/PR conventions and escalation stop conditions.
