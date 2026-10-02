# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Consumers pin the
moving major tag `@v1`.

## [1.15.1](https://github.com/tibor-horvath/ci-toolkit/compare/v1.15.0...v1.15.1) (2026-10-02)


### Documentation

* Add social preview ([#44](https://github.com/tibor-horvath/ci-toolkit/issues/44)) ([85373ab](https://github.com/tibor-horvath/ci-toolkit/commit/85373ab46eedfbf219711ae974c9ea6b21f7d2e0))

## [1.15.0](https://github.com/tibor-horvath/ci-toolkit/compare/v1.14.0...v1.15.0) (2026-10-01)


### Added

* add .NET coverage comment workflow and documentation ([#42](https://github.com/tibor-horvath/ci-toolkit/issues/42)) ([3ffe4cb](https://github.com/tibor-horvath/ci-toolkit/commit/3ffe4cbb6fbfb8ecb5d892bc5854a09f933ab9e8))


### Fixed

* update cache action version to v1.14.0 in workflows ([14e15da](https://github.com/tibor-horvath/ci-toolkit/commit/14e15dacaa666b96c55c5731be59cac926bb3eb6))

## [1.14.0](https://github.com/tibor-horvath/ci-toolkit/compare/v1.13.1...v1.14.0) (2026-10-01)


### Added

* add concurrency settings and cancel superseded runs to workflows ([f9f9987](https://github.com/tibor-horvath/ci-toolkit/commit/f9f9987125787610899a4a4d225890306ef1da9f))

## [1.13.1](https://github.com/tibor-horvath/ci-toolkit/compare/v1.13.0...v1.13.1) (2026-10-01)


### Fixed

* bump actions/download-artifact from 4.3.0 to 8.0.1 ([#23](https://github.com/tibor-horvath/ci-toolkit/issues/23)) ([e0401c4](https://github.com/tibor-horvath/ci-toolkit/commit/e0401c49e8b6c7a2455ebf413fd311b1b7c31370))
* bump actions/upload-artifact from 4.6.2 to 7.0.1 ([#22](https://github.com/tibor-horvath/ci-toolkit/issues/22)) ([9c625ff](https://github.com/tibor-horvath/ci-toolkit/commit/9c625ff6a86bd34d3acb8a01ab5a660dda7ef0cf))
* bump docker/build-push-action from 6.19.2 to 7.3.0 ([#20](https://github.com/tibor-horvath/ci-toolkit/issues/20)) ([dfc126f](https://github.com/tibor-horvath/ci-toolkit/commit/dfc126f33ff36857414d9f03822b495c4c31f3ac))
* bump docker/login-action from 3.7.0 to 4.6.0 ([#21](https://github.com/tibor-horvath/ci-toolkit/issues/21)) ([9f92361](https://github.com/tibor-horvath/ci-toolkit/commit/9f92361b3f25b2351d863de39041497bec57488e))
* bump docker/setup-buildx-action from 3.12.0 to 4.3.0 ([#24](https://github.com/tibor-horvath/ci-toolkit/issues/24)) ([dc8b87e](https://github.com/tibor-horvath/ci-toolkit/commit/dc8b87e8520c98883be0039d11894aca850ee09c))

## [1.13.0](https://github.com/tibor-horvath/ci-toolkit/compare/v1.12.0...v1.13.0) (2026-10-01)


### Added

* Optimize workflows ([#36](https://github.com/tibor-horvath/ci-toolkit/issues/36)) ([2a494b9](https://github.com/tibor-horvath/ci-toolkit/commit/2a494b97962ab4aa7a12d3c1824f99e4ab253598))

## [1.12.0](https://github.com/tibor-horvath/ci-toolkit/compare/v1.11.0...v1.12.0) (2026-10-01)


### Added

* add CodeQL, dependency review, PR title lint, workflow lint, stale and NuGet vulnerability workflows ([#34](https://github.com/tibor-horvath/ci-toolkit/issues/34)) ([866b715](https://github.com/tibor-horvath/ci-toolkit/commit/866b715f469cc1f9242bd65c6c2f0775badfabfd))

## [1.11.0](https://github.com/tibor-horvath/ci-toolkit/compare/v1.10.0...v1.11.0) (2026-09-30)


### Added

* enhance self-check workflows with structural YAML checks and smoke tests ([#32](https://github.com/tibor-horvath/ci-toolkit/issues/32)) ([75a2696](https://github.com/tibor-horvath/ci-toolkit/commit/75a2696e525b225d240315e167ca954d3bd1764a))

## [1.10.0](https://github.com/tibor-horvath/ci-toolkit/compare/v1.9.0...v1.10.0) (2026-09-30)


### Added

* implement smart dependency caching for NuGet packages and build outputs ([#28](https://github.com/tibor-horvath/ci-toolkit/issues/28)) ([844cc1b](https://github.com/tibor-horvath/ci-toolkit/commit/844cc1b45e24366014875cbde401316664476ebe))

## [1.9.0](https://github.com/tibor-horvath/ci-toolkit/compare/v1.8.0...v1.9.0) (2026-09-30)


### Added

* add reusable secret scan workflow to detect leaked credentials ([#27](https://github.com/tibor-horvath/ci-toolkit/issues/27)) ([690625f](https://github.com/tibor-horvath/ci-toolkit/commit/690625f9958d420c5e6ed3f70b4f1dc2fb164364))


### Documentation

* add badge for author in README ([#25](https://github.com/tibor-horvath/ci-toolkit/issues/25)) ([c1f1774](https://github.com/tibor-horvath/ci-toolkit/commit/c1f17745245d7786ced56ae11c8a357d7a4fadb1))

## [1.8.0](https://github.com/tibor-horvath/ci-toolkit/compare/v1.7.1...v1.8.0) (2026-08-31)


### Added

* add outputs for reusable workflows in actions consumption, docker publish, dotnet build & test, and nuget publish ([#17](https://github.com/tibor-horvath/ci-toolkit/issues/17)) ([afa79b4](https://github.com/tibor-horvath/ci-toolkit/commit/afa79b4503a9cf040ef5fee268c939cb2b946b31))

## [1.7.1](https://github.com/tibor-horvath/ci-toolkit/compare/v1.7.0...v1.7.1) (2026-08-31)


### Fixed

* bump actions/cache from 4.3.0 to 6.1.0 ([#13](https://github.com/tibor-horvath/ci-toolkit/issues/13)) ([5e241d3](https://github.com/tibor-horvath/ci-toolkit/commit/5e241d30dac6150fa6f33ce3a33f9a627d8514db))
* bump actions/checkout from 4.3.1 to 7.0.1 ([#15](https://github.com/tibor-horvath/ci-toolkit/issues/15)) ([43e64d3](https://github.com/tibor-horvath/ci-toolkit/commit/43e64d34ed10436434f27c0f4913ff6ab602ad0d))
* bump actions/setup-dotnet from 4.3.1 to 6.0.0 ([#14](https://github.com/tibor-horvath/ci-toolkit/issues/14)) ([8afb1eb](https://github.com/tibor-horvath/ci-toolkit/commit/8afb1eb8f419d140736a074e38a52d643d350a81))
* bump dorny/test-reporter from 1 to 3 ([#11](https://github.com/tibor-horvath/ci-toolkit/issues/11)) ([e2aea37](https://github.com/tibor-horvath/ci-toolkit/commit/e2aea37a6fe37318a9366de1ec7cb6ea6b6dfdeb))
* bump googleapis/release-please-action from 4.4.1 to 5.0.0 ([#12](https://github.com/tibor-horvath/ci-toolkit/issues/12)) ([204592e](https://github.com/tibor-horvath/ci-toolkit/commit/204592e3253bd6adfc853213229496153a61995d))

## [1.7.0](https://github.com/tibor-horvath/ci-toolkit/compare/v1.6.0...v1.7.0) (2026-08-30)


### Added

* rename CI job to dotnet and update documentation for clarity ([#7](https://github.com/tibor-horvath/ci-toolkit/issues/7)) ([c08814c](https://github.com/tibor-horvath/ci-toolkit/commit/c08814cf691f73f095d997d21b9a60400a5648d4))

## [1.6.0](https://github.com/tibor-horvath/ci-toolkit/compare/v1.5.1...v1.6.0) (2026-06-24)


### Added

* add reusable workflows for NuGet publishing and Docker builds, and update documentation ([b1860cd](https://github.com/tibor-horvath/ci-toolkit/commit/b1860cde0bc6524d269565361cd7d16fbf50f1b3))

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
