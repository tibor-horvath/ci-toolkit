# `codeql.yml`

Reusable static analysis (SAST) with [CodeQL](https://codeql.github.com/). One
job per language; findings land in the repo's **Code scanning** alerts.

The default `build-mode: none` analyses C# and JavaScript/TypeScript straight
from source — no restore, build or SDK. Use `autobuild` or `manual` only for
languages that need a build (Java, C/C++).

| Input | Default | Purpose |
|---|---|---|
| `languages` | `["javascript-typescript"]` | JSON array of CodeQL languages, one job each |
| `build-mode` | `none` | `none`, `autobuild` or `manual` |
| `queries` | `security-extended` | `default`, `security-extended` or `security-and-quality` |
| `runs-on` | `ubuntu-latest` | Runner label |

No secrets required. Private repos need GitHub Code Security enabled for the
results upload.

## Example

```yaml
on:
  push: { branches: [main] }
  pull_request:
  schedule: [{ cron: '0 6 * * 1' }]   # new query packs surface new alerts
jobs:
  codeql:
    uses: tibor-horvath/ci-toolkit/.github/workflows/codeql.yml@v1
    with:
      languages: '["csharp","javascript-typescript"]'
    permissions:
      contents: read
      security-events: write
      actions: read
```

The caller must grant `security-events: write`; a reusable workflow cannot
exceed its caller's token scope.
