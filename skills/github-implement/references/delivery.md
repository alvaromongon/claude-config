# Delivery conventions

## Branch

One branch per issue, created from the repo's default branch:
`issue-<number>-<short-slug-from-title>`. Verify the working tree is clean and the default branch
is up to date before branching (`git status`, `git pull`) — never force-reset over local state you
didn't create this session.

## Commits

Small, logical, each referencing the issue (`#<number>` in the body). TDD red/green/refactor steps
can be separate commits or squashed at the end — whichever makes the diff easiest to review; don't
leave a broken intermediate commit as the final history.

## Pull request

Open with `gh pr create`, body covering:
- **Summary**: what changed and why, tied to the issue's acceptance criteria.
- **Evidence**: test output showing the change (failing → passing), or before/after for anything
  visual.
- **Linked issue**: `Closes #<number>`.

This skill does not merge the PR and does not review it — that's the caller's job
(`github-work-queue` spawns a separate reviewer subagent; a standalone invocation leaves it to the
user).

## Stop conditions (escalate instead of guessing)

Matches the defaults in `github-workflow-setup`'s `templates/workflow.md` (check the repo's
`docs/agents/workflow.md` for overrides):

- Tests don't stabilize after 3 attempts at the same seam.
- An acceptance criterion turns out ambiguous once you're implementing it.
- The change touches a sensitive area (auth, payments, infra, CI) that wasn't already flagged
  `ready-for-agent` with that in mind.
- The issue doesn't actually carry `ready-for-agent`, or one of its blocking issues isn't closed
  yet.

On any of these: stop, report what you found and why you stopped, and leave the branch/commits as
they are for a human to pick up — don't push partial work as if it were done.
