# NuGet publish

Pack once and push every resulting package with `--skip-duplicate`, so re-runs
are idempotent. Mark non-package projects with `<IsPackable>false</IsPackable>`
so only real packages publish. Typically triggered on `release: published`.

There are two entry points, and **which one to use depends on how you
authenticate**:

| You authenticate with | Use |
|---|---|
| nuget.org Trusted Publishing (OIDC, no stored secret) — recommended | the composite action `.github/actions/nuget-publish` |
| A long-lived API key | the composite action, or the reusable workflow `nuget-publish.yml` |

## Why Trusted Publishing needs the action

nuget.org only issues a key when the OIDC token's `job_workflow_ref` claim
starts with `<owner>/<repo>/.github/workflows/` of the repository in your
Trusted Publishing policy. For a job that runs inside a reusable workflow from
another repository, GitHub sets that claim to the **called** workflow
(`tibor-horvath/ci-toolkit/.github/workflows/nuget-publish.yml@…`), so the
exchange fails:

```
Token exchange failed (HTTP 401) … Claim 'job_workflow_ref' has value
'tibor-horvath/ci-toolkit/.github/workflows/nuget-publish.yml@…' which does not
start with <owner>/<repo>/.github/workflows/.
```

A composite action runs as steps inside your own job, so the claim names your
workflow file and the policy matches. No nuget.org policy setting can make the
reusable workflow pass.

## Composite action (Trusted Publishing)

On nuget.org → your username → **Trusted Publishing**, add a policy with the
repository owner, repository name and **your** workflow file name (e.g.
`publish-nuget.yml`, file name only). Store your nuget.org profile name (not
your email) as a repository variable, e.g. `NUGET_USER`.

```yaml
# .github/workflows/publish-nuget.yml
on:
  release:
    types: [published]
permissions:
  contents: read
jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write # GitHub OIDC token for NuGet/login
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
      - id: nuget
        uses: tibor-horvath/ci-toolkit/.github/actions/nuget-publish@v2
        with:
          dotnet-version: "10.0.x"
          nuget-user: ${{ vars.NUGET_USER }}
      - run: echo "Shipped ${{ steps.nuget.outputs.packages }} at ${{ steps.nuget.outputs.version }}"
```

Call it after `actions/checkout`; it installs the SDK, restores the NuGet cache,
packs into `$RUNNER_TEMP`, logs in right before the push (the temporary key
lasts 1 hour) and pushes.

| Input | Default | Purpose |
|---|---|---|
| `dotnet-version` | `10.0.x` | SDK version to install. Empty skips `setup-dotnet` |
| `project` | `''` | sln/project to pack. Empty → root `.sln`/`.slnx` |
| `configuration` | `Release` | Build configuration |
| `version` | `''` | Package version. Empty → release tag with leading `v` stripped |
| `nuget-source` | nuget.org | Feed to push to |
| `nuget-user` | `''` | nuget.org profile name for Trusted Publishing. Set → OIDC login |
| `nuget-api-key` | `''` | API key, used when `nuget-user` is empty |
| `include-symbols` | `false` | Also pack + push `.snupkg` |
| `cache` | `true` | Restore/save the NuGet package cache |

Outputs: `version` (the version actually packed) and `packages`
(comma-separated `.nupkg` filenames that were packed and pushed).

## Reusable workflow `nuget-publish.yml` (API key only)

| Input | Default | Purpose |
|---|---|---|
| `dotnet-version` | `10.0.x` | SDK version to install |
| `project` | `''` | sln/project to pack. Empty → root `.sln`/`.slnx` |
| `configuration` | `Release` | Build configuration |
| `version` | `''` | Package version. Empty → release tag with leading `v` stripped |
| `nuget-source` | nuget.org | Feed to push to |
| `nuget-user` | `''` | **Unsupported.** Setting it fails the run with a pointer to the composite action (see above) |
| `include-symbols` | `false` | Also pack + push `.snupkg` |
| `runs-on` | `ubuntu-latest` | Runner label |
| `timeout-minutes` | `60` | Job timeout in minutes |

| Secret | Purpose |
|---|---|
| `nuget-api-key` | API key for the feed. Required. nuget.org discourages long-lived keys for CI, and they expire |

The job no longer requests `id-token: write`, so callers don't need to grant it.

| Output | Purpose |
|---|---|
| `version` | The version actually packed |
| `packages` | Comma-separated `.nupkg` filenames that were packed and pushed |

`version` is worth reading back rather than assuming: when the `version` input is
empty it is derived from the release tag, so the caller does not know it up front.

```yaml
on:
  release:
    types: [published]
permissions:
  contents: read
jobs:
  publish:
    uses: tibor-horvath/ci-toolkit/.github/workflows/nuget-publish.yml@v2
    secrets:
      nuget-api-key: ${{ secrets.NUGET_API_KEY }}

  announce:
    needs: publish
    runs-on: ubuntu-latest
    steps:
      - run: echo "Shipped ${{ needs.publish.outputs.packages }} at ${{ needs.publish.outputs.version }}"
```

## Migrating from `nuget-user` on the reusable workflow

Replace the `uses: …/workflows/nuget-publish.yml` job with a `runs-on` job that
checks out and calls the action, as in the first example. Keep `id-token: write`
on the job, keep your nuget.org policy pointing at the same workflow file, and
move the `with:` inputs (except `runs-on` / `timeout-minutes`, which become job
keys) onto the action step. Outputs move from `needs.<job>.outputs.*` to
`steps.<id>.outputs.*`; expose them as job outputs if another job needs them.
