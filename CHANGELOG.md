# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Consumers pin the
moving major tag `@v1`.

## [1.5.1](https://github.com/tibor-horvath/ci-toolkit/compare/v1.5.0...v1.5.1) (2026-06-24)


### Fixed

* update permissions handling in Docker publish workflow documentation ([b3310cb](https://github.com/tibor-horvath/ci-toolkit/commit/b3310cb63e97c75fe2c850a355376161eb7f646f))

## [1.5.0](https://github.com/tibor-horvath/ci-toolkit/compare/v1.4.2...v1.5.0) (2026-06-24)


### Added

* add reusable Docker publish workflow with configurable inputs ([4ea495c](https://github.com/tibor-horvath/ci-toolkit/commit/4ea495c17e5333e446075968a08aa4f22374b82b))


### Fixed

* update PAT scope description in billing documentation ([f62a372](https://github.com/tibor-horvath/ci-toolkit/commit/f62a3726432ff7508580457b6ac2b51f903bc847))

## [1.4.2](https://github.com/tibor-horvath/ci-toolkit/compare/v1.4.1...v1.4.2) (2026-06-23)


### Fixed

* compute consumption from job timestamps ([#1](https://github.com/tibor-horvath/ci-toolkit/issues/1)) ([84c7774](https://github.com/tibor-horvath/ci-toolkit/commit/84c7774ca5113422a1c6eb5164d0495073370c7f))
* Fix/consumption from timestamps ([#3](https://github.com/tibor-horvath/ci-toolkit/issues/3)) ([aeb8a81](https://github.com/tibor-horvath/ci-toolkit/commit/aeb8a81135122a8efe8843a5f213769bb4b779a9))

## [1.4.1] - 2026-06-23

### Added
- `LICENSE` (MIT) and this `CHANGELOG.md`.

## [1.4.0] - 2026-06-23

### Changed
- **Unified `build` → `test` shape** for every caller. Replaced the dual-mode
  design (a combined job for unsharded callers vs. split jobs for sharded ones)
  with a single structure: one `build` job compiles once and uploads its output,
  and the `test` job runs `--no-build`, fanning into parallel shards via
  `test-matrix`. Removes the skipped "phantom" job that showed on sharded runs and
  gives all consumers an identical run graph.

## [1.3.0] - 2026-06-23

### Added
- **Per-job breakdown** in the consumption report (joins `runs/{id}/timing`
  `job_runs` with the jobs API for names; shows raw runtime and per-job billed
  minutes, rounded up to the minute).
- Optional **account-balance** section (used / included / remaining) gated on a
  `billing_token` secret. Skipped when no token is supplied, since the built-in
  `GITHUB_TOKEN` cannot read billing.

## [1.2.0] - 2026-06-23

### Fixed
- Consumption report no longer reports zeros. A run cannot read its own finalized
  billing, so the reporter now takes a `run-id` input (intended for a
  `workflow_run` trigger on the completed run) and polls until billing is ready.

## [1.1.0] - 2026-06-23

### Added
- Build-once / test-in-parallel handling for sharded runs (later generalized in
  1.4.0): compile once, share the output as an artifact, test with `--no-build`.

## [1.0.0] - 2026-06-23

### Added
- `dotnet-build-test.yml` — parameterized, SHA-pinned .NET build/test reusable
  workflow with NuGet caching, trx reporting, and coverage upload.
- `actions-consumption.yml` — stack-agnostic GitHub Actions consumption reporter.
- `README.md` with inputs reference and caller examples.

[1.4.1]: https://github.com/tibor-horvath/ci-toolkit/compare/v1.4.0...v1.4.1
[1.4.0]: https://github.com/tibor-horvath/ci-toolkit/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/tibor-horvath/ci-toolkit/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/tibor-horvath/ci-toolkit/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/tibor-horvath/ci-toolkit/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/tibor-horvath/ci-toolkit/releases/tag/v1.0.0
