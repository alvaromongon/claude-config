# Spec and decision issue formats

The global `CLAUDE.md` › *Decisions* method, applied to shaping. Write in the repo's documentation
language; keep it short enough to re-read in one pass.

## Spec issue (label `spec`)

Title: the outcome, not the solution ("Users see their balance without a page reload", not
"Add websocket").

```markdown
## Problem

<who has it and what happens today, from their side; one paragraph>

## Why it matters

<the customer, money, risk or date at stake, with a figure labelled measured (source) or
estimated (assumption)>

## Success metric

- **Metric**: <what is measured>
- **Target**: <the number that means it worked>
- **How it's measured**: <technical promise → the executable check that proves it (k6 threshold,
  named test, CI gate); business promise → the metric and where it's read, or "estimate" with its
  assumption>
- **Scope**: <which users, teams or systems it affects>
- **Baseline**: <today's value, measured or estimated, or `TBD` with what's needed>

## Appetite

<how much this is worth investing, in PRs or days — e.g. "about 3 PRs", "one week". Past the
appetite, cut scope or re-shape; don't extend silently>

## Options

- **<option A> (chosen)**: <one line> — trade-off, risk
- **<option B>**: <one line> — trade-off, risk
- **Do nothing / buy**: <when they apply> — trade-off, risk

**What we give up**: <the accepted trade-off, and what would change our mind. If it adds
complexity, why the simple option isn't enough>

## Not doing

- <explicitly out of scope>

## Risks

- <where it can get stuck, and how we'd find out early>

## Decisions

- <open: link to each blocking decision issue> / <closed: link — one-line answer>
```

## Decision issue (label `decision`)

Blocks its spec. Title: the question ("Which store holds session state?").

```markdown
## Question

<the decision this issue resolves, and why the spec can't proceed without it>

**Spec**: <link>

**Resolve by**: <conversation | research | prototype | someone else's input — who>
```

The answer goes in a closing comment: conclusion first, then the options weighed and what we give
up, with figures labelled measured or estimated. Link the ADR if one was written.
