# `workflow-lint.yml`

Reusable linter for a repo's own GitHub Actions workflows — the same guard this
toolkit runs on itself in `self-check.yml`.

- **actionlint** validates workflow syntax, expressions, `needs`/`if` references
  and matrix shapes, and runs every `run:` block through shellcheck.
- **Pin check** fails any `uses:` that is not a full 40-character commit SHA.
  Local (`./`) and `docker://` references are skipped.

| Input | Default | Purpose |
|---|---|---|
| `actionlint-version` | `1.7.7` | actionlint release to install |
| `shellcheck-opts` | `''` | Passed to shellcheck via `SHELLCHECK_OPTS` (e.g. `-e SC2153`) |
| `require-pinned-actions` | `true` | Fail on unpinned third-party `uses:` |
| `runs-on` | `ubuntu-latest` | Runner label (Linux x64) |
| `timeout-minutes` | `15` | Job timeout in minutes |

No secrets required. The actionlint download is verified against the release's
checksums file.

## Example

```yaml
on:
  pull_request:
    paths: ['.github/**']
permissions:
  contents: read
jobs:
  lint:
    uses: tibor-horvath/ci-toolkit/.github/workflows/workflow-lint.yml@v1
```

The pin check also applies to the `uses:` line that calls this toolkit, so a
caller referencing `@v1` will be flagged. Pin it by SHA, or set
`require-pinned-actions: false`.
