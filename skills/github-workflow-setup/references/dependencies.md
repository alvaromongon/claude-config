# Blocking dependencies

Single reference for how the `github-*` skills record and check "issue A is blocked by issue B".
Written by `github-refine` (and `github-shape`: a decision blocks its spec); read by `github-implement` (precondition) and `github-work-queue`
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

## Between milestones

GitHub has no relations between milestones. The order between milestones is the blocking edges
between their `spec` issues: spec A is blocked by spec B when work in A needs what B delivers —
typically an open ticket of A blocked by an open ticket of B (a closed blocker orders nothing). Only **real** dependencies: a preference ("do B
first") is never an edge, so the graph stays trustworthy; between milestones with no edge, the
owner chooses. `github-shape` adds the edge when a new spec needs another one's outcome, and
`github-refine` when a slice's blocker (or a ticket it blocks) lives in another milestone.

A spec blocked by another spec can still be shaped and refined (only an open `decision` blocks
refinement). The work queue doesn't read these edges: they tell the owner which milestone to scope
a queue run to. **What's next**: the ticket frontier above decides what can be worked; the spec
edges decide which milestone goes first — one whose spec blocks others is on the path that
unblocks them. A milestone whose spec is blocked can still have tickets on the frontier: they are
workable, just not on the path to closing it. Between milestones with no edge, the owner chooses.
Spec blockers of each open spec:

```bash
for n in $(gh issue list --label spec --state open --json number --jq '.[].number'); do
  echo "#$n blocked by specs: $(gh api repos/{owner}/{repo}/issues/$n/dependencies/blocked_by \
    --jq '[.[] | select(.state == "open" and any(.labels[]; .name == "spec")) | "#\(.number)"] | join(" ")')"
done
```

