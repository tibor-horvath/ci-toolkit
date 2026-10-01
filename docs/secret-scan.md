# `secret-scan.yml`

Reusable secret scan. Runs [gitleaks](https://github.com/gitleaks/gitleaks) over
the commits a push or pull request introduces and fails the job if it finds an
API key, token, private key or connection string — so it is caught before it
reaches the main branch.

Only the event's commit range is scanned (PR: `base..head`, push:
`before..after`), so an old leak in history does not fail every new PR. A new
branch, a force-push, a manual run, or `scan-full-history: true` scans the whole
history instead. Matches are printed redacted.

| Input | Default | Purpose |
|---|---|---|
| `config` | `''` | gitleaks config in the caller repo. Empty → `.gitleaks.toml` if present, else built-in rules |
| `scan-full-history` | `false` | Scan every reachable commit, not just the event's range |
| `gitleaks-version` | `8.28.0` | gitleaks release to install |
| `runs-on` | `ubuntu-latest` | Runner label (Linux x64) |
| `timeout-minutes` | `30` | Job timeout in minutes |
| `cancel-superseded` | `true` | Cancel an in-flight run when a newer one starts for the same pull request. PR events only; see [Cancel superseded runs](../README.md#cancel-superseded-runs) |

No secrets required. The CLI is used rather than `gitleaks-action`, which needs a
paid licence key for organisation-owned repos.

## Example

```yaml
on:
  push: { branches: [main] }
  pull_request:
permissions:
  contents: read
jobs:
  secrets:
    uses: tibor-horvath/ci-toolkit/.github/workflows/secret-scan.yml@v1
```

Make it a required status check in branch protection to actually gate merges.

## If it flags something

A leaked credential stays in git history even after the file is fixed — **rotate
it first**, then clean up. For a genuine false positive (a test fixture, an
example key), allowlist it in `.gitleaks.toml`:

```toml
[extend]
useDefault = true

[[allowlists]]
description = "Dummy keys in test fixtures"
paths = ['''tests/fixtures/.*''']
```

Or add the finding's fingerprint to a `.gitleaksignore` file at the repo root.
