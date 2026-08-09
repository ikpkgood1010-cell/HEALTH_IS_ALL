# WP-0003 — Database and Environment Governance

Version: v1.0
Project: HEALTH_IS_ALL
Baseline branch: `main`
Working branch: `codex/wp-0003-db-env-governance`

## Purpose

Determine, from repository evidence, whether `/02_DATABASE` has an actual database-application tool, command, or accountable owner, and whether `.env.example` is needed and how it should be governed.

## Scope

Investigation and documentation only. Inspect repository configuration, launch commands, automation, database connection code, migration files, version control state, and documentation. Never expose secret values.

## Required deliverables

Create:

1. `docs/DATABASE_MIGRATION_RUNTIME_DECISION.md`
2. `docs/ENVIRONMENT_TEMPLATE_DECISION.md`
3. `docs/WP-0003_RESULT.md`

## Decision rule

Record a database-application path or environment-template requirement only when an observable repository artifact proves it. When evidence is absent or insufficient, record `UNKNOWN`; do not infer an owner, command, or configuration policy.

## Prohibited actions

Do not modify or execute DB SQL, schemas, migrations, application code, `.env`, `.env.example`, API contracts, dependencies, lock files, generated files, or product behavior. Do not create environment files.

## Completion gate

- Verify every cited path and evidence.
- Confirm only WP-0003 documentation files changed with `git diff --check` and `git status`.
- Commit only documentation, push the working branch, and create a Draft PR targeting `main`.
- Do not push directly to `main` or merge the PR.
