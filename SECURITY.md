# Security Policy

## Supported Versions

The latest `main` branch is supported. Releases are tagged in `CHANGELOG.md`.

## Reporting a Vulnerability

Please do **not** open a public issue for security vulnerabilities. Report privately through GitHub Security Advisories:

<https://github.com/cjw19950315-lgtm/open-agent-architecture/security/advisories/new>

Include:

- affected file and version
- a minimal reproduction
- impact description

We aim to respond within 7 days and coordinate a fix before public disclosure.

## Project Rules

- No credentials, API keys, or private paths in this repository.
- All workspace writes are sandboxed; destructive operations require explicit approval.
- Execution receipts and contracts are auditable by design.