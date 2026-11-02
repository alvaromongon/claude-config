---
status: Accepted
date: 2026-11-02
decision-makers: Alvaro Montero
consulted: "N/A"
---

# 0008. Run the work-queue orchestrator as a foreground Sonnet subagent

- **Builds on**: [0003](0003-assign-models-per-skill-by-role.md) — assigns each skill a model by role, with the work queue's orchestrator on Sonnet. This ADR changes how that assignment is enforced, not the assignment.

**Decision**: the work queue's main session only launches one foreground subagent on Sonnet, which orchestrates the whole queue, so the orchestrator stays on Sonnet whatever model the session was started on.

## Context and problem statement

The work queue is a skill that orchestrates one subagent per task. A skill's `model:` setting covers only the turn it is invoked in; a background subagent finishing starts a new turn, and that turn runs on the session model. So a session started on Opus orchestrates on Opus after its first subagent returns.

**Why it matters**: the orchestrator on Opus was 38% of the estimated cost of four queue runs on a real repository ($103.73 of $273.79, measured from transcripts at list prices, 2026-10-17 to 2026-10-26; session went back to Opus in 3 of the 4 runs). Sonnet costs half of Opus, so the expected effect is about −19% cost per merged PR, $8.83 to about $7.15 (estimated: same tokens at half the price).

## Decision drivers

- The saving must not depend on the person launching the queue remembering an option; a forgotten option fails silently.
- The review gate before an unattended merge must not get weaker.
- The queue is unattended: it needs no human input between tickets.

## Considered options

- A. Do nothing: leave the skill's `model:` setting alone.
- B. Run the skill in a forked context (`context: fork`).
- C. Require the session to start on Sonnet, with the skill saying so before its first ticket.
- D. The main session launches one foreground Sonnet subagent that orchestrates; every subagent it launches is foreground too.

## Decision outcome

Chosen option: "D", because it is the only option measured to hold without depending on the launch.

**What we give up**: an extra level of nesting, the ticket-by-ticket progress in the main session, and the chance to steer mid-run. The simple option, C, held when followed but relied on the launcher, and nothing could enforce it.

**Scope**: every work-queue run in every repository; nobody needs to change how they launch it.

**Confidence**: medium. Measured over two short sandbox runs only. Revisit if a long queue degrades inside a subagent, if a security review misses a real defect, or if Claude Code changes the nesting limits or how a skill's model applies.

### Consequences

- Good: the session model no longer matters to the queue's cost.
- Good: the main session uses almost nothing: about $0.07 per run (estimated, list prices, 2 runs).
- Bad: the orchestrator can't ask the owner anything; decisions wait for the end-of-run report.
- Bad: the work runs one level deeper, down to level 3, so a lower nesting limit would break it.
- Bad: at that depth security reviewers skipped their sub-tasks unless told otherwise, so the requirement has to stay explicit in the queue's rules.
- Bad: not shown yet that a security review at this depth catches a real vulnerability, nor how a long queue behaves.

### Confirmation

A behavioural scenario of the work queue checks that a run launched from a session on Opus makes no main-session call on Opus, reading the model of each call from the transcripts. It names this ADR.

**Success measure**: the orchestrator's Opus share of the estimated cost ≈ 0 and cost per merged PR near $7.15 (estimated target), read from the session transcripts once at least 10 PRs have merged in a real repository, with owner messages per PR, review rounds and escaped defects unchanged.

## Pros and cons of the options

### A. Do nothing

- Good: no change.
- Bad: measured in the sandbox, one ticket: 5 main-session calls on Sonnet, then 7 on Opus from the first subagent's notification.

### B. Forked context

- Bad: measured in the sandbox, one run: 47 of 47 main-session calls on Opus. The fork launched a background subagent and returned, and the main session carried on orchestrating on its own model.

### C. Session started on Sonnet

- Good: simple. Measured in the sandbox, one ticket: 11 of 11 main-session calls on Sonnet.
- Bad: depends on the launcher, and a miss is silent.

### D. Foreground Sonnet subagent

- Good: measured in the sandbox, launched from Opus, 2 runs and 7 tickets: main session 4 of 4 calls on Sonnet, orchestrator 39 of 39, reviewers on Opus and still parallel, no nesting refusals.
- Bad: see *Consequences*.

## More information

Foreground matters: a background subagent ends the orchestrator's turn and hands the queue back to the main session, which is what made option B fail. Measured on Claude Code 2.1.289 for options A to C; orchestration cost in option D was about $0.11 to $0.12 per ticket (estimated, list prices), against $0.50 and $0.16 per ticket in options A and C, on different tickets, so indicative only.

No doubt review ran: the change is one skill's text and is reverted by restoring it.
