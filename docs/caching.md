# Smart dependency caching

Standard caching for NuGet packages and build outputs, to cut build time and
billed Actions minutes. It ships two ways:

- **Built in** — `dotnet-build-test.yml` and `nuget-publish.yml` already use the
  key scheme below; nothing to configure.
- **Composite action** — `.github/actions/cache` for your own workflows.

## Key scheme

| Tier | Key | Matches |
|---|---|---|
| Exact | `<os>-nuget-v1-<hash of manifests>` | Identical dependency state → full hit, **no save** |
| Fallback | `<os>-nuget-v1-` | Newest cache of any earlier state → restore only the delta, then save the new state |

The hash covers everything that changes the resolved package set: `*.csproj`,
`*.fsproj`, `*.vbproj`, `Directory.Packages.props`, `Directory.Build.props`,
`packages.lock.json`, `nuget.config` and `global.json`. (Previously only
`*.csproj`, so central package management edits didn't bust the cache.)

Bump the `v1` segment (`cache-version` in the action) to invalidate everything.

**Save once, restore everywhere.** The `build` job saves; the test shards use
`actions/cache/restore`, so N shards don't each try to upload the same entry.

## Composite action

```yaml
steps:
  - uses: actions/checkout@<sha>
  - uses: actions/setup-dotnet@<sha>
    with: { dotnet-version: "10.0.x" }
  - uses: tibor-horvath/ci-toolkit/.github/actions/cache@v1
  - run: dotnet restore
```

| Input | Default | Purpose |
|---|---|---|
| `nuget` | `true` | Cache `~/.nuget/packages` |
| `nuget-key-files` | csproj/props/lock/config globs | Globs hashed into the key |
| `restore-only` | `false` | Restore without saving — use in fan-out/matrix jobs |
| `build-paths` | `''` | Extra build-output paths to cache; empty = off |
| `build-key-files` | `''` | Globs hashed into the build-output key |
| `build-key-prefix` | `build` | Name segment; change to bust one cache |
| `cache-version` | `v1` | Bump to invalidate everything |

Outputs: `nuget-cache-hit`, `build-cache-hit` (`'true'` on an exact match).

### Build-output cache

Build caches use `…-<manifest hash>-<sha>` with fallbacks to the same manifest
hash, then any. Every run saves a fresh snapshot (caches are immutable) and
restores the most recent.

```yaml
# Node / Next.js
- uses: tibor-horvath/ci-toolkit/.github/actions/cache@v1
  with:
    nuget: "false"
    build-paths: |
      .next/cache
      node_modules/.cache
    build-key-files: "**/package-lock.json"
```

**Caveat for .NET:** don't cache `bin`/`obj` expecting faster compiles. A fresh
checkout resets file mtimes, so MSBuild treats everything as stale and
recompiles anyway. The toolkit's build-once artifact already avoids repeat
compiles across jobs. Build-output caching pays off for tools with
content-hash incremental caches (webpack, Next.js, Gradle, ccache).

## Cost notes

- Caches are evicted after 7 days unused and past 10 GB per repo; fallback
  restores accumulate stale packages until then. Bump `cache-version` if a
  cache bloats.
- PR caches are scoped to the PR's ref but can read the default branch's, so
  keep `main` warm (it runs on every merge).
- A cache hit is free; restoring a large cache still takes time — don't cache
  what downloads faster than it restores.
