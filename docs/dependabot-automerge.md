# `dependabot-automerge.yml`

Reusable workflow that approves and auto-merges Dependabot PRs that stay within
a policy you choose (by default, minor and patch bumps). Everything else is left
for a person, and the reviewers you name are asked to review it.

| PR | Result (defaults) |
|---|---|
| `lodash` 4.17.20 → 4.17.21 (patch) | Approved, auto-merge enabled |
| Group: three minors and one patch | Approved, auto-merge enabled |
| Group: two minors and one **major** | Left for review, `reviewers` requested |
| `react` 18 → 19 (major) | Left for review, `reviewers` requested |
| Any PR not opened by Dependabot, or one a person pushed to | Job skipped |

Every dependency in a PR is checked, so a grouped PR is merged only when all of
its members pass. If a later Dependabot update brings a grouped PR outside the
policy (for example by adding a major), the run switches off the auto-merge
that an earlier run had queued.

| Input | Default | Purpose |
|---|---|---|
| `update-types` | `minor`, `patch` | Newline- or comma-separated semver bumps that may be auto-merged: `patch`, `minor`, `major`. An update without a semver type (for example, a commit-SHA bump) never matches |
| `dependency-types` | `''` | Newline- or comma-separated dependency types that may be auto-merged: `direct:production`, `direct:development`, `indirect`. Empty → any |
| `merge-method` | `squash` | `squash`, `merge` or `rebase`. Squash keeps the PR title as the commit, which release-please reads |
| `approve` | `true` | Approve the PR before enabling auto-merge, for branches that require a review |
| `reviewers` | `''` | Newline- or comma-separated users or `org/team` slugs to request when a PR is *not* auto-merged. Empty → no request |
| `runs-on` | `ubuntu-latest` | Runner label |
| `timeout-minutes` | `15` | Job timeout in minutes |
| `cancel-superseded` | `true` | Cancel an in-flight run when a newer one starts for the same pull request. PR events only; see [Cancel superseded runs](../README.md#cancel-superseded-runs) |

| Output | Description |
|---|---|
| `automerge` | `true` when auto-merge was enabled, `false` when the PR was left for review, empty when the job was skipped (not a Dependabot PR) |

No secrets required. The workflow's own token is used and needs
`contents: write` and `pull-requests: write`. A reusable workflow cannot get
more permissions than its caller grants, so the caller must grant both.

## Setup

1. **Settings → General → Pull Requests → Allow auto-merge.**
2. **Settings → Actions → General → Allow GitHub Actions to create and approve
   pull requests.** Only needed with `approve: true`.
3. **Protect the base branch with required status checks** (branch protection
   or a ruleset). `gh pr merge --auto` waits only for *required* checks. On a
   branch that requires none, the PR is merged as soon as auto-merge is
   enabled, before your CI has run. This is the setting that actually decides
   whether a Dependabot PR gets merged, not this workflow.

## Example

```yaml
# .github/workflows/dependabot-automerge.yml
on: pull_request
jobs:
  automerge:
    uses: tibor-horvath/ci-toolkit/.github/workflows/dependabot-automerge.yml@v1
    with:
      reviewers: my-org/maintainers
    permissions:
      contents: write
      pull-requests: write
```

Auto-merging only patch bumps of dev dependencies, which is a cautious policy
for npm or NuGet, where a minor bump is more likely to break things than in
GitHub Actions:

```yaml
jobs:
  automerge:
    uses: tibor-horvath/ci-toolkit/.github/workflows/dependabot-automerge.yml@v1
    with:
      update-types: patch
      dependency-types: |
        direct:development
        indirect
    permissions:
      contents: write
      pull-requests: write
```

## Safety

- The job runs only when both the PR author and `github.actor` (the account that
  triggered this run) are `dependabot[bot]`. A person pushing to a Dependabot
  branch becomes the actor, so a modified PR is never merged without review.
- No PR code is checked out or run. The workflow reads Dependabot's metadata
  and calls the GitHub API, nothing else.
- Use `on: pull_request`. Dependabot-triggered `pull_request` runs get a token
  with the permissions the workflow asks for. They can read Dependabot secrets
  only, not Actions secrets, but this workflow needs neither.
- Pair it with Dependabot `groups` that keep majors out of the minor/patch
  group (see this repo's [`dependabot.yml`](../.github/dependabot.yml)). That
  way one major doesn't hold a whole weekly batch back from auto-merge.
