# Cross-language baseline

## Tests
- **Unit**: fast, isolated, mocks for collaborators. Folder/namespace mirrors source; one test
  class/file per unit; names `Method_Scenario_ExpectedResult` (or the language idiom).
- **Component**: run the service in-process, stub every external HTTP dependency (WireMock or
  equivalent). Never call real third-party APIs from tests.
- **Load**: k6 against the container with dependencies stubbed (WireMock with latency), via Docker
  Compose, in `tests/<Project>.LoadTests/`. The SLO numbers are the k6 **thresholds**. `setup()`
  waits on the readiness endpoint (`/health/ready`) so the run measures steady state. Also assert
  downstream protection by counting requests received by the stub (`/__admin/requests/count`).
  For a batch job/CLI, run the job against stubs with a representative volume and assert duration
  per run and number of downstream calls instead of HTTP percentiles.
- **Test doubles**: hand-written fakes/stubs shared by several tests (e.g. a stub
  `HttpMessageHandler`) live in a `TestDoubles/` folder (namespace `<TestProject>.TestDoubles`) at
  the root of each test project, the only folder that does not mirror the source. Prefer a mocking
  library for one-off collaborators.
- TDD: failing test → minimal code → refactor; one PR per step.

## Runtime production practices
Cross-language baseline for the code itself, independent of CI gates:
- **Config validation**: parse and validate configuration/env vars at startup; fail fast with a
  clear error instead of failing lazily on first use.
- **Observability**: structured logging (not string concatenation) carrying a
  request/correlation id through the call chain; log levels used consistently (no `info` for
  errors or vice versa); no secrets/PII in logs.
- **Resilience on outbound calls**: explicit timeout, retry (bounded, with backoff) and circuit
  breaker/concurrency limit on every call to an external dependency — this is what the SLO's
  downstream-protection requirement is actually implemented with.
- **Input validation at boundaries**: parse and validate every external input (HTTP request,
  message payload, CLI arg) against a schema before using it; never trust `any`/untyped data past
  the boundary.
- **Health checks**: every long-running service exposes liveness (`/health/live`: the process
  responds) and readiness (`/health/ready`: dependencies reachable, warm-up done, e.g. cache
  primed). The load test's `setup()` waits on readiness.
- **Graceful shutdown**: on `SIGTERM`, stop accepting new work, drain in-flight requests/messages
  within a bounded timeout, close connections, then exit — so deploys and container restarts
  don't surface as errors.

## SLO (in README)
Every repo has one, adapted to the kind of project:
- HTTP service: sustained load (req/s) + latency p95/p99 at that load + error rate + downstream
  protection (upstream calls bounded independent of traffic) + data freshness when caching.
- Batch job/CLI: duration per run at a stated volume + error rate + downstream protection (calls
  and rate towards each dependency bounded).
State the reference environment. Treat the first numbers as a proposal and **calibrate**: run the
load test at several rates (e.g. 0.5×, 1×, 2×, 4× the proposal) on the reference runner, find the
saturation point and set the sustained objective well below it (≈ half), documenting the runs in
the README.

## CI (GitHub Actions)
- Jobs: `changes` (dorny/paths-filter with `.github/path-filters.yml`) → build & test → docker.
- Gates: format check, build with warnings as errors + analyzers, locked restore, vulnerable
  dependency audit, tests with coverage (≥ 80% lines, fail below), coverage summary to
  `$GITHUB_STEP_SUMMARY`, upload results, container build + Trivy scan (CRITICAL/HIGH).
- Separate CodeQL workflow (PR + push + weekly schedule). Dependabot for packages, actions, docker,
  each with `cooldown` (e.g. 7 days) so a just-published — possibly compromised — version isn't
  proposed immediately.
- Pin third-party actions by full commit SHA with the version in a comment
  (`uses: owner/action@<sha> # v1.2.3`): a tag can be moved to malicious code, a SHA cannot.
  Dependabot keeps SHA pins up to date. GitHub-owned actions (`actions/*`, `github/*`) may stay on
  major tags.
