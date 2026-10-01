# `dotnet-vulnerable-packages.yml`

Reusable NuGet vulnerability check — the .NET counterpart of `node-audit.yml`.
Runs `dotnet list package --vulnerable` over direct and transitive packages and
fails if it finds any.

`dotnet list package` exits 0 even when it finds vulnerabilities, so the job
parses the report and decides itself. If the advisory source cannot be reached
the job also fails: a "clean" report from a failed lookup is not trustworthy.

| Input | Default | Purpose |
|---|---|---|
| `dotnet-version` | `10.0.x` | .NET SDK version to install |
| `project` | `''` | Solution or project. Empty → auto-discover the single `.sln`/`.slnx` in the root |
| `include-transitive` | `true` | Also check transitive dependencies |
| `fail-on-findings` | `true` | `false` makes it advisory: findings are logged, the job passes |
| `runs-on` | `ubuntu-latest` | Runner label |
| `timeout-minutes` | `15` | Job timeout in minutes |

No secrets required.

## Example

```yaml
on:
  pull_request:
  schedule: [{ cron: '0 6 * * 1' }]   # advisories appear without code changes
jobs:
  vulnerable:
    uses: tibor-horvath/ci-toolkit/.github/workflows/dotnet-vulnerable-packages.yml@v1
    permissions:
      contents: read
```

## If it flags something

Bump the package, or the direct dependency that pulls it in. For a transitive
one, add a direct `PackageReference` at the fixed version, or enable
[transitive pinning](https://learn.microsoft.com/nuget/consume-packages/Central-Package-Management#transitive-pinning).
