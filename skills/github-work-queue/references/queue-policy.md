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
model than the one whose work they check. Aliases only, never model IDs.

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
6. **Recompute the frontier** (closing this ticket may unblock others) and continue.

## Escalation

Same triggers as `github-implement`'s stop conditions, plus:
- the fix loop in step 3 didn't produce a clean review.

When a brief's acceptance criteria already require a sensitive area its *Sensitive areas* field
doesn't list, escalate it while building the queue instead of spawning an implementer that would
only stop.

On escalation: leave the ticket's branch/PR as-is, label it back to `ready-for-human` with a
comment explaining why, and **keep processing the rest of the frontier** — one stuck ticket
doesn't stall tickets that don't depend on it.

## End-of-run report

Summarize: merged, waiting-for-human-review (including refreshed ones), escalated (with reason), and still-blocked (with
what they're waiting on).
