# Codex Handover — WP-0003

## Branch and allowed files

- Work only on `codex/wp-0003-db-env-governance`.
- Compare against `main`.
- Only these five documentation files may change:
  - `docs/WP-0003_CODEX_SPEC_v1.0.md`
  - `docs/CODEX_HANDOVER_WP-0003.md`
  - `docs/DATABASE_MIGRATION_RUNTIME_DECISION.md`
  - `docs/ENVIRONMENT_TEMPLATE_DECISION.md`
  - `docs/WP-0003_RESULT.md`

## Evidence standard

Use only observable repository evidence: executable launch commands, CI/workflow configuration, migration-tool configuration, source imports, SQL runners, version-control metadata, and repository documentation. Cite paths and describe evidence without copying credential values.

Use `UNKNOWN` for a missing DB application tool, command, responsibility owner, or environment-template requirement. Do not invent remediation steps that modify a protected file.

## Protection and publication

- Do not execute or edit SQL, migrations, schema, code, `.env`, `.env.example`, APIs, dependencies, lock files, or generated files.
- Do not delete, untrack, rename, or relocate existing files.
- Run documentation-safe verification only; record failures accurately.
- Create a Draft PR to `main` after push, then wait for review without merging.
