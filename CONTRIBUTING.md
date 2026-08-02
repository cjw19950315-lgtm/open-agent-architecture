# Contributing to Open Agent Architecture

Thanks for helping improve OAA. This project follows simple, transparent rules so contributions stay reviewable.

## How to Contribute

1. Open an issue for bugs, design questions, or feature ideas before large PRs.
2. Fork the repository and create a feature branch.
3. Keep changes small and focused. One PR should solve one problem.
4. Run the verification gate before submitting:

```bash
python scripts/verify_architecture.py
```

5. Add or update tests/examples when your change affects runtime behavior.

## Standards

- Documentation is maintained in EN (primary) and ZH/JA/ES/DE (i18n).
- JSON contracts must stay valid against the schemas in `schemas/`.
- Never commit credentials, private paths, or personal data.
- Use clear commit messages with a conventional prefix (`feat:`, `fix:`, `docs:`, `ci:`, `test:`).

## Review Process

Maintainers review every PR. CI runs the architecture gate and the demo workflow on every push and pull request. Feedback is welcome; please keep the discussion constructive.