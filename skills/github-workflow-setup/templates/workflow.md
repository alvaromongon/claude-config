<!--
Template for docs/agents/workflow.md in the child repo. Replace bracketed notes; drop anything
that doesn't apply (e.g. no work queue if the repo is fully supervised). Keep it short — this is a
map of the cycle, not a copy of the skills themselves.
-->

# Agent workflow

This repo uses the GitHub-native workflow from `~/.claude/skills/github-*`
(design: [ADR 0001](https://github.com/alvaromongon/claude-config/blob/main/docs/decisions/0001-github-driven-triage-refinement-and-autonomous-implementation.md)
in `claude-config`). Milestones are specs/epics; issues are tracer-bullet tickets; blocking
dependencies are GitHub's native issue-blocking relations.

## Cycle

1. **Triage** (`github-triage`) — incoming issues start `needs-triage`. Classified into
   `needs-info`, `ready-for-agent`, `ready-for-human`, or closed `wontfix`.
2. **Refine** (`github-refine`) — a spec or milestone is broken into tracer-bullet issues with
   blocking edges, each ending up `ready-for-agent` or `ready-for-human`.
3. **Implement** (`github-implement`) — one `ready-for-agent` issue at a time, TDD, in an
   isolated subagent.
4. **Review** — a separate subagent reviews the diff/PR (reusing `code-review`, fresh context,
   report-only) before merge.
5. **Work queue** (`github-work-queue`) — orchestrates steps 3-4 sequentially over the
   `ready-for-agent` backlog, escalating to a human when a ticket needs it (see below).

## Autonomy

Per-issue, via labels — not a repo-wide switch:
- `ready-for-agent`: the agent may implement it without asking after every step.
- `ready-for-human`: needs supervision; the work queue skips it.

## Escalation triggers

The work queue stops and asks instead of continuing when:
- tests don't stabilize after [N, default 3] attempts,
- acceptance criteria turn out ambiguous mid-implementation,
- the change touches a sensitive area: [list for this repo, e.g. auth, payments, infra, CI],
- the issue lacks the `ready-for-agent` label.

## Overrides for this repo

[State here anything that differs from the defaults above: a different N, extra sensitive areas,
a tracker other than GitHub for parts of the flow, etc. Leave "None" if there are no overrides.]
