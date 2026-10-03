---
name: github-work-queue
description: Sequentially work through the ready-for-agent backlog without asking for approval between tickets — implement, independently review for correctness and security, wait for CI, merge or hand off, then move to the next. Use when the user wants the agent to process a batch of ready issues autonomously instead of being invoked ticket by ticket.
---

# GitHub work queue

Orchestrates `github-implement` and an independent review over the `ready-for-agent` backlog,
one ticket at a time, per `references/queue-policy.md`. This is what turns "invoke the agent per
ticket and review every step" into "hand it a backlog and get a report back."

Modeled on the orchestration role of `implement-spec` from
[mattpocock/skills](https://github.com/mattpocock/skills) — see `docs/credits.md`. Unlike it,
this version is **sequential**, not parallel across worktrees — see ADR 0001's deferred work.

## Requires

The `Agent` tool, to spawn an implementer subagent and a separate reviewer subagent per ticket —
this skill is not just instructions read in the main session, it actively dispatches subagents.

## Procedure

Follow `references/queue-policy.md`: build the queue and its frontier, then per ticket —
implement (subagent) → independent review, correctness and security in parallel (two separate
subagents, report-only) → one fix retry if needed → wait for CI → merge or hand off → recompute
the frontier → continue. Escalate a single ticket without stalling the rest of the queue. Report
a summary at the end.

## Reference

- `references/queue-policy.md` — frontier computation, the per-ticket loop, escalation, and the
  end-of-run report.
