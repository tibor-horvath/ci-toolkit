# `lighthouse-ci.yml`

Builds the app, serves the build output with Lighthouse CI's static server, audits it, and
fails if a category score falls below your minimum. Reports are kept as a workflow artifact.

| Input | Default | Purpose |
|---|---|---|
| `min-performance` | `''` | Minimum score, 0 to 1. Empty → not asserted |
| `min-accessibility` | `''` | Minimum score, 0 to 1. Empty → not asserted |
| `min-best-practices` | `''` | Minimum score, 0 to 1. Empty → not asserted |
| `min-seo` | `''` | Minimum score, 0 to 1. Empty → not asserted |
| `config-path` | `''` | Your own `lighthouserc`, for budgets and per-audit assertions. Overrides the `min-*` inputs |
| `number-of-runs` | `3` | Audits per page; the median is used. Generated config only |
| `lhci-version` | `0.15.1` | `@lhci/cli` version, pinned so a release cannot shift scores |
| `build-script` | `build` | Script that produces the build |
| `build-output-dir` | `dist` | Directory served for the audit |
| `build-env` | `''` | Newline-separated `KEY=VALUE` for the build. Public values only |
| `package-manager` | `''` | `npm`, `pnpm` or `yarn`. Empty → detected from the lockfile |
| `pnpm-version` | `''` | pnpm version. Empty → the `packageManager` field |
| `node-version` / `node-version-file` | `22.x` / `''` | Node version |
| `working-directory` | `.` | Folder with `package.json` and the lockfile |
| `install-command` | `''` | Override the dependency install |
| `artifact-retention-days` | `7` | Retention for the report artifact |
| `runs-on` | `ubuntu-latest` | Runner label |

| Secret | Purpose |
|---|---|
| `npm-token` | Optional registry auth, exposed as `NODE_AUTH_TOKEN` during install |

Needs only `permissions: { contents: read }`. With no `min-*` input and no `config-path`, it
still runs and uploads reports but asserts nothing, so it can never fail.

## Usage

```yaml
jobs:
  lighthouse:
    uses: tibor-horvath/ci-toolkit/.github/workflows/lighthouse-ci.yml@v1
    with:
      min-performance: "0.8"
      min-accessibility: "0.9"
    permissions:
      contents: read
```

Budgets or per-audit rules need a config file:

```json
{
  "ci": {
    "assert": {
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.85 }],
        "unused-javascript": ["warn", { "maxNumericValue": 100000 }]
      }
    }
  }
}
```

```yaml
    with:
      config-path: lighthouserc.json
```

## Notes

- **Cancel superseded runs.** Set `concurrency:` in your calling workflow; see
  [Cancel superseded runs](../README.md#cancel-superseded-runs).
- **Reports stay private.** The upload target is forced to the local filesystem, even with
  your own config. Lighthouse's `temporary-public-storage` would publish the report at a
  public URL, which is wrong for a private repo. Download the `lighthouse-reports` artifact
  to read the HTML reports.
- **It audits the static build, not a deployed URL.** Good for catching regressions before
  merge. It does not see your CDN, headers or backend latency, so treat performance scores
  as relative: compare them against earlier runs, not against a production PageSpeed result.
- **Scores vary between runs.** Three runs and the median steady them, but set minimums
  with some margin or the job will fail intermittently.
- **Single-page apps.** The static server finds the pages in the output directory, so a
  client-routed app is audited at its entry page, not at each route. List routes in a
  custom config with `collect.url` if you need more.
