# `node-audit.yml`

Checks the lockfile against the registry's advisory database using the package manager's
own audit command (`npm audit`, `pnpm audit`, `yarn audit` / `yarn npm audit`). It audits
from the lockfile alone, so there is no install and no dependency cache: one fast job.

| Input | Default | Purpose |
|---|---|---|
| `audit-level` | `high` | Lowest severity that fails: `low`, `moderate`, `high`, `critical` |
| `production-only` | `true` | Audit runtime dependencies only. Set `false` to include devDependencies |
| `fail-on-findings` | `true` | `false` makes it advisory: findings are logged as a warning and the job passes |
| `package-manager` | `''` | `npm`, `pnpm` or `yarn`. Empty → detected from the lockfile |
| `pnpm-version` | `''` | pnpm version. Empty → the `packageManager` field |
| `node-version` / `node-version-file` | `22.x` / `''` | Node version |
| `working-directory` | `.` | Folder with `package.json` and the lockfile |
| `runs-on` | `ubuntu-latest` | Runner label |
| `timeout-minutes` | `15` | Job timeout in minutes |
| `cancel-superseded` | `true` | Cancel an in-flight run when a newer one starts for the same pull request. PR events only; see [Cancel superseded runs](../README.md#cancel-superseded-runs) |

Needs only `permissions: { contents: read }`.

## Usage

Advisories are published without any change in your repo, so a PR-only trigger misses them.
Run it on a schedule too:

```yaml
on:
  pull_request:
  schedule:
    - cron: "0 6 * * 1"   # Mondays

jobs:
  audit:
    uses: tibor-horvath/ci-toolkit/.github/workflows/node-audit.yml@v1
    permissions:
      contents: read
```

## Notes

- **Why `production-only` defaults on.** A Vite app ships its bundle, not its
  devDependencies. An advisory in a build tool (a dev server, a bundler plugin) is rarely
  exploitable in production and would keep failing PRs. Turn it off for libraries you
  publish, or where the build runs on untrusted input.
- **Tune with `audit-level`, not by ignoring the job.** Start at `high`; raise the bar to
  `moderate` once the backlog is clear.
- **A failed audit is not always a finding.** The command also exits non-zero when it cannot
  reach the registry, which this job reports as a failure. Re-run it if the log shows a
  network error rather than an advisory.
- **Fixing.** Dependabot security updates open PRs for vulnerable packages. See
  [dependabot-node.md](dependabot-node.md).
