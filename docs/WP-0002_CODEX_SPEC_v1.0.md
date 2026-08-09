# WP-0002 — Canonical Runtime Map

Version: v1.0
Project: HEALTH_IS_ALL
Baseline branch: `main`
Working branch: `codex/wp-0002-canonical-runtime-map`

## Purpose

Establish the canonical runtime and repository path classification from observable evidence: imports, entry points, API calls, execution commands, and database connection relationships. Directory names alone are not evidence.

## Investigation candidates

- `/lib`: Flutter runtime candidate
- `/backend`: FastAPI runtime candidate
- `/02_DATABASE`: database migration candidate
- `/test`: Flutter/Dart test candidate
- `/tests`: backend or other test candidate
- `/scripts`: automation candidate
- `/00_PROJECT`, `/01_ARCHITECTURE`, `/07_PRODUCT`: planning and architecture evidence candidates

## Classification values

Each investigated path must be classified as exactly one of:

- `ACTIVE`: directly used by a current runtime entry point or execution path
- `SUPPORTING`: used by active runtime, tests, tooling, or delivery flow but not itself the primary runtime
- `REFERENCE`: retained evidence or documentation that is useful for understanding but not executed
- `LEGACY`: superseded implementation with evidence of a replacement
- `GENERATED`: output created by tools rather than maintained source
- `UNKNOWN`: evidence is insufficient to make a reliable classification

Do not infer a classification from a directory name. Use `UNKNOWN` when evidence is insufficient.

## Required deliverables

Create:

1. `docs/REPOSITORY_RUNTIME_MAP.md`
2. `docs/REPOSITORY_PATH_CLASSIFICATION.md`

The runtime map must record actual paths and evidence for the flow:

`Flutter entry → navigation/router → screen/state/API client → FastAPI app/router → service/engine → DB/migration`

The classification document must include this table:

`경로 | 분류 | 역할 | 수정 가능 여부 | 판정 근거 | 확인 상태`

## Out of scope

Do not modify product, game, UI, navigation, API contract, database schema or migration, dependencies, lock files, runtime code, generated files, or legacy folders. Do not refactor or move folders.

## Verification and completion

- Verify every documented file path and cited evidence against the repository.
- Run `git diff --check` and confirm with `git status` that only WP-0002 documents changed.
- Run safe existing validation commands when available and record their results.
- Commit only WP-0002 documentation, push the current branch, and create a Draft PR targeting `main`.
- Do not push directly to `main` or merge the PR.
