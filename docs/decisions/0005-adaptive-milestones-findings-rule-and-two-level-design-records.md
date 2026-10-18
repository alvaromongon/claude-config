---
status: Proposed
date: 2026-10-18
decision-makers: Alvaro Montero
consulted: "N/A"
---

# 0005. Adaptive milestones: a findings rule, a post-merge checkpoint and two-level design records

- **Issue**: N/A (design conversation on 2026-10-18, after the first milestone run in `finance-agent`)
- **Supersedes**: N/A (extends [0001](0001-github-driven-triage-refinement-and-autonomous-implementation.md)
  and [0004](0004-three-layer-baseline-decisions-shaping-implementation.md))

**Decision**: a milestone adapts while it runs. Every finding gets a destination inside the
milestone or an explicit discard, a checkpoint after each merge refines the next slices and reroutes
findings, the milestone escalates to the owner once discovered work passes 50 % of its original
size, and design records split in two: architecture ADRs, accepted when the milestone closes, and
a living flow document per repo, which together with the code is the source of truth. Target: 0
findings without a destination at the end of each milestone (baseline 20, measured).

## Context and problem statement

The workflow from [0001](0001-github-driven-triage-refinement-and-autonomous-implementation.md)
and [0004](0004-three-layer-baseline-decisions-shaping-implementation.md) is a forward pipeline:
shape → refine the whole milestone at once → implement each ticket without re-planning → close out.
Specs are a best effort and implementation always deviates from them; the pipeline's only response
to a deviation is to escalate one ticket. What is learned in ticket N never reaches tickets N+1…M,
findings outside a ticket's scope have no home, and nothing interleaves tidying, debt or rethinking
with features. Kent Beck's point applies: shipping feature after feature against a fixed plan is a
waterfall that ends in a big ball of mud.

The ADRs suffer the same rigidity. The `adr` skill makes an ADR immutable once accepted, and ADRs
are accepted early and written at code level, so a spec that pivots forces new superseding ADRs.

