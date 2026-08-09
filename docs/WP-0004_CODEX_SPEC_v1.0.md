# WP-0004 — Environment Example Template

Version: v1.0
Project: HEALTH_IS_ALL
Baseline branch: `main`
Working branch: `codex/wp-0004-env-example`

## Purpose

Create a repository-root `.env.example` from only environment variable names that are observable in application code, README documentation, CI configuration, or compose configuration. The template must never contain a real secret, token, password, or production address.

## Allowed files

- `.env.example`
- `docs/WP-0004_CODEX_SPEC_v1.0.md`
- `docs/CODEX_HANDOVER_WP-0004.md`
- `docs/ENVIRONMENT_TEMPLATE_IMPLEMENTATION.md`
- `docs/WP-0004_RESULT.md`

## Evidence and value rules

- Include a variable only when a tracked repository artifact explicitly names it.
- Use an empty value or a safe non-production placeholder.
- Do not copy values from compose files, local environment files, logs, history, or any external system.
- Record unconfirmed candidate names as `UNKNOWN`; do not add them to the template.

## Prohibited actions

Do not modify code, API contracts, databases, migrations, `.env`, `.gitignore`, dependencies, lock files, generated files, or product behavior.

## Verification and publication

- Run `git diff --check`, `scripts/check_patch005_integrity.py`, and `scripts/check_canonical_constants.py`; record all outcomes accurately.
- Confirm only the allowed files changed.
- Commit only the allowed files, push the working branch, and create a Draft PR targeting `main`.
- Do not push directly to `main` or merge the PR.
