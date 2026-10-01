# ci-toolkit

[![Built by Tibor Horváth](https://tiborhorvath.dev/badge/built-by-compact.svg)](https://tiborhorvath.dev)

Reusable GitHub Actions workflows for building, testing, and shipping projects.
Stack-neutral by name, so pipelines for any language can coexist here.

Pin callers to the moving major tag: **`@v1`**. All third-party actions are SHA-pinned.

## Workflows

### .NET

| Workflow | Purpose | Docs |
|---|---|---|
| `dotnet-build-test.yml` | .NET build + test — build-once/test-in-parallel sharding, coverage, trx report | [docs](docs/dotnet-build-test.md) |
| `nuget-publish.yml` | NuGet pack + push (idempotent, `--skip-duplicate`) | [docs](docs/nuget-publish.md) |
| `dotnet-vulnerable-packages.yml` | NuGet vulnerability check, direct + transitive, fails on findings | [docs](docs/dotnet-vulnerable-packages.md) |

### Node / React

| Workflow | Purpose | Docs |
|---|---|---|
| `node-build-test.yml` | Node/React lint, typecheck, test (sharded) and build — npm/pnpm/yarn auto-detected, script-driven | [docs](docs/node-build-test.md) |
| `node-audit.yml` | Dependency vulnerability audit from the lockfile (npm/pnpm/yarn), severity threshold, prod-only by default | [docs](docs/node-audit.md) |
| `bundle-size.yml` | Builds PR and base, posts gzip/raw size delta as a PR comment, optional size gate | [docs](docs/bundle-size.md) |
| `lighthouse-ci.yml` | Lighthouse CI on the static build with minimum category scores; reports kept private as an artifact | [docs](docs/lighthouse-ci.md) |
| Dependabot template | `dependabot.yml` for Node/React repos — grouped React/tooling/lint updates | [docs](docs/dependabot-node.md) |

### Containers

| Workflow | Purpose | Docs |
|---|---|---|
| `docker-publish.yml` | Docker build + push to any registry (Buildx, GHA cache) | [docs](docs/docker-publish.md) |

### Any stack

| Workflow | Purpose | Docs |
|---|---|---|
| `secret-scan.yml` | Scan commits/PRs for leaked API keys, tokens and connection strings (gitleaks) | [docs](docs/secret-scan.md) |
| `codeql.yml` | CodeQL static analysis, one job per language, results in Code scanning | [docs](docs/codeql.md) |
| `dependency-review.yml` | Blocks PRs that add vulnerable or disallowed-licence dependencies | [docs](docs/dependency-review.md) |
| `pr-title-lint.yml` | Enforces Conventional Commit PR titles (what release-please reads) | [docs](docs/pr-title-lint.md) |
| `workflow-lint.yml` | actionlint + shellcheck + SHA-pin check for a repo's own workflows | [docs](docs/workflow-lint.md) |
| `stale.yml` | Label and close inactive issues and PRs | [docs](docs/stale.md) |
| `actions-consumption.yml` | Report a run's Actions usage (per OS / per job, optional account balance) | [docs](docs/actions-consumption.md) |
| `.github/actions/cache` | Composite action: NuGet + build-output caching with restore-key fallbacks | [docs](docs/caching.md) |
| `.github/actions/node-setup` | Composite action: package-manager detection, pnpm/corepack, Node + dependency cache, frozen install | [docs](docs/node-setup.md) |

Each doc page lists the workflow's inputs/secrets and copy-paste caller examples.

Contributing? See [CONTRIBUTING.md](CONTRIBUTING.md) for the checks every PR must pass.

## Quick start

```yaml
# .github/workflows/ci.yml
on:
  push: { branches: [main] }
  pull_request: { branches: [main] }
jobs:
  dotnet:
    name: .NET
    uses: tibor-horvath/ci-toolkit/.github/workflows/dotnet-build-test.yml@v1
    with:
      dotnet-version: "10.0.x"
      test-matrix: '["unit","integration"]'
    secrets: inherit
    permissions:
      checks: write
      contents: read
```

## Cancel superseded runs

A reusable workflow cannot cancel its caller's earlier runs; the `concurrency:`
group belongs to the calling workflow. Without it, every push to a PR branch
keeps the previous run going and burns minutes. Add this to your caller:

```yaml
concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
```

Cancelling only on `pull_request` keeps runs on `main` (and any release or
publish run) from being cut short by the next merge. Heavy workflows such as
`node-build-test`, `dotnet-build-test`, `lighthouse-ci` and `bundle-size` gain
the most.

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
