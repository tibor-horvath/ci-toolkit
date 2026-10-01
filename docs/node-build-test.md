# `node-build-test.yml`

Toolchain-agnostic Node pipeline: lint, typecheck, test and build as parallel jobs. It
runs your `package.json` scripts rather than any specific tool, so it fits Vite +
Vitest, Jest, Next, Astro or a plain library. The package manager is detected from the
lockfile and the dependency store is cached. All third-party actions are SHA-pinned.

| Input | Default | Purpose |
|---|---|---|
| `node-version` | `22.x` | Node version. Ignored when `node-version-file` is set |
| `node-version-file` | `''` | Version file such as `.nvmrc` or `.node-version` |
| `package-manager` | `''` | `npm`, `pnpm` or `yarn`. Empty → detected from the lockfile |
| `pnpm-version` | `''` | pnpm version. Empty → the `packageManager` field in `package.json` |
| `working-directory` | `.` | Folder with `package.json` and the lockfile (monorepo sub-package) |
| `registry-url` | `''` | Private registry. Pair with the `npm-token` secret |
| `install-command` | `''` | Override the install. Empty → `npm ci` / `pnpm install --frozen-lockfile` / `yarn install --immutable` |
| `lint-script` | `lint` | Script to run. Empty skips the lint job |
| `typecheck-script` | `typecheck` | Script to run. Empty skips the typecheck job |
| `test-script` | `test` | Script to run. Empty skips the test job |
| `test-args` | `''` | Extra args for the test script (e.g. `--run` if `test` is `vitest` in watch mode) |
| `test-shards` | `1` | Parallel test jobs, 1–10. Each gets `--shard=<i>/<n>` |
| `collect-coverage` | `false` | Append `--coverage` and upload the report |
| `coverage-path` | `coverage` | Coverage directory, relative to `working-directory` |
| `build-script` | `build` | Script to run. Empty skips the build job |
| `build-output-dir` | `dist` | Build output, relative to `working-directory` |
| `build-env` | `''` | Newline-separated `KEY=VALUE` for the build. **Public values only** |
| `upload-build-output` | `true` | Upload the build output as an artifact |
| `build-artifact-name` | `build` | Artifact name |
| `artifact-retention-days` | `7` | Retention for build and coverage artifacts |
| `runs-on` | `ubuntu-latest` | Runner label |

| Secret | Purpose |
|---|---|
| `npm-token` | Optional. Exposed as `NODE_AUTH_TOKEN` during install, for `registry-url` |

| Output | Purpose |
|---|---|
| `package-manager` | The package manager that was used |

The calling job only needs `permissions: { contents: read }`.

## Shape

```
lint ∥ typecheck ∥ test (1..n shards) ∥ build
```

The jobs are independent, so each shows as its own status check and a lint failure does
not wait for the build. Each job installs from the cached store (a warm hit is seconds);
`node_modules` is deliberately not shipped between jobs, since a large artifact transfer
usually costs more than a cached install.

Every script input switches its job on, so `typecheck-script: ''` drops that job
entirely. Scripts are invoked as `<pm> run <script>`, so whatever your `package.json`
defines is what runs.

## Sharding

`test-shards: 4` runs four jobs, each with `--shard=<i>/4`. Vitest and Jest both support
the flag. With `collect-coverage`, each shard uploads `coverage-<i>`; merge them in a
follow-up job if you need a single report.

## Examples

**Vite + Vitest, defaults.** Needs `lint`, `build` and (optionally) `typecheck` scripts,
and a `test` script that exits, such as `vitest run`:

```yaml
jobs:
  node:
    uses: tibor-horvath/ci-toolkit/.github/workflows/node-build-test.yml@v1
    permissions:
      contents: read
```

**`test` is `vitest` (watch mode), sharded, with coverage and a public build variable:**

```yaml
jobs:
  node:
    uses: tibor-horvath/ci-toolkit/.github/workflows/node-build-test.yml@v1
    with:
      test-args: --run
      test-shards: 3
      collect-coverage: true
      build-env: |
        VITE_API_URL=https://api.example.com
    permissions:
      contents: read
```

**Monorepo package, pnpm, no typecheck job:**

```yaml
jobs:
  web:
    uses: tibor-horvath/ci-toolkit/.github/workflows/node-build-test.yml@v1
    with:
      working-directory: apps/web
      node-version-file: .nvmrc
      typecheck-script: ''
    permissions:
      contents: read
```

## Notes

- **Cancel superseded runs.** Set `concurrency:` in your calling workflow; see
  [Cancel superseded runs](../README.md#cancel-superseded-runs).
- **Coverage needs a provider.** `collect-coverage` adds `--coverage`, which fails
  without e.g. `@vitest/coverage-v8` installed. That is why it is off by default.
- **`build-env` is not for secrets.** Vite inlines `VITE_*` values into the bundle, so
  anything set there ships to browsers. The values are exported for the build step only.
- **Lockfile required.** The frozen install fails if the lockfile is missing or out of
  date, which is the point: CI should not resolve new versions.
