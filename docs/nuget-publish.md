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
| `include-symbols` | `false` | Also pack + push `.snupkg` |
| `runs-on` | `ubuntu-latest` | Runner label |

Requires the `nuget-api-key` secret. Typically triggered on `release: published`.

## Example

```yaml
on:
  release:
    types: [published]
permissions:
  contents: read
jobs:
  publish:
    uses: tibor-horvath/ci-toolkit/.github/workflows/nuget-publish.yml@v1
    secrets:
      nuget-api-key: ${{ secrets.NUGET_API_KEY }}
```
