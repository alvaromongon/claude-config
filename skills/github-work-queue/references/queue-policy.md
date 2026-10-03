# Queue policy

## Preconditions

The repo is set up by `github-workflow-setup`: `docs/agents/workflow.md` exists and the push
policy lets agents push `issue-*` branches. If not, stop before the first ticket and say what's
missing — without push rights every ticket would end as a local branch.

## Building the queue

List open issues labeled `ready-for-agent` (optionally scoped to one milestone if the user asked
for that). Compute the **frontier** per `../../github-workflow-setup/references/dependencies.md`:
issues in that set whose blocking issues are all closed. Only the frontier is workable right now;
the rest wait for their blockers.

## Per-ticket loop

For each issue on the frontier, one at a time (no parallel worktrees in this version — see ADR
0001's deferred work):

1. **Implement**: spawn a subagent (via the `Agent` tool, fresh context) with a prompt that
   invokes `github-implement` with the issue number as argument. Wait for it to finish; collect
   branch/PR.
2. **Review**: spawn two **separate** subagents in parallel (fresh context each, never the
   implementer's), each with `isolation: "worktree"` and told to run `gh pr checkout <n>` in that
   worktree first — so both review exactly the PR's branch, without touching each other's or the
   main session's working tree:
   - one invoking `code-review` with the PR number as target (correctness, reuse, simplification
     — same pattern as Matt Pocock's `code-review` axes);
   - one invoking `security-review`, which reviews the pending changes of the checked-out branch
     against the default branch, i.e. the PR's diff.

   Both report-only, neither edits code nor pushes. This is the only review gate before an
   unattended merge, so security findings get the same weight as correctness findings here, not
   left to CI's CodeQL pass alone.
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

On escalation: leave the ticket's branch/PR as-is, label it back to `ready-for-human` with a
comment explaining why, and **keep processing the rest of the frontier** — one stuck ticket
doesn't stall tickets that don't depend on it.

## End-of-run report

Summarize: merged, waiting-for-human-review, escalated (with reason), and still-blocked (with
what they're waiting on).
