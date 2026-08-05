# Governance Model

Version: 1.0.0

## Principle

OAA is governance-first: safety and auditability are runtime behavior, not documentation.

## Guarantees

### 1. Verification is a gate

Every task ends with a verification node (`oaa/verification.py`). An artifact that fails secret scanning, policy checks, tests, or approval never reaches `PASSED`.

### 2. Ground truth is human-owned

The Obsidian vault adapter (`oaa/memory.py::GroundTruthStore`) rejects writes from non-human authors (`GroundTruthWriteDenied`). AI-generated content can be ingested, but it cannot silently overwrite human decisions.

### 3. Execution is auditable

Every task produces a chained SHA-256 receipt (`oaa/receipt.py`) containing:

- task input hash
- intent dimensions
- DAG plan
- tool calls (params hash + result hash)
- state transitions
- artifact digests
- verification results
- environment (provider, model config, python, platform)
- parent receipt hash

### 4. Zero trust by default

- `PathPolicy` rejects any path that escapes the workspace.
- `CredentialMasker` redacts secret-like patterns from tool results and artifacts.
- Writes require approval (`ApprovalGate`).

## Enforcement Points

| Guarantee | Runtime component | Fails closed? |
|---|---|---|
| Verification gate | `VerificationGate.verify` | yes |
| Human-owned ground truth | `GroundTruthStore.write_note` | yes |
| Auditability | `ReceiptBuilder.build` + `EvidenceStore` | yes |
| Path isolation | `PathPolicy.resolve` | yes |
| Secret masking | `CredentialMasker.mask` | yes |
| Write approval | `ApprovalGate.request` | yes (auto mode approves; manual mode requires callback) |

## What governance does not cover today

- Pause/resume approval (write denial fails the task instead of waiting) - roadmap.
- Process-level isolation for sub-agents - roadmap.
- OpenTelemetry export - roadmap.

## Multi-Model Role Binding

Confirmed 2026-08-05 as a deployment pattern of the reference architecture:

- The orchestrator is a single main model: it decomposes work, decides, arbitrates, and produces the final summary. The main window keeps orchestration state only.
- An independent implementation lane (DeepSeek V4 Flash) acts as the single writer per lane; no concurrent writers exist for the same artifact.
- A verification lane (Gemini 3.6 Flash) runs a parallel read-only preflight and an independent final verification, fully separate from implementation.

Binding constraints:

- No intermediate subagent models between the orchestrator and the lanes.
- Quota-limited lanes fall back to any available capable model instead of blocking or silently degrading.
- The binding changes task routing only; it never rewrites history sessions or state.
