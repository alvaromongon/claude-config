# CLAUDE.md

The README is the single source of truth. Read the relevant section instead of duplicating it here:

| Topic | README section |
|---|---|
| What it does, how to run it | [At a glance](README.md#at-a-glance), [How to run](README.md#how-to-run) |
| Tests and local gate | [How to test](README.md#how-to-test), [Quality gates](README.md#quality-gates) |
| Folder structure and conventions | [Structure and conventions](README.md#structure-and-conventions) |
| Design, flows and decisions | [Design](README.md#design), [docs/flows.md](docs/flows.md), [docs/decisions/](docs/decisions/README.md) |
| SLI/SLO and load test | [SLO](README.md#slo) |

## Rules for Claude
- TDD: failing test → minimal code → refactor. No production code ahead of a failing test.
- Run the local gate (`./.githooks/pre-push`) before declaring a change done.
- Keep the SLO table in the README and the k6 thresholds (`tests/*.LoadTests/scripts/`) in sync.
- Architecture decisions are recorded as ADRs (`adr` skill), proposed via PR; design detail goes
  in the spec's *Decisions* and then `docs/flows.md`.
- A change to a main flow updates `docs/flows.md` in the same PR.

## Push and merge policy
Ask before every `git push`. <!-- Or, for repos running the autonomous GitHub workflow (set up by
`github-workflow-setup`): "Agents may push `issue-*` branches, open PRs and merge PRs of
`ready-for-agent` issues once reviews and CI are green; ask before any other push." -->

## Overrides of the personal baseline
None. <!-- State each override and why, e.g. "No load test: library without a runtime." -->
