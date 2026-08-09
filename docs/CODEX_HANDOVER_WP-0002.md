# Codex Handover — WP-0002

## Branch and scope

- Work only on `codex/wp-0002-canonical-runtime-map`.
- Use `main` as the comparison baseline.
- This work package is documentation-only. The four WP-0002 documents are the only permitted changed files:
  - `docs/WP-0002_CODEX_SPEC_v1.0.md`
  - `docs/CODEX_HANDOVER_WP-0002.md`
  - `docs/REPOSITORY_RUNTIME_MAP.md`
  - `docs/REPOSITORY_PATH_CLASSIFICATION.md`

## Evidence method

Inspect source imports, configured entry points, startup commands, router registrations, HTTP client calls, service/engine calls, database configuration, migration files, and test configuration. Record exact repository-relative paths. Never record credential values.

When a path has no confirmed runtime relationship, classify it as `UNKNOWN`; do not label it legacy merely because it appears old.

## Protection rules

- Do not edit `/lib`, `/backend`, `/02_DATABASE`, `/test`, `/tests`, `/scripts`, planning evidence, dependencies, lock files, or generated artifacts.
- Do not delete, untrack, rename, or relocate existing files.
- Do not change UI, navigation, API, migrations, schema, or feature behavior.

## Handoff gate

Before publication, confirm the changed-file list contains only the four permitted documentation files, run `git diff --check`, run safe existing validation where available, and ensure the working tree is clean after push and PR creation. Create a Draft PR to `main`; await human or review-AI approval without merging.
