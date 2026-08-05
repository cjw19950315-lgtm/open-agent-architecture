# Open Agent Architecture (OAA)

> Governance-first Agent Runtime and Reference Architecture.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.4.0-blue.svg)](CHANGELOG.md)
[![CI: verify](https://img.shields.io/badge/CI-verify-brightgreen.svg)](.github/workflows/verify.yml)

**Open Agent Architecture (OAA)** is a runnable Agent Runtime whose design puts governance first: every task goes through a control plane, a dynamic skill router, a parallel DAG executor, an agent loop, a verification gate, durable session checkpoints, and a chained SHA-256 execution receipt. It also ships as a reference architecture for teams that want the same guardrails in their own agents.

It runs offline out of the box with a deterministic provider, and supports pluggable model providers (OpenAI-compatible adapter included).

---

## 🧭 Positioning

What OAA is:

- A **real, runnable runtime** (`python -m oaa run "..."`), not a slide deck.
- A **governance-first design**: verification gates, human-only ground-truth writes, zero-trust path isolation, and chained receipts are first-class runtime components, not add-ons.
- A **reference architecture**: MIT-licensed specs and JSON-Schema contracts you can adopt independently of this codebase.

What OAA is not (yet):

- Not a production agent framework with a server, MCP ecosystem, or managed persistence — see [ROADMAP.md](ROADMAP.md).
- Not a model vendor: OpenAI/Claude/DeepSeek adapters are pluggable, but only the offline provider is covered by CI today.

---

## 🌐 Multi-Language Documentation

- 🇺🇸 [English](README.md)
- 🇨🇳 [简体中文](docs/i18n/README.zh-CN.md)
- 🇯🇵 [日本語](docs/i18n/README.ja.md)
- 🇪🇸 [Español](docs/i18n/README.es.md)
- 🇩🇪 [Deutsch](docs/i18n/README.de.md)

---

## ⚙️ Runtime Quick Start

No API key required. The deterministic provider runs the full chain offline.

```bash
# run a real task through Control Plane -> Skill Router -> DAG -> Agent Loop -> Verification -> Receipt
python examples/real_task.py .
```

Or use the CLI:

```bash
python -m oaa run "Read README.md and pyproject.toml, analyze the project architecture, and write analysis.md" --workspace .

python -m oaa state <task_id> --workspace .
python -m oaa resume <task_id> --workspace .
python -m oaa receipt <task_id> --workspace .
```

Programmatic API:

```python
from oaa.runtime import Runtime

runtime = Runtime(workspace=".")
result = runtime.run("Read README.md and pyproject.toml, analyze the project architecture, and write analysis.md")
print(result["state"])  # PASSED
print(runtime.get_receipt(result["task_id"]))
```

---

## 🔄 Real Execution Path

```
User Request
  -> Control Plane (create/plan/run lifecycle)
  -> Intent Compiler (5 routing dimensions)
  -> Skill Router (registry + match + rank + select)
  -> DAG Planner (read fan-out -> reason -> write -> verify fan-in)
  -> DAG Executor (parallel waves, single-writer lock, retries, timeouts)
  -> Agent Loop (provider prompt -> tool call -> result -> provider)
  -> Verification Gate (secret scan / policy / tests / approval)
  -> Session Harness + Memory (checkpoints, Obsidian vault, evidence)
  -> Chained SHA-256 Receipt
  -> Final Result (state = PASSED/FAILED/CANCELLED)
```

This is the code path implemented in the `oaa` package; the unit tests and CI execute it end to end.

---

## 🚀 Key Features

1. **Control Plane** — task lifecycle, risk assessment, approval hooks, cancellation, retry, resume, final verification.
2. **Intent Compiler** — compresses a prompt into `final_artifact / input_source / primary_action / business_domain / risk_level`.
3. **Dynamic Skill Router** — `SkillRegistry` with `register_skill / discover_skills / match_skill / rank_skills / select_skills` (max 1 primary + 2 auxiliary).
4. **Parallel DAG Executor** — topological scheduling, fan-out/fan-in, per-node timeout, retries, failure propagation, single-writer concurrency. DAG nodes execute in worker threads inside one process; process-level sub-agent isolation is on the roadmap.
5. **Agent Loop** — pluggable `LLMProvider` (offline deterministic provider + optional OpenAI-compatible provider), prompt → model → tool call → result → model.
6. **Tool Runtime** — filesystem tools with workspace path isolation, credential masking, write approvals. Command-policy scaffolding exists; shell execution is intentionally not wired up yet.
7. **Session Harness** — durable checkpoints, resume after process restart, JSON persistence.
8. **Three-Layer Memory** — Ingestion (unconfirmed), Obsidian Ground-Truth Vault (human-only writes, versioned), Session/Evidence stores.
9. **Verification Gate** — secret scan, policy checks, tests, and approval; failures block PASSED.
10. **Chained Receipts** — SHA-256 over task input, intent, plan, tool calls, state transitions, artifacts, verification, environment, and parent receipt.
11. **Zero-Trust Security** — path isolation, secret masking, write approvals.
12. **Observability** — structured logs, spans, execution timeline, metrics.
13. **Runtime API** — `run / resume / cancel / approve / retry / get_state / get_receipt` + CLI.

## Multi-Model Role Binding

The confirmed operating pattern (2026-08-05) separates concerns across models instead of running one model for every role:

| Role | Model | Responsibility |
|---|---|---|
| Orchestrator | Main model | Decompose, decide, arbitrate and summarize; the main window keeps orchestration state only. |
| Implementation lane | DeepSeek V4 Flash | Independent implementation lane; single writer per lane, no concurrent writers for the same artifact. |
| Verification lane | Gemini 3.6 Flash | Parallel read-only preflight and independent final verification, fully separate from implementation. |

Constraints: no intermediate subagent models between the orchestrator and the lanes; a quota-limited lane falls back to any available capable model instead of blocking or silently degrading; the binding changes task routing only and never rewrites history sessions or state. Model providers in the `oaa` runtime remain pluggable, so this binding is a deployment pattern of the reference architecture.

---

## 🧠 Obsidian & Harness Integration

OAA separates memory into three decoupled layers:

| Layer | Role | Format |
|---|---|---|
| **Ingestion** | raw docs, external sources, code indexes | LLM Wiki / searchable index |
| **Ground Truth** | human-confirmed decisions, reviews, experience | Obsidian Markdown Vault |
| **Session** | task state, checkpoints, receipts across sessions | Harness (JSON + git-backed) |

Agents cannot write to the ground-truth vault (`GroundTruthStore` rejects non-human authors); the Harness persists checkpoints and receipts so tasks survive restarts.

See [docs/obsidian-harness-integration.md](docs/obsidian-harness-integration.md) and [docs/governance-model.md](docs/governance-model.md).

---

## 🛡 Governance Model

OAA treats governance as runtime behavior, not documentation:

- **Verification is a gate**: an artifact that fails the gate never reaches `PASSED`.
- **Ground truth is human-owned**: the Obsidian vault rejects agent writes.
- **Execution is auditable**: every task produces a chained receipt with input hash, plan, tool calls, state transitions, artifacts, and verification results.
- **Zero trust by default**: path isolation and credential masking are enforced in the tool layer.

See [docs/governance-model.md](docs/governance-model.md) for the full model.

---

## 📋 The 12 Factors of Autonomous AI Agents

| # | Factor | Implementation |
|---|---|---|
| 1 | Single Control Plane | `oaa/control.py` |
| 2 | Context Budgeting | `oaa/intent.py` + agent message seeding |
| 3 | Structured Outputs & Gates | `oaa/verification.py` + JSON schemas |
| 4 | Controlled Tool Selection | `oaa/skills.py` |
| 5 | Fast-Path Execution | `oaa/runtime.py` direct run path |
| 6 | Memory Separation | `oaa/memory.py` (Obsidian vault + Harness) |
| 7 | Auditable DAG | `oaa/dag.py` |
| 8 | Cryptographic Receipts | `oaa/receipt.py` |
| 9 | Self-Evolution & Precondition Memory | skill preconditions + harness checkpoints |
| 10 | Zero-Trust Security Boundary | `oaa/security.py` |
| 11 | Ecosystem Multi-Language Support | docs in EN/ZH/JA/ES/DE |
| 12 | Independent Delivery & Gates | `scripts/verify_architecture.py` + CI |

---

## 💻 Tests

```bash
python -m unittest discover -s tests -v
```

Tests cover: real end-to-end task chain, resume after process restart, DAG parallel fan-out/fan-in, path isolation, ground-truth write protection, receipt chaining, verification rejection, state-machine guards, and CLI smoke.

---

## 🗺 Roadmap

Honest, prioritized roadmap (no promises): MCP adapter, HTTP server, SQLite/Postgres persistence, OpenTelemetry, process-level sub-agent isolation, pause/resume approval, real model E2E tests, PyPI publishing. Details: [ROADMAP.md](ROADMAP.md).

---

## 📊 Repository Structure

```
open-agent-architecture/
├── README.md                           # Main documentation
├── CODE_OF_CONDUCT.md                  # Community standards
├── CONTRIBUTING.md                     # Contribution guide
├── SECURITY.md                         # Security policy
├── CHANGELOG.md                        # Release history
├── ROADMAP.md                          # Honest roadmap
├── LICENSE                             # MIT License
├── pyproject.toml                      # Package configuration
├── .github/
│   ├── workflows/verify.yml            # CI: gate + tests + real task
│   ├── workflows/release.yml           # CI: release on version tags
│   ├── ISSUE_TEMPLATE/                 # Bug report + feature request
│   └── pull_request_template.md
├── oaa/                                # Runnable Agent Runtime
│   ├── runtime.py                      # Public Runtime API
│   ├── control.py                      # Control Plane
│   ├── intent.py                       # Intent Compiler
│   ├── skills.py                       # Skill Registry + Router
│   ├── tools.py                        # Tool Runtime
│   ├── dag.py                          # DAG Planner + Executor
│   ├── agents.py                       # LLM Provider + Agent Loop
│   ├── harness.py                      # Session Harness
│   ├── memory.py                       # Ingestion / Obsidian / Evidence
│   ├── verification.py                 # Verification Gate
│   ├── receipt.py                      # Chained SHA-256 Receipts
│   ├── security.py                     # Path isolation / masking / approvals
│   ├── observability.py                # Spans / logs / metrics
│   └── cli.py                          # CLI entry
├── docs/
│   ├── i18n/                           # ZH / JA / ES / DE READMEs
│   ├── governance-model.md             # Governance-first model
│   └── obsidian-harness-integration.md # Memory separation pattern
├── spec/
│   ├── 12-factor-agent-spec.md         # 12-Factor specification
│   ├── skill-routing-spec.md           # Skill routing specification
│   └── architecture-contract.json      # Machine-readable contract
├── schemas/
│   ├── architecture-contract.schema.json
│   └── skill-registry.schema.json
├── scripts/
│   └── verify_architecture.py          # Automated verification gate
├── examples/
│   └── real_task.py                    # Real end-to-end task
└── tests/
    └── test_runtime.py                 # Runtime unit tests
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
