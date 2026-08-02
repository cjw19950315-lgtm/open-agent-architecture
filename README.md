# Open Agent Architecture (OAA)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Architecture: 12--Factor](https://img.shields.io/badge/Architecture-12--Factor-green.svg)](docs/12-factor-agent-spec.md)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](scripts/verify_architecture.py)

**Open Agent Architecture (OAA)** is a production-ready, open-source architectural framework for building, orchestrating, and governing autonomous AI Agent systems. It implements the **12-Factor Agent Architecture**, dynamic skill routing, auditable multi-agent DAG execution, and cross-session state harness.

---

## ?? Multi-Language Documentation

- ???? [English](README.md)
- ???? [????](docs/i18n/README.zh-CN.md)
- ???? [???](docs/i18n/README.ja.md)
- ???? [Espa?ol](docs/i18n/README.es.md)
- ???? [Deutsch](docs/i18n/README.de.md)

---

## ?? Key Features

1. **12-Factor Agent Principles**: Clear separation of Control Plane, Context Budgeting, Verification Gates, and Deterministic State Reducers.
2. **Dynamic Skill Routing Engine**: Intent compression algorithm, metadata recall, precondition memory, and sub-agent capability matching.
3. **Session Harness & State Persistence**: Non-blocking fast-path execution, auditable DAG orchestration, and cryptographic execution receipts.
4. **Zero-Trust Security & Privacy Guard**: Automated credential sanitization, workspace sandboxing, and policy enforcement.
5. **Multi-Model & Provider Agnostic**: Native support for OpenAI GPT-5 / Codex, Claude, DeepSeek, and local LLM runtimes.

---

## ?? System Architecture Diagram

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
|   - Ingestion: LLM Wiki     - Human Truth: Markdown Vault        |
|   - Session: Harness        - Evidence: Verified JSON Receipts   |
+-------------------------------------------------------------------+
```

---

## ?? The 12 Factors of Autonomous AI Agents

| # | Factor | Description |
|---|---|---|
| 1 | **Single Control Plane** | One orchestrator retains final authority, risk evaluation, and user delivery. |
| 2 | **Context Budgeting** | Strict token management, progressive disclosure, and compaction-resilient history. |
| 3 | **Structured Outputs & Gates** | All tool responses and state transitions use verifiable schemas and QA gates. |
| 4 | **Controlled Tool Selection** | Dynamic skill discovery with max 1 primary + 2 secondary skills per turn. |
| 5 | **Fast-Path Execution** | Non-blocking execution paths for local operations, fallbacks, and offline diagnostic checks. |
| 6 | **Memory Separation** | Ingestion (Wiki), Human Ground Truth (Vault), and Session Harness are strictly decoupled. |
| 7 | **Auditable Multi-Agent DAG** | Sub-agents run isolated DAGs with bounded timeouts and single-writer concurrency. |
| 8 | **Cryptographic Receipts** | Every output emits reproducible execution receipts signed by SHA-256 state hashes. |
| 9 | **Self-Evolution & Feedback Loop** | Automated capture of execution failures into precondition memory guards. |
| 10 | **Zero-Trust Security Boundary** | File system sandboxing, credential masking, and mandatory write approvals. |
| 11 | **Ecosystem Multi-Language Support** | Internationalization across documentation, schemas, and runtime error messages. |
| 12 | **Independent Delivery & Gates** | System architecture verification is decoupled from external deployment blocks. |

---

## ?? Quick Start

### Installation

```bash
git clone https://github.com/open-agent-architecture/open-agent-architecture.git
cd open-agent-architecture
pip install -e .
```

### Run Architecture Verification

```bash
python scripts/verify_architecture.py
```

### Run Sample Workflow

```bash
python examples/demo_agent_workflow.py
```

---

## ?? Repository Structure

```
open-agent-architecture/
??? README.md                           # Main English documentation
??? pyproject.toml                      # Package build configuration
??? LICENSE                             # MIT License
??? CODEX_FOR_OSS_APPLICATION.md        # OpenAI Codex for OSS application package
??? docs/
?   ??? 12-factor-agent-spec.md         # Detailed 12-Factor specification
?   ??? skill-routing-spec.md           # Dynamic skill routing specification
?   ??? i18n/
?       ??? README.zh-CN.md             # ???? README
?       ??? README.ja.md                # ??? README
?       ??? README.es.md                # Espa?ol README
?       ??? README.de.md                # Deutsch README
??? spec/
?   ??? architecture-contract.json      # Machine-readable architecture contract
??? schemas/
?   ??? architecture-contract.schema.json
?   ??? skill-registry.schema.json
??? scripts/
?   ??? verify_architecture.py          # Automated architecture gate script
??? examples/
    ??? demo_agent_workflow.py          # Runnable 12-Factor agent demo
```

---

## ?? OpenAI Codex for OSS Program

This repository is maintained as an open-source reference implementation for autonomous agent governance. We actively apply for the **OpenAI Codex for Open Source (Codex for OSS)** program to empower open-source AI maintainers with 6 months of ChatGPT Pro, Codex Security, and API credit infrastructure.

For maintainers interested in our grant application template and guidelines, see [`CODEX_FOR_OSS_APPLICATION.md`](CODEX_FOR_OSS_APPLICATION.md).

---

## ?? License

This project is licensed under the [MIT License](LICENSE).
