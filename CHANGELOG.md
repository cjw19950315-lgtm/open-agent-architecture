# Changelog

All notable changes to this project are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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