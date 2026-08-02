# Open Agent Architecture (OAA)

> Production-grade architecture for building, orchestrating, and governing autonomous AI Agent systems.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Architecture: 12-Factor](https://img.shields.io/badge/Architecture-12-Factor-green.svg)](spec/12-factor-agent-spec.md)
[![CI: verify](https://img.shields.io/badge/CI-verify-brightgreen.svg)](.github/workflows/verify.yml)
[![Codex for OSS](https://img.shields.io/badge/Codex%20for%20OSS-Apply-000000.svg)](https://openai.com/zh-Hans-CN/form/codex-for-oss/)

**Open Agent Architecture (OAA)** is an open-source reference framework for governing autonomous AI agents. It implements the **12-Factor Agent Architecture**, dynamic skill routing, auditable multi-agent DAG execution, and a **session Harness** with an **Obsidian Markdown Vault** as the human ground-truth layer.

---

## 🌐 Multi-Language Documentation

- 🇺🇸 [English](README.md)
- 🇨🇳 [简体中文](docs/i18n/README.zh-CN.md)
- 🇯🇵 [日本語](docs/i18n/README.ja.md)
- 🇪🇸 [Español](docs/i18n/README.es.md)
- 🇩🇪 [Deutsch](docs/i18n/README.de.md)

---

## 🚀 Key Features

1. **12-Factor Agent Principles** — clear separation of Control Plane, Context Budgeting, Verification Gates, and deterministic state reducers.
2. **Dynamic Skill Routing Engine** — intent compression, metadata recall, precondition memory, and bounded tool selection (max 1 primary + 2 secondary skills).
3. **Auditable Multi-Agent DAG** — isolated sub-agent execution with bounded timeouts, single-writer concurrency, and SHA-256 execution receipts.
4. **Zero-Trust Security Boundary** — workspace sandboxing, credential masking, and explicit write approvals.
5. **Obsidian Ground-Truth Vault** — human-confirmed decisions, reviews, and long-term experience live in a Markdown vault.
6. **Session Harness** — cross-session task state, checkpoints, and cryptographic receipts survive compaction and restarts.
7. **Multi-Model & Provider Agnostic** — OpenAI GPT / Codex, Claude, DeepSeek, and local LLM runtimes.

---

## 🧠 Obsidian & Harness Integration

OAA separates memory into three decoupled layers:

| Layer | Role | Format |
|---|---|---|
| **Ingestion** | raw docs, external sources, code indexes | LLM Wiki / searchable index |
| **Ground Truth** | human-confirmed decisions, reviews, experience | Obsidian Markdown Vault |
| **Session** | task state, checkpoints, receipts across sessions | Harness (JSON + git-backed) |

This separation prevents AI-generated content from silently overwriting human decisions, and lets long-running agent work resume after context compaction.

See [docs/obsidian-harness-integration.md](docs/obsidian-harness-integration.md) for the full pattern.

---

## 🏗 System Architecture Diagram

```
+-------------------------------------------------------------------+
|                        User / API Request                         |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|               Factor 1: Single Control Plane (Codex)               |
|   - Intent Compression      - Risk Assessment & Approvals         |
|   - Task Contract           - Final Verification & Receipt        |
+-------------------------------------------------------------------+
                                  |
            +---------------------+---------------------+
            |                                           |
            v                                           v
+-----------------------+                   +-----------------------+
|  Factor 4: Skill      |                   |  Factor 7: DAG        |
|  Routing Engine       |                   |  Orchestrator (OMO)   |
| - Precondition Memory |                   | - Sub-agent DAG       |
| - Tool Selection Gate |                   | - Parallel Explorer   |
+-----------------------+                   +-----------------------+
            |                                           |
            +---------------------+---------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|       Factor 3: Executor / QA / Gate Layer (LazyCodex)            |
|   - Sandboxed Execution       - Cryptographic Receipt Generator   |
|   - Automated Linting         - Precondition Guard Verification   |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|            Factor 6: Multi-Layer Memory & Fact Store              |
|   - Ingestion: LLM Wiki        - Ground Truth: Obsidian Vault     |
|   - Session: Harness           - Evidence: SHA-256 Receipts       |
+-------------------------------------------------------------------+
```

---

## 📋 The 12 Factors of Autonomous AI Agents

| # | Factor | Description |
|---|---|---|
| 1 | **Single Control Plane** | One orchestrator retains final authority, risk evaluation, and user delivery. |
| 2 | **Context Budgeting** | Strict token management, progressive disclosure, and compaction-resilient history. |
| 3 | **Structured Outputs & Gates** | All tool responses and state transitions use verifiable schemas and QA gates. |
| 4 | **Controlled Tool Selection** | Dynamic skill discovery with max 1 primary + 2 secondary skills per turn. |
| 5 | **Fast-Path Execution** | Non-blocking execution paths for local operations, fallbacks, and offline diagnostics. |
| 6 | **Memory Separation** | Ingestion (LLM Wiki), human ground truth (Obsidian Vault), and session Harness are strictly decoupled. |
| 7 | **Auditable Multi-Agent DAG** | Sub-agents run isolated DAGs with bounded timeouts and single-writer concurrency. |
| 8 | **Cryptographic Receipts** | Every output emits reproducible execution receipts signed by SHA-256 state hashes. |
| 9 | **Self-Evolution & Feedback Loop** | Automated capture of execution failures into precondition memory guards. |
| 10 | **Zero-Trust Security Boundary** | File system sandboxing, credential masking, and mandatory write approvals. |
| 11 | **Ecosystem Multi-Language Support** | Documentation, schemas, and runtime errors support EN/ZH/JA/ES/DE. |
| 12 | **Independent Delivery & Gates** | Architecture verification is decoupled from external deployment blocks. |

---

## 💻 Quick Start

```bash
git clone https://github.com/cjw19950315-lgtm/open-agent-architecture.git
cd open-agent-architecture
pip install -e .
```

```bash
# Run the architecture verification gate
python scripts/verify_architecture.py

# Run the sample 12-Factor agent workflow
python examples/demo_agent_workflow.py
```

---

## 📊 Repository Structure

```
open-agent-architecture/
├── README.md                           # Main English documentation
├── CODEX_FOR_OSS_APPLICATION.md        # Codex for OSS application kit
├── CONTRIBUTING.md                     # Contribution guide
├── SECURITY.md                         # Security policy
├── CHANGELOG.md                        # Release history
├── LICENSE                             # MIT License
├── pyproject.toml                      # Package configuration
├── .github/workflows/verify.yml        # CI: architecture + demo gates
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
└── examples/
    └── demo_agent_workflow.py          # Runnable 12-Factor demo
```

---

## 🏅 OpenAI Codex for OSS Program

This repository is maintained as an open-source reference implementation for autonomous agent governance. We apply to the **OpenAI Codex for Open Source** program to support 6 months of ChatGPT Pro with Codex, Codex Security, and API-credit infrastructure for maintainer automation.

- Official form (中文): <https://openai.com/zh-Hans-CN/form/codex-for-oss/>
- Official form (English): <https://openai.com/form/codex-for-oss/>
- Field-by-field application kit: [CODEX_FOR_OSS_APPLICATION.md](CODEX_FOR_OSS_APPLICATION.md)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).