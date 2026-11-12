# `pr-title-labels.yml`

Reusable workflow that labels pull requests from their
[Conventional Commit](https://www.conventionalcommits.org/) title, so you can
filter PRs by type and group them in GitHub's
[generated release notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes).

| Title | Labels (defaults) |
|---|---|
| `feat: add retry option` | `type: feat` |
| `fix(api)!: drop v1 endpoints` | `type: fix`, `breaking-change` (+ `scope: api` with `scope-labels: true`) |
| `chore: bump deps` with a `BREAKING CHANGE:` footer in the PR body | `type: chore`, `breaking-change` |
| `Update stuff` (not a Conventional Commit) | unchanged |

When the title is edited, labels the workflow manages that no longer match are
removed, so retitling `fix:` to `feat:` swaps `type: fix` for `type: feat`.
"Managed" means: names starting with `type-label-prefix`, the label names in
`type-labels`, `breaking-label`, and (with `scope-labels`) names starting with
`scope-label-prefix`. Every other label, including release-please's
`autorelease: *`, is left alone.

| Input | Default | Purpose |
|---|---|---|
| `types` | `''` | Newline-separated types that get a type label (`feat`, `fix`). Others get none. Empty → every type |
| `type-label-prefix` | `type: ` | Prefix for type labels: `feat` → `type: feat` |
| `type-labels` | `''` | Newline-separated `type=label` overrides (`feat=enhancement`). `chore=` skips a type |
| `breaking-label` | `breaking-change` | Label for `type!:` titles or a `BREAKING CHANGE:` body footer. Empty → none |
| `scope-labels` | `false` | Also add a label for the title's `(scope)` (comma-separated scopes each get one) |
| `scope-label-prefix` | `scope: ` | Prefix for scope labels |
| `runs-on` | `ubuntu-latest` | Runner label |
| `timeout-minutes` | `15` | Job timeout in minutes |
| `cancel-superseded` | `true` | Cancel an in-flight run when a newer one starts for the same pull request. PR events only; see [Cancel superseded runs](../README.md#cancel-superseded-runs) |

No secrets required. The workflow's own token is used and needs
`pull-requests: write`. Labels that don't exist yet are created with GitHub's
default colour; create them yourself first if you want specific colours or
descriptions.

## Example

```yaml
on:
  pull_request_target:
    types: [opened, edited, reopened]
jobs:
  labels:
    uses: tibor-horvath/ci-toolkit/.github/workflows/pr-title-labels.yml@v1
    permissions:
      pull-requests: write
```

Labelling only the types that matter for release notes:

```yaml
jobs:
  labels:
    uses: tibor-horvath/ci-toolkit/.github/workflows/pr-title-labels.yml@v1
    with:
      types: |
        feat
        fix
        perf
    permissions:
      pull-requests: write
```

A `chore:` PR then gets no type label (it still gets `breaking-change` if it
is one), and retitling `feat:` to `chore:` removes `type: feat`.

Mapping types to GitHub's default labels instead of `type: *`:

```yaml
jobs:
  labels:
    uses: tibor-horvath/ci-toolkit/.github/workflows/pr-title-labels.yml@v1
    with:
      type-labels: |
        feat=enhancement
        fix=bug
        docs=documentation
    permissions:
      pull-requests: write
```

Types without an override still get `type-label-prefix` + type. Set
`type-label-prefix: ""` with overrides only if you want *just* the mapped types,
but then add an override for every type you use, since an empty prefix makes
the bare type name (`chore`) the label.

`pull_request_target` is safe here: the script reads only the title and body
from the event payload and never checks out or runs PR code. It also gives fork
PRs a token that can write labels (with `pull_request`, fork PRs get a
read-only token and the job fails). Include `edited` so retitling re-labels.

## Why it isn't part of `pr-title-lint.yml`

A reusable workflow that asks for more permissions than its caller grants fails
to start. The lint only needs `pull-requests: read`; adding labelling there
would break every existing caller. Run both side by side instead:

```yaml
jobs:
  title:
    uses: tibor-horvath/ci-toolkit/.github/workflows/pr-title-lint.yml@v1
    permissions: { pull-requests: read }
  labels:
    uses: tibor-horvath/ci-toolkit/.github/workflows/pr-title-labels.yml@v1
    permissions: { pull-requests: write }
```
