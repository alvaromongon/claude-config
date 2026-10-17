# Agent brief format

Posted as a comment on a triaged issue when it moves to `ready-for-agent` or `ready-for-human`;
for tickets created by `github-refine`, it is the issue body. Written
so `github-implement` (or a human) can start from it without re-reading the whole thread.

```markdown
## Agent brief

**What**: <one or two sentences, the demoable behavior change — not a layer>

**Verified**: <what you actually reproduced/checked — repro steps run, PR diff read (never
checked out), log/error confirmed — not just "the reporter says">

**Acceptance criteria**:
- <checkable condition>
- <checkable condition>

**Sensitive areas**: <`none`, or the sensitive areas (per docs/agents/workflow.md) this change is
expected to touch and that the human approved for agent work, e.g. "CI workflows">

**Pointers**: <relevant modules if already known (paths only when verified and stable); omit if
unknown — do not guess>

**Out of scope**: <anything explicitly not included, to prevent scope creep>
```

*Sensitive areas* makes the implementer's stop condition decidable: touching a sensitive area
not listed here means stop and escalate. An issue whose sensitive areas aren't acceptable for
agent work is `ready-for-human`, not `ready-for-agent` with a long list.

Keep it short enough to re-read in one pass. Link domain terms to the repo's glossary; if the
change introduces a term, adding it there is an acceptance criterion. No file paths/line numbers unless you actually
verified them — stale pointers are worse than none.
