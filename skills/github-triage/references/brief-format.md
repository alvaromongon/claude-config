# Agent brief format

Posted as a comment on the issue when it moves to `ready-for-agent` or `ready-for-human`. Written
so `github-implement` (or a human) can start from it without re-reading the whole thread.

```markdown
## Agent brief

**What**: <one or two sentences, the demoable behavior change — not a layer>

**Verified**: <what you actually reproduced/checked — repro steps run, PR branch checked out and
read, log/error confirmed — not just "the reporter says">

**Acceptance criteria**:
- <checkable condition>
- <checkable condition>

**Pointers**: <relevant files/modules if already known; omit if unknown — do not guess>

**Out of scope**: <anything explicitly not included, to prevent scope creep>
```

Keep it short enough to re-read in one pass. No file paths/line numbers unless you actually
verified them — stale pointers are worse than none.
