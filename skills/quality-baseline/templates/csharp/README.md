# <Project name>

<!-- Template: keep the section order; delete what does not apply and say why under Assumptions. -->

## At a glance

- **What it does**: <one or two sentences>.
- **Run it**: `docker compose up` → <http://localhost:8080>.
- **SLO**: <status (met / aspirational / baseline) and the headline figure, e.g. p95 measured
  48 ms vs objective < 50 ms at 1000 req/s> — see [SLO](#slo).
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

<Main components, in a paragraph. How each main flow works: [docs/flows.md](docs/flows.md).
Decisions: [docs/decisions/](docs/decisions/README.md).>

## SLO

<Reference environment and calibration runs (0.5×, 1×, 2×, 4×). One row per SLI; status is
*Met*, *Aspirational* (state gap and plan), *Baseline* (objective = measured value) or
*Insufficient data* (state minimum sample). The k6
thresholds enforce the measured value unless the status is *Met*.>

| SLI | How it is measured | Measured | Objective | Status |
|---|---|---|---|---|
| <p95 latency at 1000 req/s> | <k6, stubbed dependency> | <48 ms> | << 50 ms> | <Met> |
| <error rate> | <k6> | <0.05%> | << 0.1%> | <Met> |
| <upstream calls per interval> | <stub request count> | <N> | <≤ N> | <Baseline> |

## Assumptions

- <Assumption and its consequence.>

## Quality gates

| Check | Local (pre-push) | CI |
|---|---|---|
| Format | ✅ | ✅ |
| Build, analyzers, warnings as errors | ✅ | ✅ |
| Locked restore + vulnerable dependencies | ✅ | ✅ |
| Tests + coverage ≥ 80% | ✅ | ✅ |
| CodeQL | — | ✅ |
| Container build + image scan | — | ✅ |
| Load test (SLO) | on demand | on demand (`workflow_dispatch`) |

## Future enhancements

- <Enhancement and why it was deferred.>

## AI-assisted development

<How AI assistance was used (e.g. Claude Code with TDD, local gate and human review of every
change) and where the project rules for it live (`CLAUDE.md`).>
