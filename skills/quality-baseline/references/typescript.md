# TypeScript / Node baseline

Not yet verified in a real repo like the C# templates: check current versions and docs when applying.

- **Runtime/tooling pinning**: `.nvmrc` / `engines`, `packageManager` field (pnpm via Corepack),
  committed lockfile, `pnpm install --frozen-lockfile` in CI.
- **tsconfig**: `strict: true`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`,
  `noImplicitOverride`, `verbatimModuleSyntax`; shared base config in monorepos.
- **Lint/format**: ESLint flat config with `typescript-eslint` strict + stylistic type-checked,
  Prettier (or Biome) with `--check` in CI; warnings fail CI (`--max-warnings 0`); `.editorconfig`.
- **Structure**: `src/` and `tests/` mirroring `src/` (or colocated `*.test.ts` if the framework
  convention says so); kebab-case files, PascalCase types, camelCase functions.
- **Tests**: Vitest (unit, coverage via v8 with thresholds ≥ 80%), component tests with the app
  in-process (e.g. supertest / Fastify inject) and HTTP deps stubbed (msw or WireMock), Playwright
  for UI, k6 load tests with SLO thresholds.
- **Gates**: typecheck (`tsc --noEmit`), lint, format check, tests + coverage, `pnpm audit`
  (high+), CodeQL `javascript-typescript`, Docker build + Trivy.
- **Local gate**: `.githooks/pre-push` (or lefthook) running typecheck, lint, format, tests.
- **Docker**: multi-stage, `node:<lts>-slim` build, distroless/`-slim` non-root runtime, `npm ci`/`pnpm` from lockfile.
- **Monorepo**: workspaces + Turborepo/Nx; one centralized config per concern (tsconfig base, eslint, prettier).

## Production runtime practices (see `common.md` for the cross-language principles)
- **Config validation**: parse `process.env` through a `zod` schema (or `envalid`) once at startup;
  throw and exit non-zero on failure instead of reading `process.env.X` ad hoc throughout the code.
- **Structured logging**: `pino` (or the framework's built-in logger, e.g. Fastify) with a
  request-id/correlation-id bound via `asyncLocalStorage` or the framework's request context;
  never `console.log` in production code.
- **Resilience on outbound calls**: `undici` with a connect/body timeout and a bounded
  `Agent`/pool, plus a retry-with-backoff wrapper (`cockatiel` or `p-retry`) and a concurrency cap
  for third-party calls; this implements the SLO's downstream-protection requirement.
- **Input validation at boundaries**: validate every request body/query/params (and message
  payloads) with a `zod` schema at the route/handler boundary; treat the parsed result, not the
  raw `unknown`/`any`, as the type used downstream.
- **Health checks**: `/health/live` and `/health/ready` endpoints (ready checks real dependency
  connectivity) for any long-running service; the load test's `setup()` waits on `/health/ready`.
- **Graceful shutdown**: on `SIGTERM`, stop accepting new connections, drain in-flight requests,
  close DB/queue connections, then exit.
