# `nuget-publish.yml`

Reusable NuGet pack + push. Packs once and pushes every resulting package with
`--skip-duplicate` (re-runs are idempotent). Mark non-package projects with
`<IsPackable>false</IsPackable>` so only real packages publish.

| Input | Default | Purpose |
|---|---|---|
| `dotnet-version` | `10.0.x` | SDK version to install |
| `project` | `''` | sln/project to pack. Empty → root `.sln`/`.slnx` |
| `configuration` | `Release` | Build configuration |
| `version` | `''` | Package version. Empty → release tag with leading `v` stripped |
| `nuget-source` | nuget.org | Feed to push to |
| `nuget-user` | `''` | nuget.org profile name for Trusted Publishing. Set → OIDC login instead of `nuget-api-key` |
| `include-symbols` | `false` | Also pack + push `.snupkg` |
| `runs-on` | `ubuntu-latest` | Runner label |
| `timeout-minutes` | `60` | Job timeout in minutes |

Typically triggered on `release: published`.

## Authentication

**Trusted Publishing (recommended).** Set `nuget-user`; the job exchanges a
GitHub OIDC token for a 1-hour API key via
[`NuGet/login`](https://github.com/NuGet/login), so no secret is stored. On
nuget.org → your username → **Trusted Publishing**, add a policy with the
repository owner, repository name and the **caller's** workflow file name
(e.g. `publish-nuget.yml`, file name only).

**API key.** Pass the `nuget-api-key` secret and leave `nuget-user` empty.
nuget.org now discourages long-lived keys for CI, and they expire.

Either way the job requests `id-token: write`, so the calling job must grant it
(a reusable workflow cannot receive more permissions than its caller gives).

## Outputs

| Output | Purpose |
|---|---|
| `version` | The version actually packed |
| `packages` | Comma-separated `.nupkg` filenames that were packed and pushed |

`version` is worth reading back rather than assuming: when the `version` input is
empty it is derived from the release tag, so the caller does not know it up front.

```yaml
jobs:
  publish:
    permissions:
      contents: read
      id-token: write
    uses: tibor-horvath/ci-toolkit/.github/workflows/nuget-publish.yml@v2
    with:
      nuget-user: ${{ vars.NUGET_USER }}

  announce:
    needs: publish
    runs-on: ubuntu-latest
    steps:
      - run: echo "Shipped ${{ needs.publish.outputs.packages }} at ${{ needs.publish.outputs.version }}"
```

## Example

```yaml
on:
  release:
    types: [published]
permissions:
  contents: read
jobs:
  publish:
    permissions:
      contents: read
      id-token: write
    uses: tibor-horvath/ci-toolkit/.github/workflows/nuget-publish.yml@v2
    with:
      nuget-user: ${{ vars.NUGET_USER }}
```
