# Contributing

`@v1` is a moving tag, so a mistake merged to `main` reaches every consumer on
the next release. The **Self Check** workflow
([`self-check.yml`](.github/workflows/self-check.yml)) is the guard for that;
every PR must pass it.

## What Self Check enforces

| Job | Fails when |
|---|---|
| `actionlint` | A workflow has invalid syntax, expressions, `needs`/`if` references, or a `run:` block that shellcheck flags |
| `yamllint` | Any YAML under `.github/` or `tests/` has duplicate keys, bad indentation or syntax errors ([config](.yamllint.yml)) |
| `pinned-actions` | A third-party `uses:` (workflows or `.github/actions`) is not pinned to a full 40-character commit SHA |
| `explicit-permissions` | A workflow has no `permissions:` block |
| `docs-consistency` | A reusable workflow is missing from the README, has no `docs/<name>.md`, or that page omits an input, secret or output |
| `secret-scan` | gitleaks finds a leaked secret (this runs the toolkit's own reusable workflow) |
| `smoke-*` | `node-build-test`, `node-audit`, `dotnet-build-test` or `dotnet-vulnerable-packages` fails when run for real against the fixtures |

## Adding or changing a reusable workflow

1. Add or edit `.github/workflows/<name>.yml` and declare `permissions:`.
2. Add or update `docs/<name>.md`. It must mention every input, secret and
   output by name, and include a copy-paste caller example.
3. Add a row to the README workflow table.
4. Pin third-party actions to a full SHA with the version as a trailing comment
   (`uses: owner/repo@<sha> # v4`).
5. Use [Conventional Commits](https://www.conventionalcommits.org/); release
   automation derives the version bump from them (see the README).

### Deliberately inheriting the caller's permissions

If a workflow's needs depend on the caller (like `docker-publish.yml`, where the
registry decides the scope), omit `permissions:` and add this comment so
`explicit-permissions` skips it:

```yaml
# self-check: inherit-permissions
```

## Smoke-test fixtures

`tests/fixtures/` exists only for the `smoke-*` jobs; nothing there is shipped.

- `node-app` has no dependencies: a `package.json` with stub scripts and a
  lockfile. It exercises the npm path only, not pnpm or yarn.
- `dotnet-app` has one xunit test. Its namespace contains `.unit.` because the
  workflow filters shards with `FullyQualifiedName~.<shard>.`.

If you add an input that changes runtime behaviour, extend a fixture or the
smoke job's `with:` so the new path is exercised.

## Versions that are bumped by hand

Dependabot does not track versions held in `env:` or `run:` steps. Update these
manually:

- the `actionlint-version` default in `workflow-lint.yml` (`self-check.yml` uses it)
- in `self-check.yml`: `yamllint==…` and `pyyaml==…` in the `yamllint` and `docs-consistency` jobs

## Dependabot PRs

[`dependabot.yml`](.github/dependabot.yml) opens one grouped PR a week for minor
and patch bumps of the actions used here, and one PR per action for majors.
[`dependabot-automerge.yml`](.github/workflows/dependabot-automerge.yml) treats
them differently:

- **Minor / patch (the grouped PR):** approved and set to auto-merge. GitHub
  merges it once the required checks on `main` pass. A group containing a major
  is not merged automatically, because the group's update type is its highest
  bump.
- **Major:** left open. Read the changelog first; `upload-artifact` and
  `download-artifact` must be bumped together, since their versions have to be
  compatible.

Every merge is a `fix(deps):` commit, so release-please cuts a patch release and
moves `v1`. Consumers get the new action versions without doing anything.

The automerge needs these repo settings, which live outside the code:

- **Allow auto-merge** (Settings → General → Pull Requests).
- **Allow GitHub Actions to create and approve pull requests** (Settings →
  Actions → General), so the approval satisfies the required-review rule.
- A branch protection rule or ruleset on `main` requiring the Self Check jobs.
  Without required checks, `--auto` merges immediately, so the workflow relies
  on this rule as its only gate.

If Dependabot PRs stop merging on their own, check those three first.

## Running checks locally

```bash
pip install yamllint pyyaml
python -m yamllint --strict -c .yamllint.yml .github tests .yamllint.yml
python .github/scripts/check-docs.py
actionlint   # https://github.com/rhysd/actionlint
```

The smoke tests only run on GitHub-hosted runners; push a branch to run them.
