# `pr-path-labels.yml`

Reusable workflow that labels pull requests from the files they change, using
[`actions/labeler`](https://github.com/actions/labeler). Pair it with
[`pr-title-labels.yml`](pr-title-labels.md), which labels from the title; the
two manage different labels and can run side by side.

| Changed files | Labels (with the example config below) |
|---|---|
| `docs/setup.md` | `documentation` |
| `src/api/client.ts`, `README.md` | `area: api`, `documentation` |
| `package-lock.json` only | none |

The rules live in a labeler config: `.github/labeler.yml` in your repo by
default, read from the **base branch** (a PR cannot change the rules it is
labelled by), or inline through `configuration`. See the labeler's
[match object docs](https://github.com/actions/labeler#match-object) for the
full format, including branch-name rules.

| Input | Default | Purpose |
|---|---|---|
| `configuration-path` | `.github/labeler.yml` | Path of the labeler config in the calling repo. Ignored when `configuration` is set |
| `configuration` | `''` | Inline labeler config (YAML), used instead of `configuration-path` |
| `sync-labels` | `false` | Remove config-defined labels whose rules no longer match (e.g. after the files are reverted). Labels not in the config are never touched |
| `dot` | `true` | Let globs like `**` match paths that start with a dot (`.github/`) |
| `runs-on` | `ubuntu-latest` | Runner label |
| `timeout-minutes` | `15` | Job timeout in minutes |
| `cancel-superseded` | `true` | Cancel an in-flight run when a newer one starts for the same pull request. PR events only; see [Cancel superseded runs](../README.md#cancel-superseded-runs) |

| Output | Purpose |
|---|---|
| `new-labels` | Comma-separated labels this run added |
| `all-labels` | Comma-separated labels the PR has after this run |

No secrets required. The workflow's own token is used and needs
`contents: read` (to read the config) and `pull-requests: write`. Labels that
don't exist yet are created with GitHub's default colour.

## Example

```yaml
# .github/workflows/pr-labels.yml
on:
  pull_request_target:
    types: [opened, synchronize, reopened]
jobs:
  labels:
    uses: tibor-horvath/ci-toolkit/.github/workflows/pr-path-labels.yml@v1
    with:
      sync-labels: true
    permissions:
      contents: read
      pull-requests: write
```

```yaml
# .github/labeler.yml
documentation:
  - changed-files:
      - any-glob-to-any-file: ["docs/**", "**/*.md"]

"area: api":
  - changed-files:
      - any-glob-to-any-file: "src/api/**"
```

A single rule inline, without a config file:

```yaml
jobs:
  labels:
    uses: tibor-horvath/ci-toolkit/.github/workflows/pr-path-labels.yml@v1
    with:
      configuration: |
        documentation:
          - changed-files:
              - any-glob-to-any-file: ["docs/**", "**/*.md"]
    permissions:
      contents: read
      pull-requests: write
```

`pull_request_target` is safe here because nothing from the PR is checked out
or run, and it gives fork PRs a token that can write labels. With plain
`pull_request`, fork PRs get a read-only token and the labelling fails.
