# `pr-title-lint.yml`

Reusable check that pull request titles follow
[Conventional Commits](https://www.conventionalcommits.org/). With squash merges
the PR title becomes the commit message, which is what release-please reads to
choose the version bump — a malformed title means a missed or wrong release.

| Input | Default | Purpose |
|---|---|---|
| `types` | `''` | Newline-separated allowed types. Empty → the Conventional Commits defaults |
| `scopes` | `''` | Newline-separated allowed scopes. Empty → any |
| `require-scope` | `false` | Fail when the title has no `(scope)` |
| `subject-pattern` | `''` | Regex the subject must match. Empty → any |
| `runs-on` | `ubuntu-latest` | Runner label |

No secrets required (the workflow's own token is used, read-only).

## Example

```yaml
on:
  pull_request_target:
    types: [opened, edited, synchronize, reopened]
jobs:
  title:
    uses: tibor-horvath/ci-toolkit/.github/workflows/pr-title-lint.yml@v1
    permissions:
      pull-requests: read
```

`pull_request_target` is safe here: the action reads only the title from the
event payload and never checks out or runs PR code. It also makes the check work
on fork PRs. Include `edited` so fixing the title re-runs the check.
