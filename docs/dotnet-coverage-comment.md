# `dotnet-coverage-comment.yml`

Posts a code-coverage summary as a sticky pull-request comment. It reads the
`coverage*` artifacts that [`dotnet-build-test.yml`](dotnet-build-test.md) uploads,
merges them (sharded runs included) with ReportGenerator, summarises the result
and updates a single comment on the PR. All third-party actions are SHA-pinned.

| Input | Default | Purpose |
|---|---|---|
| `dotnet-version` | `10.0.x` | SDK version to install |
| `thresholds` | `60 80` | Line-rate thresholds `<red-below> <green-from>` (percent) |
| `fail-below-min` | `false` | Fail the job when line coverage is below the lower threshold |
| `runs-on` | `ubuntu-latest` | Runner label |
| `timeout-minutes` | `15` | Job timeout in minutes |
| `cancel-superseded` | `true` | Cancel an in-flight run when a newer one starts for the same pull request. PR events only; see [Cancel superseded runs](../README.md#cancel-superseded-runs) |

The calling job must grant `permissions: { contents: read, pull-requests: write }`.
No secrets required.

## Example

```yaml
on:
  pull_request:
jobs:
  dotnet:
    uses: tibor-horvath/ci-toolkit/.github/workflows/dotnet-build-test.yml@v1
    with:
      runsettings: "coverlet.runsettings"
    permissions:
      checks: write
      contents: read

  coverage:
    needs: dotnet
    uses: tibor-horvath/ci-toolkit/.github/workflows/dotnet-coverage-comment.yml@v1
    permissions:
      contents: read
      pull-requests: write
```

The job only runs on `pull_request` events, so the caller needs no `if:` — on a
push it is simply skipped.

## Notes

- **Why a separate workflow, not a `dotnet-build-test` input.** Commenting needs
  `pull-requests: write`. A reusable workflow that requests a permission its caller
  did not grant fails at startup, even if the job is skipped, so adding it to
  `dotnet-build-test` would break every existing caller.
- **Needs coverage.** `dotnet-build-test` must run with `collect-coverage: true`
  (the default); with no `coverage*` artifact the download step fails.
- **Fork PRs are skipped.** Their token is read-only, so the comment could not be
  posted.
- **Informational by default.** The thresholds only colour the indicators; set
  `fail-below-min: true` to make low coverage fail the job.
