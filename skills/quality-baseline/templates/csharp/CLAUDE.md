# CLAUDE.md

The README is the single source of truth. Read the relevant section instead of duplicating it here:

| Topic | README section |
|---|---|
| What it does, how to run it | [At a glance](README.md#at-a-glance), [How to run](README.md#how-to-run) |
| Tests and local gate | [How to test](README.md#how-to-test), [Quality gates](README.md#quality-gates) |
| Folder structure and conventions | [Structure and conventions](README.md#structure-and-conventions) |
| Design and decisions | [Design](README.md#design), [docs/decisions/](docs/decisions/README.md) |
| SLO and load test | [SLO](README.md#slo) |

## Rules for Claude
- TDD: failing test → minimal code → refactor. No production code ahead of a failing test.
- Run the local gate (`./.githooks/pre-push`) before declaring a change done.
- Keep the SLO in the README and the k6 thresholds (`tests/*.LoadTests/scripts/`) in sync.
- Architecturally significant designs are recorded as ADRs (`adr` skill), proposed via PR.

## Overrides of the personal baseline
None. <!-- State each override and why, e.g. "No load test: library without a runtime." -->
