# Queue policy

## Preconditions

The repo is set up by `github-workflow-setup`: `docs/agents/workflow.md` exists and the push
policy lets agents push `issue-*` branches. If not, stop before the first ticket and say what's
missing — without push rights every ticket would end as a local branch.

## Building the queue

List open issues labeled `ready-for-agent` (optionally scoped to one milestone if the user asked
for that). Compute the **frontier** per `../../github-workflow-setup/references/dependencies.md`:
issues in that set whose blocking issues are all closed. Only the frontier is workable right now;
the rest wait for their blockers. Leave out issues that already have a linked PR
(`gh issue view <n> --json closedByPullRequestsReferences`): they are waiting for review from an
earlier run (`Unattended merge: no`), and implementing them again would open a duplicate PR.

Outlines (`../../github-refine/references/tracer-bullets.md` › *Outline issues*: no `ready-*`
label, body headed `## Outline`) are never implemented. If an outline in the milestone of a queued
issue (or the milestone the user scoped the run to) has all its blockers closed, run a *Checkpoint* before the first ticket, so it is briefed and can join
the frontier.

## Waiting PRs

With `Unattended merge: no`, PRs wait for review side by side, each branched from the same
default branch; once the human merges one, the others can conflict with it. (With `yes` this
can't happen: each ticket is merged before the next one branches.) So before the per-ticket loop,
check every open PR linked to a `ready-for-agent` issue (`gh pr view <n> --json mergeable`) and,
for each `CONFLICTING` one, spawn an implementer subagent to refresh it: `gh pr checkout <n>`,
`git pull --no-rebase origin <default branch>`, resolve keeping both sides' intent, run the local
gate, `git push origin <issue branch>` (a normal push — never rewrite the branch). Then review it
again (step 2 below) and wait for CI, and leave it ready for review. If a conflict can't be
resolved without guessing at intent, escalate that ticket. Re-run the queue after merging a
waiting PR to refresh the rest.

## Subagent models

Pass `model` on every `Agent` call
([ADR 0003](../../../docs/decisions/0003-assign-models-per-skill-by-role.md)): `"sonnet"` for
implementer subagents (implement, fix loop, refreshing a conflicting PR) and `"opus"` for both
reviewers. The reviewers are the only gate before an unattended merge, so they run on a stronger
model than the one whose work they check. The checkpoint subagent runs on `"sonnet"`: it follows
rules over findings already produced and never reviews code
([ADR 0005](../../../docs/decisions/0005-adaptive-milestones-findings-rule-and-two-level-design-records.md)).
Aliases only, never model IDs.

## Per-ticket loop

For each issue on the frontier, one at a time (no parallel worktrees in this version — see ADR
0001's deferred work):

1. **Implement**: spawn a subagent (via the `Agent` tool, `model: "sonnet"`, fresh context) with
   a prompt that invokes `github-implement` with the issue number as argument. Wait for it to
   finish; collect branch/PR.
2. **Review**: spawn two **separate** subagents in parallel (`model: "opus"`, fresh context each,
   never the implementer's), each with `isolation: "worktree"` and told to run `gh pr checkout <n>`
   in that worktree first — so both review exactly the PR's branch, without touching each other's
   or the main session's working tree:
   - one invoking `code-review` with the PR number as target (correctness, reuse, simplification
     — same pattern as Matt Pocock's `code-review` axes);
   - one invoking `security-review`, which reviews the pending changes of the checked-out branch
     against the default branch, i.e. the PR's diff.

   Tell the `code-review` reviewer to also report, as findings, a change to a main flow that
   doesn't update `docs/flows.md`, and a change that contradicts an accepted ADR, a `Proposed` ADR
   of the open milestone or the spec's *Decisions*.

   Both report-only, neither edits code nor pushes. This is the only review gate before an
   unattended merge, so security findings get the same weight as correctness findings here, not
   left to CI's CodeQL pass alone. Tell each reviewer it **must** invoke its skill through the
   Skill tool — not "if available": given the option, reviewers skip `code-review` and review by
   hand. Afterwards remove both worktrees (`git worktree remove --force <path>`, then
   `git branch -D worktree-agent-*`): they hold another commit, so Claude Code keeps them.
3. **Fix loop**: if either review raises blocking findings, spawn one more implementer subagent to
   address them, referencing both reviews' findings verbatim. One retry only — if it's still not
   clean after that, escalate (see below), don't keep looping.
4. **CI**: wait for the PR's checks (`gh pr checks <n> --watch` or poll) to go green.
5. **Merge or hand off**: if everything above is clean and `docs/agents/workflow.md` says
   `Unattended merge: yes` (the default), merge (`gh pr merge --squash` or the repo's configured
   strategy). With `Unattended merge: no`, stop at "ready for your review" instead — but keep the
   ticket marked done on this skill's side and continue the queue; don't block other frontier
   tickets on this one's human review.
6. **Checkpoint**: collect the ticket's findings — the PR's *Learned* section and every
   non-blocking finding of both reviews still standing after the fix round, each with the PR it
   came from — and run a *Checkpoint* if there are any, or if an outline in the milestone now has
   all its blockers closed. Also after an escalated ticket: its non-blocking findings count too.
   Otherwise skip it and say so in the report.
7. **Recompute the frontier** (closing this ticket may unblock others, and the checkpoint may have
   briefed outlines or added tickets) and continue.

## Escalation

Same triggers as `github-implement`'s stop conditions, plus:
- the fix loop in step 3 didn't produce a clean review.

When a brief's acceptance criteria already require a sensitive area its *Sensitive areas* field
doesn't list, escalate it while building the queue instead of spawning an implementer that would
only stop.

On escalation: leave the ticket's branch/PR as-is, label it back to `ready-for-human` with a
comment explaining why, and **keep processing the rest of the frontier** — one stuck ticket
doesn't stall tickets that don't depend on it.

## Checkpoint

Spawn one subagent (`Agent`, `model: "sonnet"`, fresh context). Its prompt carries the findings
verbatim with their source PR, the milestone and its spec issue. It may read the spec (including
*Decisions*) and the milestone's issues with `gh`; it **never** reads a diff, checks out a branch
or explores the codebase — that is the reviewers' job and the expensive part. A question only the
code can answer is routed as R1 or written into a brief as unverified. Its tasks:

1. **Route** each finding per `../../github-workflow-setup/references/findings.md` (merge
   duplicates first; check the growth cap). Apply R2, R3 and R4 directly — the agent decides
   inside the spec's bounds. Don't apply R1 or R5: return them for the owner. When unsure, R1.
2. **Brief** each outline whose blockers are all closed: replace its body with a brief
   (`../../github-triage/references/brief-format.md`) built from the outline, the spec and what
   the earlier tickets learned, and label it the way `github-refine` does. It can't pre-approve a
   sensitive area: if the slice needs one, label it `ready-for-human` and propose the area.
3. **Spot pivots**: if an outline no longer fits — what was learned changes its outcome, its
   blockers or the order of the slices — don't brief or rewrite it; return it as a pivot with the
   reason, for `/github-refine` to re-refine (`opus`, owner-approved). If the spec's metric,
   *not doing* or appetite would move, return it as R1 instead.
4. **Record decisions**: a design choice settled while briefing goes into the spec's *Decisions*
   as "settled in checkpoint (date, PR #n)". The checkpoint is the only writer of *Decisions*
   while the milestone is open, and runs between tickets, never during a review.
5. **Leave a record**: one comment on the ticket's PR — findings routed (rule → destination),
   outlines briefed, pivots, R1/R5 items returned, and the growth-cap count. The spec's close-out
   reads these comments instead of reviewing the milestone's code again.

## Routing at the end of the run

Run one last checkpoint for the findings you noticed yourself while orchestrating (a plan step
with no issue, a check that didn't run). Then put every returned R1, R5 and pivot item in the
report for the owner: R1 with its `/github-shape` call, pivots with their `/github-refine` call,
and R5 discards to confirm — comment each confirmed discard on its source PR or issue. Nothing is
left as a loose list.

## End-of-run report

Summarize: merged, waiting-for-human-review (including refreshed ones), escalated (with reason),
still-blocked (with what they're waiting on), what the checkpoints routed and briefed (with the
growth-cap count), and the R1, R5 and pivot items waiting for the owner.
