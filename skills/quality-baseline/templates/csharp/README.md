# <Project name>

<!-- Template: keep the section order; delete what does not apply and say why under Assumptions. -->

## At a glance

- **What it does**: <one or two sentences>.
- **Run it**: `docker compose up` → <http://localhost:8080>.
- **SLO (measured)**: <e.g. 1000 req/s sustained, p95 < 50 ms, p99 < 100 ms, errors < 0.1%,
  ≤ N upstream calls per interval> — see [SLO](#slo).
- **Quality**: <coverage %>, warnings as errors, CodeQL, Trivy, pre-push gate — see
  [Quality gates](#quality-gates).

## Requirements

- <SDK/runtime and version>, Docker.

## How to run

<Commands and URLs (API, OpenAPI document, health endpoints).>

## How to test

<Unit, component and load tests: commands and what each level covers.>

## Structure and conventions

<Folder tree with one line per folder; naming conventions; link to the platform's official guide.>

## Design

<Main components and flows. Decisions: [docs/decisions/](docs/decisions/README.md).>

## SLO

<Objectives (load, latency percentiles, error rate, downstream protection), reference environment,
calibration runs (0.5×, 1×, 2×, 4×) and how the load test enforces them.>

## Assumptions

- <Assumption and its consequence.>

## Quality gates

| Check | Local (pre-push) | CI |
|---|---|---|
| Format | ✅ | ✅ |
| Build, analyzers, warnings as errors | ✅ | ✅ |
| Locked restore + vulnerable dependencies | — | ✅ |
| Tests + coverage ≥ 80% | ✅ | ✅ |
| CodeQL | — | ✅ |
| Container build + image scan | — | ✅ |
| Load test (SLO) | on demand | on demand (`workflow_dispatch`) |

## Future enhancements

- <Enhancement and why it was deferred.>

## AI-assisted development

<How AI assistance was used (e.g. Claude Code with TDD, local gate and human review of every
change) and where the project rules for it live (`CLAUDE.md`).>
