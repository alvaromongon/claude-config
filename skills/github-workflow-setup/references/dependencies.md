# Blocking dependencies

Single reference for how the `github-*` skills record and check "issue A is blocked by issue B".
Written by `github-refine`; read by `github-implement` (precondition) and `github-work-queue`
(frontier). GitHub's native issue dependencies are the source of truth; the checklist is only a
fallback.

## Native relations (preferred)

`{owner}/{repo}` placeholders are filled in by `gh` from the current repo.

```bash
# Add: <n> is blocked by <m>. The API takes the blocker's numeric id, not its number.
blocker_id=$(gh api repos/{owner}/{repo}/issues/<m> --jq .id)
gh api -X POST repos/{owner}/{repo}/issues/<n>/dependencies/blocked_by -F issue_id="$blocker_id"

# Check: open blockers of <n> (empty output = unblocked).
gh api repos/{owner}/{repo}/issues/<n>/dependencies/blocked_by \
  --jq '.[] | select(.state == "open") | .number'

# Remove a relation.
gh api -X DELETE repos/{owner}/{repo}/issues/<n>/dependencies/blocked_by/"$blocker_id"
```

Verified on 2026-10-03, including on a private free-plan repo (`POST` returns the blocked issue).
If these endpoints fail (plan or API not available), say so and use the fallback below — never
silently skip the blocking edges.

## Fallback: checklist in the issue body

```markdown
## Blocked by
- #12
- #15
```

Check it with `gh issue view <n> --json body`, then `gh issue view <m> --json state` for each listed
number. Treat an unparseable section as blocked and report it, rather than guessing.

## Frontier

The frontier of a set of issues is those with no open blocker by either method. Recompute it after
every merge: closing one issue may unblock others.
