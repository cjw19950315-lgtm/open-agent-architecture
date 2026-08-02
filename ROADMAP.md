# Roadmap

This is an honest, prioritized roadmap. Items are not promises; they reflect current engineering direction. Core architecture will not be replaced — these items extend the existing runtime.

## Priority 1 (next)

- [ ] MCP adapter: expose OAA tools/skills as MCP tools and consume external MCP servers.
- [ ] SQLite persistence backend for sessions, checkpoints, and evidence (replacing JSON-only storage).
- [ ] HTTP server (FastAPI or stdlib) exposing `run / resume / cancel / approve / retry / state / receipt`.

## Priority 2

- [ ] OpenTelemetry integration: traces, spans, and metrics export.
- [ ] Pause/resume approval: write denials transition tasks to `WAITING_APPROVAL` and resume on human decision.
- [ ] Real model E2E tests for the OpenAI-compatible provider (requires CI credentials or BYO-key test harness).

## Priority 3

- [ ] Process-level sub-agent isolation (DAG nodes currently run in worker threads).
- [ ] Command policy wired into a sandboxed shell tool.
- [ ] Postgres/Redis backends for multi-instance deployments.
- [ ] PyPI publishing and signed releases.

## Non-goals

- Replacing the core architecture.
- Becoming a model vendor.
- Adding features that weaken governance guarantees (verification gates, human-owned ground truth, chained receipts).