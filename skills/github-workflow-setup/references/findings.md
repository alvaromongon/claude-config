# Findings

Where something learned during a milestone goes, so nothing is lost and each milestone stays
self-contained. Design: [ADR 0005](../../../docs/decisions/0005-adaptive-milestones-findings-rule-and-two-level-design-records.md).

A **finding** is anything learned while working a milestone that the current ticket doesn't
cover: a reviewer's non-blocking item, an inconsistency the implementer saw outside its scope
(its PR's *Learned* section), a gap in the spec, a step of the plan with no issue.

## The rule

The first rule that matches wins:

| # | The finding… | Destination | Decided by |
|---|---|---|---|
| R1 | changes the spec's what or why (metric, *not doing*, a public contract) or an architecture ADR | A `decision` issue blocking the spec, or a new spec — both through `github-shape` | Owner |
| R2 | affects an open ticket not yet implemented, or one that will be redone | Edit that ticket's brief (new acceptance criterion) and comment why | Agent |
| R3 | is a defect in work delivered in this milestone | New ticket in the same milestone | Agent |
| R4 | is debt, tidying or a chore, even outside the spec's scope | New ticket in the same milestone | Agent |
| R5 | isn't worth its cost | Discarded, with the reason | Owner confirms |

When unsure between R1 and another rule, pick R1: a wrong call then costs the owner a question,
not a design change made unseen.

## Applying it

- **R2**: add the criterion to the brief under *Acceptance criteria*, and a comment on the issue
  quoting the finding and where it came from.
- **R3 / R4**: a new issue whose body is a brief (`../../github-triage/references/brief-format.md`)
  plus a first line `**Found in**: #<PR or issue> (R3|R4)`, in the milestone of the ticket that
  produced the finding (none if that ticket has none, linking it instead). Label it the way
  `github-refine` does: `ready-for-human` when it needs human judgment, manual testing or a
  sensitive area you wouldn't pre-approve, `ready-for-agent` otherwise. When a pending ticket
  needs the fix first, add the blocking edge (`dependencies.md`).
- **R1**: don't open the decision yourself; list it for the owner with the suggested
  `/github-shape` call. Tickets it affects wait: add the decision as their blocker once it exists.
- **R5**: once the owner confirms, comment the discard and its reason on the PR or issue the
  finding came from, so the decision not to act is recorded.
- **Who applies it**: the work queue's checkpoint applies R2–R4 on its own and returns R1 and R5
  to the owner (`../../github-work-queue/references/queue-policy.md` › *Checkpoint*). Outside the
  queue, whoever finds it proposes the routing and applies it after the owner approves.
- **Retro input**: a finding that shows a gap in the process (something the quality baseline, a
  review or refinement should have caught) is also tagged `retro` in the routing table.
- **Never** edit closed issues, reopen merged PRs or rewrite the milestone; the milestone only
  gains tickets.

## Growth cap

Count the open and closed issues in the milestone that carry a `**Found in**` line. When routing
one more R3 or R4 would take that count above **50 %** of the milestone's other issues (the ones
`github-refine` created), route it as R1 instead: the owner decides whether to accept the growth
and update the spec's appetite, move the rest into a new spec, or cut. The threshold is an
estimate under review (ADR 0005).

## Invariant

Every finding ends in R1–R4 or is discarded under R5. A milestone is done only when none of its
issues is open.
