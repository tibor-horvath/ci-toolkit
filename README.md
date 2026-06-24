# ci-toolkit

Reusable GitHub Actions workflows for building, testing, and shipping projects.
Stack-neutral by name, so pipelines for any language can coexist here.

Pin callers to the moving major tag: **`@v1`**. All third-party actions are SHA-pinned.

## Workflows

| Workflow | Purpose | Docs |
|---|---|---|
| `dotnet-build-test.yml` | .NET build + test — build-once/test-in-parallel sharding, coverage, trx report | [docs](docs/dotnet-build-test.md) |
| `docker-publish.yml` | Docker build + push to any registry (Buildx, GHA cache) | [docs](docs/docker-publish.md) |
| `nuget-publish.yml` | NuGet pack + push (idempotent, `--skip-duplicate`) | [docs](docs/nuget-publish.md) |
| `actions-consumption.yml` | Report a run's Actions usage (per OS / per job, optional account balance) | [docs](docs/actions-consumption.md) |

Each doc page lists the workflow's inputs/secrets and copy-paste caller examples.

## Quick start

```yaml
# .github/workflows/ci.yml
on:
  push: { branches: [main] }
  pull_request: { branches: [main] }
jobs:
  ci:
    uses: tibor-horvath/ci-toolkit/.github/workflows/dotnet-build-test.yml@v1
    with:
      dotnet-version: "10.0.x"
      test-matrix: '["unit","integration"]'
    secrets: inherit
    permissions:
      checks: write
      contents: read
```

## Versioning & releases

Consumers pin the moving major tag `@v1`. Releases are automated with
[release-please](https://github.com/googleapis/release-please) (`release.yml`):

1. Push [Conventional Commits](https://www.conventionalcommits.org/) to `main`
   (`feat:`, `fix:`, `refactor:`, `docs:`, …).
2. release-please maintains a **release PR** that bumps the version and updates
   `CHANGELOG.md`.
3. Merging that PR tags `vX.Y.Z`, cuts a GitHub release, and the workflow
   repoints **`v1`** at it — so `@v1` consumers get the change automatically.

`feat:` bumps the minor, `fix:` the patch; a `!` or `BREAKING CHANGE:` footer
bumps the major (and you'd then advertise a `@v2` tag). See `CHANGELOG.md` for
release history.
