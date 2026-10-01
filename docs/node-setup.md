# node-setup (composite action)

Detects the package manager, sets up pnpm or corepack, sets up Node with the
dependency cache, and installs dependencies. Call it right after
`actions/checkout`.

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: tibor-horvath/ci-toolkit/.github/actions/node-setup@v1
    with:
      working-directory: web
  - run: npm test
    working-directory: web
```

## Inputs

| Input | Default | Description |
|---|---|---|
| `working-directory` | `.` | Directory holding `package.json` and the lockfile. |
| `package-manager` | `""` | `npm`, `pnpm` or `yarn`. Empty detects it from the lockfile. |
| `pnpm-version` | `""` | pnpm version. Empty reads `packageManager` from `package.json`. |
| `node-version` | `22.x` | Node version (ignored when `node-version-file` is set). |
| `node-version-file` | `""` | Version file such as `.nvmrc`, relative to `working-directory`. |
| `registry-url` | `""` | Registry URL; writes an `.npmrc` that reads `NODE_AUTH_TOKEN`. |
| `cache` | `true` | Cache the package manager's store via `setup-node`. |
| `install` | `true` | Install dependencies. Set `false` for jobs that only need the toolchain. |
| `install-command` | `""` | Custom install command replacing the frozen-lockfile install. |
| `npm-token` | `""` | Auth token for `registry-url`, exposed as `NODE_AUTH_TOKEN` during install. |
| `workspace-prefix` | `""` | Path prefix (with trailing slash) for jobs that check out into a subfolder, e.g. `head/`. |

## Outputs

| Output | Description |
|---|---|
| `package-manager` | The package manager in use (`npm`, `pnpm` or `yarn`). |
| `lockfile` | Lockfile name for that package manager. |
