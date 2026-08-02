# Open Agent Architecture (OAA)

> A runnable 12-Factor Agent Runtime for building, orchestrating, and governing autonomous AI Agent systems.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Architecture: 12-Factor](https://img.shields.io/badge/Architecture-12-Factor-green.svg)](spec/12-factor-agent-spec.md)
[![CI: verify](https://img.shields.io/badge/CI-verify-brightgreen.svg)](.github/workflows/verify.yml)

**Open Agent Architecture (OAA)** is an open-source, runnable Agent Runtime: it provides a control plane, intent compiler, dynamic skill router, parallel DAG executor, agent loop with pluggable model providers, durable session Harness, Obsidian-style ground-truth vault, verification gates, and chained SHA-256 execution receipts. It runs offline out of the box with a deterministic provider, and can be pointed at OpenAI-compatible models.

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
# create a task, plan it, execute it, verify it, and persist a receipt
python -m oaa run "Read README.md and pyproject.toml, analyze the project architecture, and write analysis.md" --workspace .

# inspect task state
python -m oaa state <task_id> --workspace .

# resume a task that was interrupted (session persisted on disk)
python -m oaa resume <task_id> --workspace .

# view the chained execution receipt
python -m oaa receipt <task_id> --workspace .
```

Programmatic API:

```python
from oaa.runtime import Runtime

runtime = Runtime(workspace=".")
result = runtime.run("Read README.md and pyproject.toml, analyze the project architecture, and write analysis.md")
print(result["state"])          # PASSED
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
  -> Verification Gate (schema / policy / secret scan / tests / approval)
  -> Session Harness + Memory (checkpoints, vault, evidence)
  -> Chained SHA-256 Receipt
  -> Final Result (state = PASSED/FAILED/CANCELLED)
```

This is the real code path implemented in the `oaa` package, not a diagram-only claim.

---

## 🚀 Key Features

1. **Control Plane** — task lifecycle, risk assessment, approval hooks, cancellation, retry, resume, final verification.
2. **Intent Compiler** — compresses a prompt into `final_artifact / input_source / primary_action / business_domain / risk_level`.
3. **Dynamic Skill Router** — `SkillRegistry` with `register_skill / discover_skills / match_skill / rank_skills / select_skills` (max 1 primary + 2 auxiliary).
4. **Parallel DAG Executor** — topological scheduling, fan-out/fan-in, per-node timeout, retries, failure propagation, single-writer concurrency.
5. **Agent Loop** — pluggable `LLMProvider` (offline deterministic provider + optional OpenAI-compatible provider), prompt → model → tool call → result → model.
6. **Tool Runtime** — filesystem tools with workspace path isolation, credential masking, command policy, and approval gate.
7. **Session Harness** — durable checkpoints, resume after process restart, JSON persistence.
8. **Three-Layer Memory** — Ingestion (unconfirmed), Obsidian Ground-Truth Vault (human-only writes, versioned), Session/Evidence stores.
9. **Verification Gate** — schema validation, policy checks, secret scan, tests, and approval; failures block PASSED.
10. **Chained Receipts** — SHA-256 over task input, intent, plan, tool calls, state transitions, artifacts, verification, environment, and parent receipt.
11. **Zero-Trust Security** — path isolation, secret masking, command allowlist, write approvals.
12. **Observability** — structured logs, spans, execution timeline, metrics.
13. **Runtime API** — `run / resume / cancel / approve / retry / get_state / get_receipt` + CLI.

---

## 🧠 Obsidian & Harness Integration

OAA separates memory into three decoupled layers:

| Layer | Role | Format |
|---|---|---|
| **Ingestion** | raw docs, external sources, code indexes | LLM Wiki / searchable index |
| **Ground Truth** | human-confirmed decisions, reviews, experience | Obsidian Markdown Vault |
| **Session** | task state, checkpoints, receipts across sessions | Harness (JSON + git-backed) |

Agents cannot write to the ground-truth vault (`GroundTruthStore` rejects non-human authors); the Harness persists checkpoints and receipts so tasks survive restarts.

See [docs/obsidian-harness-integration.md](docs/obsidian-harness-integration.md) for the full pattern.

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
| 7 | Auditable Multi-Agent DAG | `oaa/dag.py` |
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

Tests cover: real end-to-end task chain, resume after process restart, DAG parallel fan-out/fan-in, path isolation, ground-truth write protection, and receipt chaining.

---

## 📊 Repository Structure

```
open-agent-architecture/
├── README.md                           # Main English documentation
├── CONTRIBUTING.md                     # Contribution guide
├── SECURITY.md                         # Security policy
├── CHANGELOG.md                        # Release history
├── LICENSE                             # MIT License
├── pyproject.toml                      # Package configuration
├── .github/workflows/verify.yml        # CI: gate + tests + real task
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