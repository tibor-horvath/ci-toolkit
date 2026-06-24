# `actions-consumption.yml`

Stack-agnostic. Posts a run's Actions usage — broken down **by OS and by job** —
to the job summary. Usage is computed from each job's start/finish timestamps
(`runs/{id}/jobs`), rounded up per job × OS multiplier, because the
`runs/{id}/timing` `billable` field returns 0 on GitHub's metered billing
platform. It's a close estimate, not the invoiced figure.

> **A run cannot measure itself.** GitHub finalizes billable time only *after* a run
> completes, so calling this as a job *inside* the run reports all zeros. Trigger it on
> the **completed** run with a `workflow_run` workflow and pass that run's id.

| Input | Default | Purpose |
|---|---|---|
| `run-id` | current run | Run to report on. Pass `github.event.workflow_run.id` |
| `included-minutes` | `0` | Plan's monthly minutes (e.g. `2000` Free, `3000` Pro) → shows "remaining". `0` = used/cost only |
| `runs-on` | `ubuntu-latest` | Runner label |

**Optional account usage.** Pass a `billing_token` secret to add an account-level
Actions usage section (per-SKU minutes + net cost) from GitHub's enhanced billing
usage API:

- Must be a **classic** PAT with the `user` scope. The billing endpoints do **not**
  accept fine-grained PATs (there is no "Plan" scope on classic tokens), and the
  built-in `GITHUB_TOKEN` can't read billing. Omit the secret to skip the section.
- The usage API reports consumption, not your allowance — set `included-minutes` to
  show **remaining**. Minutes are counted allowance-equivalent (Windows 2×, macOS 10×).
- Requires an account on GitHub's enhanced/metered billing platform.

## Example

Add as a separate workflow that fires after the measured workflow completes:

```yaml
# .github/workflows/ci-consumption.yml
name: CI Consumption
on:
  workflow_run:
    workflows: ["CI"] # must match the measured workflow's `name:`
    types: [completed]
permissions:
  actions: read
jobs:
  report:
    uses: tibor-horvath/ci-toolkit/.github/workflows/actions-consumption.yml@v1
    with:
      run-id: ${{ github.event.workflow_run.id }}
      included-minutes: 3000
    secrets:
      billing_token: ${{ secrets.BILLING_TOKEN }}
    permissions:
      actions: read
```
