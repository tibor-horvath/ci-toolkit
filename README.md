# ci-toolkit

Reusable GitHub Actions workflows shared across my repos. Stack-neutral by name so
non-.NET pipelines can live here later (e.g. `node-build-test.yml`).

Pin callers to the moving major tag: **`@v1`**.

## Workflows

### `.github/workflows/dotnet-build-test.yml`

Parameterized .NET build + test (restore → build → test → trx report → coverage artifact).
All third-party actions are SHA-pinned; NuGet packages are cached.

| Input | Default | Purpose |
|---|---|---|
| `dotnet-version` | `10.0.x` | SDK version to install |
| `build-project` | `''` | sln/csproj to restore/build/test. Empty → SDK auto-discovers the root `.sln`/`.slnx` |
| `configuration` | `Release` | Build configuration |
| `run-tests` | `true` | Run `dotnet test`; set `false` for build-only repos |
| `test-matrix` | `''` | JSON array of shard tokens → runs a matrix, filtering each by `FullyQualifiedName~.<shard>.` |
| `test-filter` | `''` | Single `--filter` (ignored when `test-matrix` is set) |
| `runsettings` | `''` | Path passed to `dotnet test --settings` (e.g. coverage include filters) |
| `collect-coverage` | `true` | Collect `XPlat Code Coverage` and upload as an artifact |
| `runs-on` | `ubuntu-latest` | Runner label |

The calling job must grant `permissions: { checks: write, contents: read }` (for the
test-reporter check) and pass `secrets: inherit` if private dependencies need auth.

**Shape.** Every caller gets the same graph: a `build` job compiles **once** and
publishes its `bin`/`obj` as an artifact, then the `test` job runs
`dotnet test --no-build`. `test-matrix` fans the test job into parallel shards
(filtered by `FullyQualifiedName~.<shard>.`); empty means a single test job.
Build-only repos (`run-tests: false`) skip the test job entirely.

```
build ──▶ test                     # unsharded
build ──▶ test (unit) ∥ test (integration)   # test-matrix: '["unit","integration"]'
```

The test shards re-use the build job's NuGet cache key, so `--no-build` can resolve
package-supplied MSBuild targets without re-downloading. The compile never repeats
per shard.

### `.github/workflows/actions-consumption.yml`

Stack-agnostic. Posts a run's billable minutes — broken down **by OS and by job** —
to the job summary via the `runs/{id}/timing` and `runs/{id}/jobs` REST endpoints
(`gh api`, no extra action).

> **A run cannot measure itself.** GitHub finalizes billable time only *after* a run
> completes, so calling this as a job *inside* the run reports all zeros. Trigger it on
> the **completed** run with a `workflow_run` workflow (see below) and pass that run's id.

> The per-OS millisecond figures are raw runtime. GitHub applies billing multipliers
> (Linux 1× · Windows 2× · macOS 10×) at invoice time — not reflected in the table.

**Optional account balance.** Pass a `billing_token` secret (a PAT — classic with
`user` scope, or fine-grained with account **Plan: read-only**) to also report
account-level **used / included / remaining** minutes. The built-in `GITHUB_TOKEN`
can't read billing, so the section is skipped when no token is supplied:

```yaml
jobs:
  report:
    uses: tibor-horvath/ci-toolkit/.github/workflows/actions-consumption.yml@v1
    with:
      run-id: ${{ github.event.workflow_run.id }}
    secrets:
      billing_token: ${{ secrets.BILLING_TOKEN }}
    permissions:
      actions: read
```

## Caller examples

**Build + sharded tests:**

```yaml
jobs:
  ci:
    uses: tibor-horvath/ci-toolkit/.github/workflows/dotnet-build-test.yml@v1
    with:
      dotnet-version: "10.0.x"
      test-matrix: '["unit","integration"]'
    secrets: inherit
    permissions:
      checks: write
      contents: read
```

**Consumption report (separate workflow, fires after the CI run finishes):**

```yaml
# .github/workflows/ci-consumption.yml
name: CI Consumption
on:
  workflow_run:
    workflows: ["CI"] # must match the measured workflow's `name:`
    types: [completed]
permissions:
  actions: read
jobs:
  report:
    uses: tibor-horvath/ci-toolkit/.github/workflows/actions-consumption.yml@v1
    with:
      run-id: ${{ github.event.workflow_run.id }}
    permissions:
      actions: read
```

**Build-only (no test project):**

```yaml
jobs:
  ci:
    uses: tibor-horvath/ci-toolkit/.github/workflows/dotnet-build-test.yml@v1
    with:
      dotnet-version: "9.0.x"
      run-tests: false
    permissions:
      checks: write
      contents: read
```

**Coverage with a runsettings filter:**

```yaml
jobs:
  ci:
    uses: tibor-horvath/ci-toolkit/.github/workflows/dotnet-build-test.yml@v1
    with:
      dotnet-version: "10.0.x"
      runsettings: "coverlet.runsettings"
    permissions:
      checks: write
      contents: read
```

## Versioning

Releases are cut as `vX.Y.Z` with a moving `vX` tag that consumers pin to. To ship a fix:

```bash
git tag v1.0.1 && git push origin v1.0.1
git tag -f v1 v1.0.1 && git push -f origin v1
```
