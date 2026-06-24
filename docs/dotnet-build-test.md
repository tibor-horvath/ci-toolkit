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

## Examples

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