**Why it matters**: the first milestone run on the full flow (`finance-agent`, milestone
"Self-service setup", spec #14) shows it. All figures below are measured from that session's
transcript and the repo on 2026-10-18:

- The queue ran 5 agent tickets: 4 merged after one fix round each, 1 (#19, PR #26) escalated. A
  documentation ticket's reviewer found a flaw in the core engine's data model (one entry per
  exit), which became a new spec (#27) and decision (#28), and left #19 and #20 paused.
- 20 findings had no destination: 11 in the queue's end-of-run report and 9 non-blocking findings
  in the re-review of PR #26. The owner did not know whether to update the milestone, edit issues
  or open new ones.
- Routing them by the rule below adds 7 tickets to a 6-ticket milestone (+117 %), so the
  milestone was not close to done.
- 3 of the repo's 14 ADRs (21 %), all accepted on 2026-10-15, already need revision three days
  later (0005 SMTP, 0006 log format, 0007 portfolio lots). Judging by their titles, about half
  record code-level rules (tick age, ATR stops, setup detectors), not architecture (estimated).
- One re-review subagent cost 101,302 tokens and 204 s (one run). The implementation is about 90 %
  agent-written, so the cost of adapting is mostly tokens, not human time.

## Decision drivers

- Specs and designs change during a milestone; the process must absorb change instead of
  escalating every deviation.
- Each milestone is self-contained: nothing it finds is left pending in a backlog that may never
  be done.
- Human steps stay where judgment is needed: scope, contracts, architecture. Everything inside the
  spec's bounds is decided by the agent and recorded.
- Cost is tokens: an extra step must run only when it has something to work on, on the cheapest
  model that fits its role ([0003](0003-assign-models-per-skill-by-role.md)), and must not repeat
  work another step already did.
- One source of truth per kind of knowledge: the *why* that survives code changes, and the *how*
  that changes with the code.

## Considered options

- A. **Do nothing**: keep the forward pipeline; findings go into end-of-run reports.
- B. **Heavier up-front specs**: more shaping and design review before refining, to prevent
  deviations.
- C. **A cooldown between milestones** (Shape Up): findings, bugs and chores collect in a batch
  worked between milestones.
- D. **Adaptive milestone**: a findings rule, just-in-time refinement with a post-merge checkpoint,
  a growth cap, and two-level design records.

## Decision outcome

Chosen option: "D", because it is the only one where what a ticket learns reaches the remaining
tickets while the context is fresh, and it keeps each milestone self-contained. B fights the
premise that specs deviate; C leaves findings pending outside the milestone that produced them.

### 1. Findings rule

A finding is anything learned during a milestone that the current ticket doesn't cover: a
reviewer's non-blocking item, an inconsistency the implementer saw outside its scope, a gap in a
spec. The first rule that matches wins:

| # | The finding… | Destination | Decided by |
|---|---|---|---|
| R1 | changes the spec's what or why (metric, *not doing*, a public contract) or an architecture ADR | A `decision` issue blocking the spec, or a new spec via `github-shape` | Owner |
| R2 | affects an open ticket not yet implemented, or one that will be redone | Edit that ticket's brief (new acceptance criterion) and comment why | Agent |
| R3 | is a defect in work delivered in this milestone | New ticket in the same milestone | Agent; `ready-for-human` if it touches a sensitive area |
| R4 | is debt, tidying or a chore, even outside the spec's scope | New ticket in the same milestone | Same as R3 |
| R5 | isn't worth its cost | Discarded, with the reason, in the report | Owner confirms |

- **Invariant**: every finding lands in R1–R4 or is discarded under R5. The milestone closes only
  when none of its tickets is open.
- **Never**: edit closed issues, reopen merged PRs or rewrite the milestone; the milestone only
  gains tickets.
- **Retro input**: a finding that shows a gap in the process (something the baseline, a review or
  refinement should have caught) is also tagged for the retro, whose output are checks and rules
  in this repository.

### 2. Growth cap

When the tickets added under R3 and R4 exceed **50 %** of the milestone's original ticket count,
the next finding is treated as R1: the owner decides whether to accept the growth and update the
appetite, split the rest into a new spec, or cut. The threshold is an estimate, with no data
behind it yet; measure it over the next three milestones.

### 3. Just-in-time refinement and post-merge checkpoint

- `github-refine` publishes every slice of the milestone with its title, demoable outcome and
  blockers, so the plan is decided, but writes the full brief and the `ready-*` label only for
  the frontier (1–2 slices).
- `github-implement` adds a *Learned* section to the PR body with the findings it saw, and does
  not fix them outside its scope. Small preparatory tidyings for its own change may go in the same
  PR as separate commits (Beck's *Tidy First*).
- After each merge, the work queue runs a **checkpoint** when the PR's *Learned* section or its
  reviews hold findings, or when the frontier has no briefed ticket left: it applies the findings
  rule and writes the briefs of the next slices. The agent decides alone while the change stays
  inside the spec's metric, *not doing* and appetite (growth cap), touches no sensitive area and
  changes no architecture ADR; otherwise it escalates under R1.
- **The checkpoint runs on `sonnet` and does not review code again.** Its input is limited to the
  findings already produced (the two reviewers' reports and the implementer's *Learned* section),
  the spec and the outlines of the pending slices; it never reads the diff or explores the
  codebase, which is the reviewers' job and the expensive part. Both of its tasks follow rules:
  routing with the R1–R5 table, and filling the brief format for a slice whose title, outcome and
  blockers refinement already fixed ([0003](0003-assign-models-per-skill-by-role.md)'s
  rule-following role). When in doubt it classifies a finding as R1, so a wrong call costs the
  owner a question, not a bad design merged unseen.
- **Escalation to `opus` on a pivot**: when the checkpoint finds that a pending slice's outline no
  longer fits (what was learned changes its outcome, its blockers or the order of the slices), it
  does not rewrite it. It hands the remaining outlines to `github-refine` (`opus`, effort high),
  or to the owner under R1 when the spec's bounds move.
- The per-PR reviewers stay on `opus` with their full scope, including `security-review` on
  documentation-only PRs: the most valuable finding of the first milestone (entries stranded by
  the quarterly archive, giving a wrong R) came from the security re-review of a documentation PR
  (#26 in `finance-agent`). The savings come from the checkpoint, not from the review gate.
- The spec's close-out reads the checkpoints' records instead of reviewing the milestone's code
  again.
- Refinement orders slices so the success metric becomes measurable as early as possible (a check
  written first and failing, like spec #27's four tests). When the metric can only be measured at
  the end (spec #14's dogfood), the spec says so and the riskiest assumption goes first; the
  checkpoint then judges whether the target is still reachable, without measuring it.

### 4. Two-level design records

- **ADRs record architecture only**: decisions that are hard to reverse, surprising without
  context, a real trade-off **and** expected to survive changes to the spec and the code
  (structure, deployment, state, contracts, non-functional requirements).
- **Lifecycle**: an ADR written during a milestone stays `Proposed` and editable while the
  milestone is open, and is accepted at the spec's close-out, once the data is in. From then on it
  is immutable, as today.
- **Design detail lives elsewhere**: during the milestone, in the spec's *Decisions* section,
  which the checkpoint keeps current; after close-out, in the repo's **flow document**, which
  describes each main flow of the subsystem as it works today and links the closed spec for the
  *why*. The flow document and the code are the source of truth for how the system works; the
  README links the flow document and doesn't duplicate it.
- The implementer updates the flow document in the same PR when a flow changes, and code review
  checks it.

**What we give up**: more tokens per merge (a `sonnet` checkpoint without code exploration,
estimated at 15–30k tokens each against 101k measured for one `opus` re-review; assumption: its
input is the spec, the outlines and the findings' text only), milestones that
grow and last longer, one more document per repo to keep current, and the *why* of design detail
living in closed spec issues on GitHub rather than in `docs/decisions/` (the GitHub coupling
[0001](0001-github-driven-triage-refinement-and-autonomous-implementation.md) already accepted).

**Sequence**, by impact, one PR each:

1. The findings rule and growth cap: a shared reference in `github-workflow-setup`, used by the
   queue's end-of-run report and the *Learned* section in `github-implement`'s delivery. It
   resolves the immediate problem (20 findings without a home).
2. Just-in-time refinement and the post-merge checkpoint (`sonnet`, escalating to
   `github-refine` on a pivot) in `github-refine` and the queue policy.
3. Two-level design records: the `adr` skill (scope and lifecycle), `github-shape`'s close-out
   (accepts the milestone's ADRs, moves detail to the flow document), and the flow document as a
   `quality-baseline` item.
4. In `finance-agent`, as its own work: route the 20 findings, reclassify its 14 ADRs and write
   its flow document.

**Scope**: the GitHub workflow skills, `adr`, `quality-baseline`, and every repo that uses them;
first `finance-agent`.

**Confidence**: medium. The problem is measured on one milestone only. Revisit if the checkpoint
costs more tokens than the rework it prevents, if `sonnet` routes findings wrongly or escalates
most of them as R1 (then the checkpoint needs `opus`, or the rule is unclear), if milestones
regularly hit the growth cap (the threshold or the shaping is wrong), or if the flow document
drifts from the code.

### Consequences

- Good: what a ticket learns reaches the remaining tickets while the context is fresh; findings
  can no longer be lost.
- Good: fewer ADRs, and the ones written survive spec pivots; detail can change without
  superseding records.
- Good: tidying and debt are normal work of the milestone that produced them, as Beck recommends.
- Bad: the checkpoint is an extra step on every merge with findings. Mitigated: it runs on
  `sonnet`, reads no code and is skipped when there is nothing to route or brief; `opus` runs only
  on a pivot.
- Bad: while a milestone is open, reviewers check code against `Proposed` ADRs and the spec's
  *Decisions*, which are still moving. Mitigated: the checkpoint is the only writer of *Decisions*
  and runs between merges, never during a review, so each review sees a stable version.
- Bad: refinement is spread over the milestone instead of done once. Each brief is still written
  once, only later; the extra cost is reloading the spec at each checkpoint, plus one `opus`
  refinement per pivot.
- Bad: a `sonnet` checkpoint may miss a pivot that `opus` would see. Accepted because the per-PR
  `opus` reviewers still read every diff, and their findings are the checkpoint's input.

### Confirmation

- `skills/github-work-queue/evals/scenarios.md` gains scenarios: a finding of each kind R1–R5 is
  routed as the table says; the growth cap escalates; a checkpoint that stays inside the spec's
  bounds briefs the next slice without asking; a checkpoint unsure of a finding routes it as R1; a
  slice whose outline no longer fits goes to `github-refine` instead of being rewritten; the
  checkpoint never reads the diff.
- `queue-policy.md` passes `model: "sonnet"` to the checkpoint subagent, and
  [`docs/model-watch.md`](../model-watch.md) gets a row to review the choice after the first
  milestone run under this rule.
- `skills/adr/evals/scenarios.md`: an ADR written during an open milestone stays `Proposed`; a
  code-level decision is routed to the spec's *Decisions*, not to an ADR.
- `quality-baseline`'s audit reports a repo without a flow document linked from its README.

**Success measure**:

- Findings without a destination when a milestone closes: target 0, read by comparing the
  end-of-run reports and reviews with the milestone's issues; baseline 20 (measured,
  `finance-agent` "Self-service setup", 2026-10-18).
- ADRs accepted under this rule that need superseding within the next milestone: target 0;
  baseline 3 of 14 in three days (measured, `finance-agent`, 2026-10-18).
- Checkpoint cost per merge: estimated 15–30k tokens on `sonnet`; measure it on the first
  milestone run under this rule (subagent token usage per checkpoint) and compare it with the fix
  rounds it avoided.
- Routing quality of the `sonnet` checkpoint: share of its routings the owner corrects, read from
  the milestone's issues; target `TBD`, set after the first milestone.

## Pros and cons of the options

### A. Do nothing

- Good: no work; the pipeline stays simple.
- Bad: findings keep piling up in reports with no home; specs and ADRs keep drifting from the
  code.

### B. Heavier up-front specs

- Good: catches some deviations before any code exists.
- Bad: fights the premise. The data-model flaw in `finance-agent` surfaced only when a review
  exercised partial sales on real code; more shaping would not have found it. It also costs more
  of the owner's time, which is the scarce resource.

### C. A cooldown between milestones (Shape Up)

- Good: proven in small teams; features and chores don't compete within a cycle.
- Bad: findings wait outside the milestone that produced them and lose their context, and they
  can be postponed forever. It breaks the self-contained milestone driver.

### D. Adaptive milestone (chosen)

- Good/Bad: see *Consequences*. Inside D, the design records were weighed three ways:
  immutable code-level ADRs as today (rejected: 21 % already need revision); ADRs kept `Proposed`
  until close-out, without changing their level (rejected alone: detail keeps changing after
  acceptance); higher-level ADRs with a flow document and the code as the source of truth
  (chosen, combined with the `Proposed`-until-close-out lifecycle for architecture ADRs decided
  mid-milestone). The flow document follows how the owner works at ClearBank, where each repo
  documents the main flows of the subsystem it implements.

## More information

- Kent Beck on specs as a best effort and on interleaving tidying with behaviour changes
  (*Tidy First?*, 2023).
- Shape Up, six-week cycles followed by a cooldown: <https://basecamp.com/shapeup>
- The retro skill planned in [0004](0004-three-layer-baseline-decisions-shaping-implementation.md)
  takes its input from the findings tagged under *Retro input*.
- Doubt review: not run. The decision changes skill prose and is cheap to reverse; run it before
  accepting if the review raises doubts.
