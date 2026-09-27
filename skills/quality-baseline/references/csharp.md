# C# / .NET baseline (Microsoft conventions)

Templates: `../templates/csharp/` (verified in CI). Adapt names and versions.

## Solution
- Latest .NET LTS/STS requested; `.slnx` solution; `src/` and `tests/`.
- Naming: `Company.Product.Component` projects; tests `<Project>.UnitTests`,
  `<Project>.ComponentTests`, `<Project>.LoadTests`.
- Web APIs: **Minimal APIs** with route groups (`MapXxxApi()` extension methods), `TypedResults`,
  built-in OpenAPI, `ProblemDetails`. Folder layout as Microsoft eShop services:
  `Apis/`, `BackgroundServices/`, `Extensions/`, `Infrastructure/<Dependency>/`, `Models/`,
  `Services/`, `Program.cs`. Tests mirror these folders and namespaces.
- Typed `HttpClient` + `Microsoft.Extensions.Http.Resilience` (`AddStandardResilienceHandler`),
  options with validation on start, `HybridCache` for caching, `TimeProvider` for time,
  `LoggerMessage` source-generated logging, health checks (live/ready).
- Console apps / scheduled jobs: Generic Host (`Host.CreateApplicationBuilder`) with the same
  options validation, typed clients and logging; exit codes documented in the README.

## Build configuration
- `global.json`: SDK with `rollForward: latestFeature`; `"test": { "runner": "Microsoft.Testing.Platform" }`.
- `Directory.Build.props`: TargetFramework, Nullable, ImplicitUsings, `TreatWarningsAsErrors`,
  `AnalysisLevel latest-recommended`, `EnforceCodeStyleInBuild`, `GenerateDocumentationFile`
  (needed for IDE0005) with `NoWarn CS1591`, NuGet audit (`all`, `low`), lock files +
  `RestoreLockedMode` in CI, deterministic/CI build; test-project group (`OutputType Exe`, unique
  `--coverage-output $(MSBuildProjectName).cobertura.xml`); target that sets `core.hooksPath`
  (only one project, not in CI — parallel builds otherwise race on `.git/config`).
- `Directory.Packages.props`: Central Package Management + transitive pinning; no `Version` on
  `PackageReference`.
- `.editorconfig`: start from `dotnet new editorconfig` (Microsoft defaults), add charset/LF/final
  newline, raise key IDE/CA rules to warning, relax CA1707/CA1515 etc. under `tests/**`.
- CodeQL: see the SARIF filter for `obj/**` in `templates/csharp/.github/workflows/codeql.yml`.
- `dotnet-tools.json` with ReportGenerator; `build/coverage.sh` merges Cobertura and enforces the threshold.

## Tests
xUnit v3 (`xunit.v3.mtp-v2`), NSubstitute (+ analyzers), AwesomeAssertions (FluentAssertions is
commercial), WireMock.Net, `Microsoft.AspNetCore.Mvc.Testing` (`WebApplicationFactory<Program>`),
`Microsoft.Extensions.TimeProvider.Testing`, `Microsoft.Testing.Extensions.CodeCoverage`.
Run: `dotnet test --coverage --coverage-output-format cobertura --results-directory artifacts/TestResults`.

## Migrating an existing repo
- xUnit v2 → `xunit.v3.mtp-v2`: drop `Microsoft.NET.Test.Sdk`, `xunit.runner.visualstudio` and
  coverlet; custom `FactAttribute`s need a constructor forwarding `[CallerFilePath]`/`[CallerLineNumber]`
  (xUnit3003).
- Run `dotnet format` once and commit it apart from behaviour changes; keep process-culture code
  (e.g. a fixed `es-ES`) out of `InvariantGlobalization`.
- When coverage starts below the threshold, measure and publish first (threshold 0 in
  `build/coverage.sh`) and raise it to 80% in the PR that adds the missing tests.

## Docker
SDK image build stage with `CI=true` and restore from csproj + `packages.lock.json`; runtime
`mcr.microsoft.com/dotnet/aspnet:<ver>-noble-chiseled`, `USER $APP_UID`, port 8080.
