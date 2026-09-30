# Dependabot for Node / React repos

A `dependabot.yml` template for consumer repos. Dependabot is per-repo configuration, so it
cannot be a reusable workflow; copy this into `.github/dependabot.yml` instead. It pairs
with [`node-audit.yml`](node-audit.md): the audit tells you a dependency is vulnerable,
Dependabot opens the PR that fixes it.

```yaml
version: 2

updates:
  - package-ecosystem: "npm"
    directory: "/"          # use "/apps/web" etc. for a monorepo package
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 5
    labels: ["dependencies"]
    groups:
      # Frameworks that must move together, or the app breaks between PRs.
      react:
        patterns: ["react", "react-dom", "@types/react", "@types/react-dom"]
      tooling:
        patterns: ["vite", "@vitejs/*", "vitest", "@vitest/*"]
      lint:
        patterns: ["eslint", "eslint-*", "@eslint/*", "typescript-eslint", "prettier", "stylelint*"]
      # Everything else that is low-risk, batched into one weekly PR.
      minor-and-patch:
        update-types: ["minor", "patch"]
        exclude-patterns: ["react", "react-dom", "vite", "vitest"]
    ignore:
      # Majors of these are migrations, not updates: schedule them deliberately.
      - dependency-name: "react"
        update-types: ["version-update:semver-major"]
      - dependency-name: "react-dom"
        update-types: ["version-update:semver-major"]

  # Keeps SHA-pinned actions current. Without this, a pin is only as good as its last review.
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      actions-minor-patch:
        update-types: ["minor", "patch"]
```

## Notes

- **Groups are the point.** Ungrouped, Dependabot opens one PR per package and a React repo
  drowns in them. Grouping things that must move together (React and its types, Vite and its
  plugins) avoids a half-upgraded state, and batching minor and patch updates keeps review
  cost to about one PR a week.
- **Order matters.** A package goes into the first group whose pattern matches it, so keep
  the specific groups above `minor-and-patch`.
- **Majors stay out of the batch.** Major versions arrive as individual PRs so each gets
  read; the `ignore` entries above go further and hold React majors back entirely until you
  choose to migrate. Remove them if you prefer to see those PRs.
- **Security updates are separate.** They are enabled under Settings → Code security, need no
  config here, and ignore the schedule and groups above.
- **Conventional Commits.** If the repo uses release-please, add `commit-message: { prefix: "chore" }`
  (or `fix` for runtime dependencies) so Dependabot PR titles pass your commit-lint and
  version bumps behave as intended.
- **pnpm and yarn.** Use `package-ecosystem: "npm"` for all three; Dependabot reads the
  lockfile that is present.
