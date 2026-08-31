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
| `test-summary` | `false` | Sum the trx counters into workflow outputs. Adds one job — see [Outputs](#outputs) |
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

Off by default. Set `test-summary: true` to populate them.

| Output | Purpose |
|---|---|
| `tests-total` | Total tests across every shard |
| `tests-passed` | Passed tests across every shard |
| `tests-failed` | Failed tests across every shard |
| `tests-skipped` | Tests reported as `notExecuted` across every shard |
| `tests-outcome` | `passed`, `failed`, or `no-tests` when no trx was produced |

**Why this costs a job.** Matrix job outputs are last-writer-wins: whichever
shard finishes last overwrites the rest, nondeterministically. Shards therefore
cannot report totals themselves. Each uploads its trx instead, and a `Test
Totals` job sums them once the matrix is done. That is a billed minute per run,
which is why it is opt-in rather than always on — and why leaving it off means
one extra *skipped* job in the run graph.

The totals job runs under `always()`, so a failing shard still contributes its
counts rather than silently reporting zero failures.

```yaml
jobs:
  dotnet:
    name: .NET
    uses: tibor-horvath/ci-toolkit/.github/workflows/dotnet-build-test.yml@v1
    with:
      test-matrix: '["unit","integration"]'
      test-summary: true
    permissions:
      checks: write
      contents: read

  notify:
    needs: dotnet
    if: ${{ needs.dotnet.outputs.tests-failed != '0' }}
    runs-on: ubuntu-latest
    steps:
      - run: echo "${{ needs.dotnet.outputs.tests-failed }} of ${{ needs.dotnet.outputs.tests-total }} failed"
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
