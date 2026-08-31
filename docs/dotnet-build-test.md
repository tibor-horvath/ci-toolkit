# `dotnet-build-test.yml`

Parameterized .NET build + test (restore → build → test → trx report → coverage
artifact). All third-party actions are SHA-pinned; NuGet packages are cached.

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
| `test-report` | `false` | Aggregate trx counters and merge coverage into outputs + a job summary. Adds one job — see [Outputs](#outputs) |
| `coverage-threshold` | `0` | Fail the run below this line-coverage percentage. `0` reports without gating; any value above 0 implies `test-report` |
| `runs-on` | `ubuntu-latest` | Runner label |

The calling job must grant `permissions: { checks: write, contents: read }` (for the
test-reporter check) and pass `secrets: inherit` if private dependencies need auth.

## Shape

Every caller gets the same graph: a `build` job compiles **once** and publishes its
`bin`/`obj` as an artifact, then the `test` job runs `dotnet test --no-build`.
`test-matrix` fans the test job into parallel shards (filtered by
`FullyQualifiedName~.<shard>.`); empty means a single test job. Build-only repos
(`run-tests: false`) skip the test job entirely.

```
build ──▶ test                     # unsharded
build ──▶ test (unit) ∥ test (integration)   # test-matrix: '["unit","integration"]'
```

The test shards re-use the build job's NuGet cache key, so `--no-build` can resolve
package-supplied MSBuild targets without re-downloading. The compile never repeats
per shard.

## Outputs

Off by default. Set `test-report: true` — or any `coverage-threshold` above 0,
which implies it — to populate them.

| Output | Purpose |
|---|---|
| `tests-total` | Total tests across every shard |
| `tests-passed` | Passed tests across every shard |
| `tests-failed` | Failed tests across every shard |
| `tests-skipped` | Tests reported as `notExecuted` across every shard |
| `tests-outcome` | `passed`, `failed`, or `no-tests` when no trx was produced |
| `coverage-line-rate` | Merged line coverage, percentage to one decimal (e.g. `84.2`) |
| `coverage-branch-rate` | Merged branch coverage, percentage to one decimal |

**Why one extra job.** Matrix job outputs are last-writer-wins: whichever shard
finishes last overwrites the rest, nondeterministically, so shards cannot
aggregate anything themselves. Each uploads its trx and cobertura instead, and a
single `Test & Coverage` job reduces them once the matrix is done. Test totals
and coverage share that job deliberately — same shape, same artifacts pass, and
splitting them would cost two billed minutes and leave two skipped jobs in the
graph when disabled.

Coverage was previously collected and uploaded by default but never read by
anything. This is what consumes it: ReportGenerator merges the per-shard
cobertura files, the merged HTML/Cobertura report is uploaded as
`coverage-merged`, and the summary lands in the job summary.

ReportGenerator is installed as a .NET global tool rather than pinned as a
third-party action, keeping the trusted set to what NuGet already supplies.

The job runs under `always()`, so a failing shard still contributes its counts
rather than silently reporting zero failures.

```yaml
jobs:
  dotnet:
    name: .NET
    uses: tibor-horvath/ci-toolkit/.github/workflows/dotnet-build-test.yml@v1
    with:
      test-matrix: '["unit","integration"]'
      coverage-threshold: 80      # implies test-report
    permissions:
      checks: write
      contents: read

  notify:
    needs: dotnet
    if: ${{ needs.dotnet.outputs.tests-failed != '0' }}
    runs-on: ubuntu-latest
    steps:
      - run: |
          echo "${{ needs.dotnet.outputs.tests-failed }} of ${{ needs.dotnet.outputs.tests-total }} failed"
          echo "line coverage ${{ needs.dotnet.outputs.coverage-line-rate }}%"
```

## Check names

GitHub labels a reusable-workflow job `<calling job> / <called job>`, so the
calling job's name is the prefix on every check this workflow produces. Naming
it after the stack keeps that prefix meaningful and non-redundant:

| Calling job | Check names |
|---|---|
| `dotnet:` with `name: .NET` | `.NET / Build`, `.NET / Test (unit)`, `.NET / Test (integration)` |
| `ci:` (no name) | `ci / Build`, `ci / Test (unit)` … |

The matrix *group* header in the run graph uses the job **id** (`test`), not its
name — that is GitHub's rendering, not something this workflow sets.

These strings are the status-check names branch protection matches on, so
renaming the calling job means updating the required checks in that repo.

## Examples

**Build + sharded tests:**

```yaml
jobs:
  dotnet:
    name: .NET
    uses: tibor-horvath/ci-toolkit/.github/workflows/dotnet-build-test.yml@v1
    with:
      dotnet-version: "10.0.x"
      test-matrix: '["unit","integration"]'
    secrets: inherit
    permissions:
      checks: write
      contents: read
```

**Build-only (no test project):**

```yaml
jobs:
  dotnet:
    name: .NET
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
  dotnet:
    name: .NET
    uses: tibor-horvath/ci-toolkit/.github/workflows/dotnet-build-test.yml@v1
    with:
      dotnet-version: "10.0.x"
      runsettings: "coverlet.runsettings"
    permissions:
      checks: write
      contents: read
```
