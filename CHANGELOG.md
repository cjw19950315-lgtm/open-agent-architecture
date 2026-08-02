# Changelog

All notable changes to this project are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.3.0] - 2026-08-02

### Added

- Governance-first positioning: README, governance model doc, and contract updated.
- CODE_OF_CONDUCT.md, ROADMAP.md, docs/governance-model.md.
- GitHub issue templates (bug report / feature request) and pull request template.
- Release workflow (`release.yml`) triggered by `v*` tags.
- Extended tests: verification rejection, state-machine guards, manual-approval failure path, CLI smoke, ground-truth versioning.

### Changed

- README claims corrected to match implementation (DAG nodes run in worker threads; command policy is scaffolding; OpenAI adapter optional/untested in CI).
- Architecture contract no longer references external LazyCodex executor; points to in-repo implementation.
- Version metadata and package metadata aligned to 1.3.0.
## [1.2.0] - 2026-08-02

### Added

- Runnable `oaa` Agent Runtime package: control plane, intent compiler, dynamic skill router, parallel DAG executor, agent loop with pluggable model providers, tool runtime, session harness, three-layer memory, verification gate, chained SHA-256 receipts, observability, and CLI.
- Runtime API: `run / resume / cancel / approve / retry / get_state / get_receipt`.
- End-to-end unit tests (`tests/test_runtime.py`) covering real task chain, resume after restart, DAG parallelism, path isolation, ground-truth protection, and receipt chaining.
- Real task example (`examples/real_task.py`).
- CI now runs unit tests and the real end-to-end task.
- Offline deterministic provider so the runtime runs without API keys; optional OpenAI-compatible provider.

## [1.1.0] - 2026-08-02

### Added

- Obsidian ground-truth vault and session Harness layers added to spec, contract, and docs.
- CONTRIBUTING.md, SECURITY.md, and CHANGELOG.md.
- GitHub Actions CI (`verify.yml`) running architecture gate + demo workflow.
- README polish: features, architecture diagram, memory-layer table.

### Fixed

- UTF-8 mojibake in multilingual docs (literal `?` placeholders replaced with correct characters).
- Broken links to spec files in README.
- Wrong clone URL in README quick start.

## [1.0.0] - 2026-08-02

### Added

- Initial 12-Factor Agent Architecture framework.
- Dynamic skill routing specification and machine-readable architecture contract.
- Multi-language documentation (EN/ZH/JA/ES/DE).
- Verification gate script and runnable demo workflow.