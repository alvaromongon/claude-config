# Cross-language baseline

## Tests
- **Unit**: fast, isolated, mocks for collaborators. Folder/namespace mirrors source; one test
  class/file per unit; names `Method_Scenario_ExpectedResult` (or the language idiom).
- **Component**: run the service in-process, stub every external HTTP dependency (WireMock or
  equivalent). Never call real third-party APIs from tests.
- **Load**: k6 against the container with dependencies stubbed (WireMock with latency), via Docker
  Compose. The SLO numbers are the k6 **thresholds**. Also assert downstream protection by counting
  requests received by the stub (`/__admin/requests/count`).
- **Test doubles**: hand-written fakes/stubs shared by several tests (e.g. a stub
  `HttpMessageHandler`) live in a `TestDoubles/` folder (namespace `<TestProject>.TestDoubles`) at
  the root of each test project, the only folder that does not mirror the source. Prefer a mocking
  library for one-off collaborators.
- TDD: failing test → minimal code → refactor; one PR per step.

## SLO (in README)
Sustained load (req/s) + latency p95/p99 at that load + error rate + downstream protection (upstream
calls bounded independent of traffic) + data freshness when caching. State the reference environment.
Treat the first numbers as a proposal and calibrate with the first measurement.

## CI (GitHub Actions)
- Jobs: `changes` (dorny/paths-filter with `.github/path-filters.yml`) → build & test → docker.
- Gates: format check, build with warnings as errors + analyzers, locked restore, vulnerable
  dependency audit, tests with coverage (≥ 80% lines, fail below), coverage summary to
  `$GITHUB_STEP_SUMMARY`, upload results, container build + Trivy scan (CRITICAL/HIGH).
- Separate CodeQL workflow (PR + push + weekly schedule). Dependabot for packages, actions, docker.
- Scheduled load-test workflow (nightly 03:00 UTC + `workflow_dispatch` with rate/duration),
  report to run summary, artifacts uploaded.
- `permissions: contents: read` by default, `concurrency` with cancel-in-progress, timeouts.

## Pitfalls learned
- **Never use workflow-level `paths:` filters on workflows with required checks**: skipped workflows
  never report and PRs block forever. Use job-level `if:` from a `changes` job; skipped jobs count as passed.
- A job with `needs:` on a skipped job is skipped too: use `if: !failure() && !cancelled() && ...`.
- Default test-results directories differ between SDK versions: always pass an explicit results
  directory and unique per-project coverage file names.
- The k6 image runs non-root: create the results bind-mount dir with `install -d -m 777` on Linux.
- k6 skips the HTML dashboard export for very short runs.
- Many parallel TLS connections to third-party APIs can fail: bound outgoing concurrency.
- A test project with zero tests may fail the run (MTP exit code 8).

## Local gate
Versioned `.githooks/pre-push` running the same checks as CI (format, build, tests, coverage),
enabled automatically (`git config core.hooksPath .githooks` from the build/install step).

## GitHub repository
- Rulesets need a public repo (or paid plan) for private repos.
- Ruleset on `~DEFAULT_BRANCH`: deletion, non_fast_forward, required_linear_history, pull_request
  (0 approvals for solo repos, thread resolution), required_status_checks (strict, GitHub Actions
  integration id 15368, `do_not_enforce_on_create: true`). Keep the JSON in `.github/rulesets/`.
- Enable secret scanning + push protection, Dependabot alerts and security updates.

## Docker
Multi-stage; restore layer from manifests/lock files first; minimal non-root runtime (e.g. chiseled
for .NET, distroless for Node); `.dockerignore` excluding tests, git and build outputs.
