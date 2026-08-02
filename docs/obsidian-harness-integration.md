# Obsidian & Harness Integration Pattern

Version: 1.0.0

## Goal

Keep AI-generated content from silently overwriting human decisions, and let long-running agent work survive context compaction.

## Three Memory Layers

| Layer | Owner | Content | Storage |
|---|---|---|---|
| Ingestion | AI pipeline | raw docs, external sources, code indexes | LLM Wiki / searchable index |
| Ground Truth | Human maintainer | confirmed decisions, reviews, experience | Obsidian Markdown Vault |
| Session | Agent runtime | task state, checkpoints, receipts | Harness (JSON + git-backed) |

## Rules

1. Human-confirmed Obsidian notes are authoritative over AI-generated summaries.
2. The Harness writes checkpoints (recommended every 15 minutes) and SHA-256 receipts; it never edits the Obsidian vault directly.
3. Ingestion results are always labeled as unconfirmed until a human reviews them.
4. No credentials, private paths, or personal data are stored in any of the three layers.

## Data Flow

```
Task session (Harness)
        | checkpoint + SHA-256 receipt
        v
Review step (human)
        | confirmed decision
        v
Obsidian Markdown Vault (ground truth)
        | guard rules
        v
Skill routing & precondition memory (next sessions)
```

## Implementation Notes

- Obsidian vault entries follow a stable frontmatter schema (id, type, status, source, updated_at).
- Harness receipts are plain JSON with `input_summary_sha256`, `artifact_sha256`, `terminal_state`, and timestamps.
- Session resume reads the latest Harness checkpoint, then verifies receipt hashes before continuing.
- This pattern is storage-agnostic: any Markdown vault and JSON checkpoint store can replace the reference implementation.