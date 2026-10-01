# `dependency-review.yml`

Reusable dependency review for pull requests. Fails the PR if it adds or bumps a
dependency to a version with a known vulnerability, or to one under a
disallowed licence. Only what the PR changes is judged, so existing debt does
not fail unrelated PRs — pair it with `node-audit.yml` or
`dotnet-vulnerable-packages.yml` on a schedule for that.

Works for every ecosystem in the GitHub dependency graph (npm, NuGet, pip,
Maven, Docker, Actions, …). On non-PR events the job is skipped.

| Input | Default | Purpose |
|---|---|---|
| `fail-on-severity` | `high` | Lowest severity that fails: `low`, `moderate`, `high`, `critical` |
| `deny-licenses` | `''` | Comma-separated SPDX licences to reject |
| `allow-licenses` | `''` | Comma-separated SPDX allowlist; cannot be combined with `deny-licenses` |
| `comment-summary` | `on-failure` | PR comment with the findings: `never`, `on-failure`, `always` |
| `runs-on` | `ubuntu-latest` | Runner label |
| `timeout-minutes` | `15` | Job timeout in minutes |
| `cancel-superseded` | `true` | Cancel an in-flight run when a newer one starts for the same pull request. PR events only; see [Cancel superseded runs](../README.md#cancel-superseded-runs) |

No secrets required. Private repos need GitHub Code Security.

## Example

```yaml
on:
  pull_request:
jobs:
  deps:
    uses: tibor-horvath/ci-toolkit/.github/workflows/dependency-review.yml@v1
    with:
      deny-licenses: "GPL-3.0-only, AGPL-3.0-only"
    permissions:
      contents: read
      pull-requests: write
```

Make it a required status check in branch protection to actually gate merges.
