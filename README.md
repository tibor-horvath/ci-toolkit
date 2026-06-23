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

Stack-agnostic. Posts a run's Actions usage — broken down **by OS and by job** —
to the job summary. Usage is computed from each job's start/finish timestamps
(`runs/{id}/jobs`), rounded up per job × OS multiplier, because the
`runs/{id}/timing` `billable` field returns 0 on GitHub's metered billing
platform. It's a close estimate, not the invoiced figure.

> **A run cannot measure itself.** GitHub finalizes billable time only *after* a run
> completes, so calling this as a job *inside* the run reports all zeros. Trigger it on
> the **completed** run with a `workflow_run` workflow (see below) and pass that run's id.

> The per-OS millisecond figures are raw runtime. GitHub applies billing multipliers
> (Linux 1× · Windows 2× · macOS 10×) at invoice time — not reflected in the table.

**Optional account usage.** Pass a `billing_token` secret to add an account-level
Actions usage section (per-SKU minutes + net cost) from GitHub's enhanced billing
usage API. Notes:

- Must be a **classic** PAT with `Plan` read (`user` scope). The billing endpoints
  do **not** accept fine-grained PATs, and the built-in `GITHUB_TOKEN` can't read
  billing. Omit the secret to skip the section.
- The usage API reports consumption, not your allowance. Set `included-minutes` to
  your plan's monthly minutes (e.g. `2000` Free, `3000` Pro) to also show
  **remaining**. Minutes are counted allowance-equivalent (Windows 2×, macOS 10×).
- Requires an account on GitHub's enhanced/metered billing platform.

```yaml
jobs:
  report:
    uses: tibor-horvath/ci-toolkit/.github/workflows/actions-consumption.yml@v1
    with:
      run-id: ${{ github.event.workflow_run.id }}
      included-minutes: 3000
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

## Versioning & releases

Consumers pin the moving major tag `@v1`. Releases are automated with
[release-please](https://github.com/googleapis/release-please) (`release.yml`):

1. Push [Conventional Commits](https://www.conventionalcommits.org/) to `main`
   (`feat:`, `fix:`, `refactor:`, `docs:`, …).
2. release-please maintains a **release PR** that bumps the version and updates
   `CHANGELOG.md`.
3. Merging that PR tags `vX.Y.Z`, cuts a GitHub release, and the workflow
   repoints **`v1`** at it — so `@v1` consumers get the change automatically.

`feat:` bumps the minor, `fix:` the patch; a `!` or `BREAKING CHANGE:` footer
bumps the major (and you'd then advertise a `@v2` tag). See `CHANGELOG.md` for
release history.
