---
status: Proposed   # Proposed | Accepted | Rejected | Deprecated | Superseded by [NNNN](NNNN-title.md)
date: yyyy-mm-dd   # of the last status change
decision-makers: <who decides>
consulted: "<optional: who was consulted>"
---

# NNNN. <Title: the problem solved and the solution, in a short phrase>

- **Issue**: <link>
- **Supersedes**: <optional: [NNNN](NNNN-title.md)>

**Decision**: <one sentence: what we decide and the outcome we expect, with its figure.>

## Context and problem statement

<The problem in two or three sentences, with the context needed to understand it without reading anything else.>

**Why it matters**: <the customer, money, risk or date at stake, with a figure labelled measured (source) or estimated (assumption).>

## Decision drivers

- <requirement, constraint or quality that weighs on the decision>

## Considered options

- <option 1>
- <option 2>
- <buy / do nothing, when they apply>

## Decision outcome

Chosen option: "<option>", because <justification tied to the decision drivers>.

**What we give up**: <the accepted trade-off; if it adds complexity, why the simple option isn't enough.>

**Sequence**: <optional: what goes first and why, by impact.>

**Confidence**: <high | medium | low>. <What would make us revisit it.>

### Consequences

- Good: <…>
- Bad: <…>

### Confirmation

<How compliance with the decision is checked: link the test, CI gate or k6 threshold that enforces it.>

**Success measure**: <the metric and its target. Technical promise → link the executable check that proves it (k6 threshold, named test, CI gate). Business promise → the metric and where it's read, or "estimate" with its assumption.>

## Pros and cons of the options

### <option 1>

<short description or link>

- Good: <…>
- Neutral: <…>
- Bad: <…>

### <option 2>

- Good: <…>
- Bad: <…>

## More information

<Sources, longer research, related decisions, when to revisit it.>