- Load-test workflow with `workflow_dispatch` (rate/duration inputs), report to run summary,
  artifacts uploaded. Run it on demand after relevant changes; a nightly schedule is optional per
  project (worth it for actively changing services).
- CodeQL also has `workflow_dispatch` to re-analyze the default branch on demand.
- OS matrix (`ubuntu-latest`, `windows-latest`, `macos-latest`, `fail-fast: false`) for the test job
  when the project claims cross-platform support; keep coverage/docker jobs on Linux.
- `permissions: contents: read` by default, `concurrency` with cancel-in-progress, timeouts.

## Pitfalls learned
- **Never use workflow-level `paths:` filters on workflows with required checks**: skipped workflows
  never report and PRs block forever. Use job-level `if:` from a `changes` job; skipped jobs count as passed.
- A matrix job skipped by its `if:` reports its check with the unexpanded name (`Tests (${{ matrix.os }})`),
  which never matches a required check: use one explicit job per OS for required checks.
- A job with `needs:` on a skipped job is skipped too: use `if: !failure() && !cancelled() && ...`.
- Default test-results directories differ between SDK versions: always pass an explicit results
  directory and unique per-project coverage file names.
- The k6 image runs non-root: create the results bind-mount dir with `install -d -m 777` on Linux.
- k6 skips the HTML dashboard export for very short runs.
- Many parallel TLS connections to third-party APIs can fail: bound outgoing concurrency.
- A test project with zero tests may fail the run (MTP exit code 8).
- CodeQL with a manual build analyzes source-generated code under `obj/` and `paths-ignore` does not
  apply: analyze with `upload: failure-only`, filter the SARIF (`advanced-security/filter-sarif`,
  `-**/obj/**`) and upload it with `codeql-action/upload-sarif`.

## Repository docs and Claude settings
- **README is the single source of truth**: *At a glance* first (one-command run, what it does,
  measured SLO, quality summary with links), then requirements, how to run (with URLs), how to test,
  structure, development conventions (incl. AI-assisted development note), design, SLO +
  calibration, load test, assumptions, enhancements, quality gates (local vs CI table).
- Repo `CLAUDE.md`: a table pointing to README sections + Claude-only rules (TDD, run the local
  gate before finishing, keep SLO and k6 thresholds in sync) + the repo's **push/merge policy**
  (who may push which branches and whether agents may merge; omitted = ask before every push) +
  any overrides of the personal baseline, with the reason.
- **Decision log**: `docs/decisions/` with ADRs in MADR format and an index `README.md`, linked from
  the repo README (design section). Brownfield audit: propose retroactive ADRs for the main past
  decisions. Format and process: the `adr` skill.
- Repo `CLAUDE.md` says that designs are recorded as ADRs proposed via PR.
- Versioned `.claude/settings.json`: `allow` build/test/format/coverage/local gate and read-only
  git (`status`, `diff`, `log`); `ask` for `git push` unless the repo's push policy allows it
  (e.g. repos running the autonomous GitHub workflow allow pushes to `issue-*` branches — set up by
  `github-workflow-setup`).

## Local gate
Versioned `.githooks/pre-push` running the same checks as CI (locked restore, vulnerable
dependencies, format, build, tests, coverage), enabled automatically (`git config core.hooksPath
.githooks` from the build/install step). CodeQL, the container scan and the load test stay CI-only.
A locked restore fails when a lock file is stale: update it deliberately (`dotnet restore
--force-evaluate`, `pnpm install`) and commit it.

## GitHub repository
- Rulesets need a public repo (or paid plan) for private repos.
- Ruleset on `~DEFAULT_BRANCH`: deletion, non_fast_forward, required_linear_history, pull_request
  (0 approvals for solo repos, thread resolution), required_status_checks (strict, GitHub Actions
  integration id 15368, `do_not_enforce_on_create: true`). Keep the JSON in `.github/rulesets/`.
- Enable secret scanning + push protection, Dependabot alerts and security updates.

## Docker
Multi-stage; restore layer from manifests/lock files first; minimal non-root runtime (e.g. chiseled
for .NET, distroless for Node); `.dockerignore` excluding tests, git and build outputs.
