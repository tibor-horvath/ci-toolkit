# `docker-publish.yml`

Reusable Docker build + push (Buildx, GHA layer cache, SHA-pinned actions) to any
registry.

| Input | Default | Purpose |
|---|---|---|
| `image` | `''` | Full image name w/o tag. Empty → `<registry>/<repo lowercased>` |
| `registry` | `ghcr.io` | Registry host (`ghcr.io`, `docker.io`, …) |
| `tags` | `''` | Comma-separated tag list. Empty → `sha-<github.sha>` |
| `context` | `.` | Build context |
| `dockerfile` | `Dockerfile` | Path to the Dockerfile |
| `push` | `true` | Push (set `false` to build-only, e.g. PRs) |
| `build-args` | `''` | Newline-separated `KEY=VALUE` build args |
| `runs-on` | `ubuntu-latest` | Runner label |

This workflow declares **no permissions of its own** — it inherits the caller job's
token. So each caller grants what its registry needs: **GHCR** → `packages: write`
(login defaults to `github.actor` + `GITHUB_TOKEN`); **other registries** → just
`contents: read` plus `registry-username` / `registry-password` secrets.

## Outputs

| Output | Purpose |
|---|---|
| `image` | Image name that was built, without a tag |
| `tags` | Comma-separated list of the fully-qualified refs that were built |
| `digest` | Image digest (`sha256:…`). Empty when `push: false` — nothing reaches a registry, so there is nothing to address |

Deploy from the digest, not a tag: a tag can be repointed at a different image
later, a digest cannot.

```yaml
jobs:
  docker:
    permissions:
      contents: read
      packages: write
    uses: tibor-horvath/ci-toolkit/.github/workflows/docker-publish.yml@v1
    with:
      tags: sha-${{ github.sha }},latest

  deploy:
    needs: docker
    runs-on: ubuntu-latest
    steps:
      - run: |
          helm upgrade app ./chart \
            --set image.repository=${{ needs.docker.outputs.image }} \
            --set image.digest=${{ needs.docker.outputs.digest }}
```

## Examples

```yaml
# GHCR, push only on main
jobs:
  docker:
    needs: dotnet
    permissions:
      contents: read
      packages: write
    uses: tibor-horvath/ci-toolkit/.github/workflows/docker-publish.yml@v1
    with:
      tags: sha-${{ github.sha }}
      push: ${{ github.ref == 'refs/heads/main' }}
```

```yaml
# Docker Hub
jobs:
  docker:
    permissions:
      contents: read
    uses: tibor-horvath/ci-toolkit/.github/workflows/docker-publish.yml@v1
    with:
      registry: docker.io
      image: myuser/myapp
      tags: latest
      dockerfile: src/App/Dockerfile
    secrets:
      registry-username: ${{ secrets.DOCKER_HUB_USERNAME }}
      registry-password: ${{ secrets.DOCKER_HUB_PASSWORD }}
```
