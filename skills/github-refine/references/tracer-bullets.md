# Tracer-bullet tickets

## Core principle

Each ticket is a **vertical slice**: it crosses every layer the change touches (schema, API, UI,
tests — whichever apply), not one layer at a time. The test for a good cut: "what can I demo when
this lands?" The answer must be working behavior, not "the migration is in" or "the endpoint
exists but nothing calls it."

A horizontal slice ships one layer. Nothing works until every layer has landed — so nothing is
demoable, reviewable in isolation, or safely abandonable, until the whole set is done.

## Common pitfalls & fixes

- **Over-decomposition**: too many tiny tickets for a change that fits one context window. Fix:
  merge at the quiz step (see Procedure in `../SKILL.md`).
- **Layer-based slicing**: "add DB column" / "add API field" / "add UI field" as three tickets.
  Fix: reframe as one ticket per demoable end-to-end path; prefactoring tickets are the exception
  (see below).
- **Wide refactors**: a change that touches many call sites at once doesn't slice vertically by
  nature. Fix: expand-contract — one ticket adds the new form (old and new coexist), one or more
  tickets migrate call sites in batches, one ticket removes the old form.

## Prefactoring

Preparatory work that must land before the feature tickets can be vertical slices themselves
(e.g. extracting a seam, introducing an interface) gets its own ticket(s), sequenced first and
blocking the feature tickets. It's the one legitimate case where a ticket isn't itself demoable
new behavior — it's demoable as "nothing broke, and the seam now exists."

## Success indicators

- Every ticket is demonstrable independently once its blockers have landed.
- The first ticket in the graph has zero blockers.
- Prefactoring tickets precede the feature tickets they unblock.
- No file paths or line numbers baked into ticket bodies — they go stale; point at modules/behavior
  instead.
