# `stale.yml`

Reusable stale-bot. Labels issues and pull requests with no recent activity,
then closes them if there is still none. Items with an exempt label, a
milestone or an assignee are left alone, and any new comment resets the clock.

| Input | Default | Purpose |
|---|---|---|
| `days-before-stale` | `60` | Days of inactivity before the label is added |
| `days-before-close` | `14` | Further days before closing; `-1` never closes |
| `exempt-labels` | `pinned,security,keep-open` | Labels that exempt an item |
| `stale-label` | `stale` | Label added to stale items |
| `stale-message` | *(built-in text)* | Comment when marked stale |
| `close-message` | *(built-in text)* | Comment when closed |
| `only-labels` | `''` | Only consider items with these labels. Empty → all |
| `dry-run` | `false` | Log what would change without acting |
| `runs-on` | `ubuntu-latest` | Runner label |

No secrets required.

## Example

```yaml
on:
  schedule: [{ cron: '0 3 * * *' }]
  workflow_dispatch:
jobs:
  stale:
    uses: tibor-horvath/ci-toolkit/.github/workflows/stale.yml@v1
    with:
      dry-run: true        # inspect the log first, then remove this line
    permissions:
      issues: write
      pull-requests: write
```

Run with `dry-run: true` first: the first real run can touch every old item at
once.
