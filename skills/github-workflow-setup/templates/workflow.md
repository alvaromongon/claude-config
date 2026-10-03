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
   `needs-info`, `ready-for-agent`, `ready-for-human`, or closed `wontfix`. External PRs are
   reviewed as text and never checked out or run on the host.
2. **Refine** (`github-refine`) — a spec or milestone is broken into tracer-bullet issues with
   blocking edges (GitHub's native issue dependencies), each ending up `ready-for-agent` or
   `ready-for-human`.
3. **Implement** (`github-implement`) — one `ready-for-agent` issue at a time, TDD, in an
   isolated subagent; ends with a pushed branch and an open PR.
4. **Review** — two separate subagents review the PR's branch in parallel, each in its own git
   worktree, report-only: `code-review` (correctness) and `security-review` (security). One fix
   round if either finds blocking issues.
5. **Work queue** (`github-work-queue`) — orchestrates steps 3-4 sequentially over the
   `ready-for-agent` backlog, waits for CI, merges, and escalates individual tickets to a human
   when needed (see below) without stopping the rest of the queue.

## Autonomy

Per-issue, via labels — not a repo-wide switch:
- `ready-for-agent`: the agent may implement it without asking after every step.
- `ready-for-human`: needs supervision; the work queue skips it.

## Escalation triggers

The work queue stops working on a ticket — leaves its branch/PR as-is, relabels it
`ready-for-human` with a comment explaining why — and moves on to the next one when:
- tests don't stabilize after [N, default 3] attempts,
- acceptance criteria turn out ambiguous mid-implementation,
- the change touches a sensitive area: [list for this repo, e.g. auth, payments, infra, CI],
- the issue lacks the `ready-for-agent` label or still has an open blocker,
- the review fix round didn't produce a clean review.

## Overrides for this repo

[State here anything that differs from the defaults above: a different N, extra sensitive areas,
a tracker other than GitHub for parts of the flow, etc. Leave "None" if there are no overrides.]
