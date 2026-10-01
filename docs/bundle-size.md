# `bundle-size.yml`

Builds the PR and its base commit, measures both build output directories, and posts the
difference as one PR comment that is updated in place. It measures whatever your build
script writes to `build-output-dir`, so it works with any bundler, not only Vite.

| Input | Default | Purpose |
|---|---|---|
| `max-gzip-increase-kb` | `''` | Fail when gzip size grows by more than this many KB vs the base. Empty → report only |
| `compress-extensions` | `js mjs css html svg json` | Extensions counted in the gzip total |
| `build-script` | `build` | Script that produces the build |
| `build-output-dir` | `dist` | Output directory, relative to `working-directory` |
| `build-env` | `''` | Newline-separated `KEY=VALUE` for the build. Public values only |
| `comment` | `true` | Post the PR comment. The table always goes to the job summary too |
| `package-manager` | `''` | `npm`, `pnpm` or `yarn`. Empty → detected from the lockfile |
| `pnpm-version` | `''` | pnpm version. Empty → the `packageManager` field |
| `node-version` / `node-version-file` | `22.x` / `''` | Node version |
| `working-directory` | `.` | Folder with `package.json` and the lockfile |
| `install-command` | `''` | Override the dependency install |
| `runs-on` | `ubuntu-latest` | Runner label |
| `timeout-minutes` | `60` | Job timeout in minutes |
| `cancel-superseded` | `true` | Cancel an in-flight run when a newer one starts for the same pull request. PR events only; see [Cancel superseded runs](../README.md#cancel-superseded-runs) |

| Secret | Purpose |
|---|---|
| `npm-token` | Optional registry auth, exposed as `NODE_AUTH_TOKEN` during install |

| Output | Purpose |
|---|---|
| `head-gzip-bytes` / `base-gzip-bytes` | Gzip size of the PR and base builds |
| `gzip-delta-bytes` | PR minus base. Positive means the bundle grew |

The calling job must grant `permissions: { contents: read, pull-requests: write }`. The job
only runs on `pull_request` events and is skipped otherwise.

## Usage

```yaml
on:
  pull_request:
    branches: [main]

jobs:
  size:
    uses: tibor-horvath/ci-toolkit/.github/workflows/bundle-size.yml@v1
    with:
      max-gzip-increase-kb: "25"   # drop this line to report without gating
    permissions:
      contents: read
      pull-requests: write
```

## Notes

- **Cancel superseded runs.** Built in: a newer push to the same PR cancels the
  in-flight run. Opt out with `cancel-superseded: false`; see
  [Cancel superseded runs](../README.md#cancel-superseded-runs).
- **It builds twice.** The base commit is built from scratch each run, so this job costs
  roughly two builds. Run it on PRs only, and expect it to be the slowest of the quality
  jobs. The base is installed separately, so a lockfile change in the PR is measured fairly.
- **Gzip, not raw, is the gate.** Gzip approximates what users download. Raw size is shown
  for reference. Hashed filenames change every build, so sizes are summed per directory,
  not compared file by file.
- **Forked PRs** get a read-only token, so the comment step can fail there. It is marked
  non-fatal, and the table is still in the job summary.
- **Per-chunk budgets.** To cap one specific chunk rather than the total, use
  [`size-limit`](https://github.com/ai/size-limit) as a script and run it through the
  `lint-script` of `node-build-test.yml`.
