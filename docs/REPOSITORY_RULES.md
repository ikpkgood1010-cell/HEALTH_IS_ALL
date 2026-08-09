# Repository Working Rules

## Canonical runtime

- Flutter runtime: `/lib`
- FastAPI runtime: `/backend`
- Database migration and schema evidence: `/02_DATABASE`
- Flutter/Dart tests: `/test`
- Backend and other tests: `/tests`
- Validation and automation: `/scripts`

`apps/mobile/` and `packages/*` are not canonical runtime paths and must not be created as a side effect of maintenance work.

## Allowed change scope

- Make the smallest change that directly implements the approved work package.
- Preserve existing repository layout unless the approved work package explicitly changes it.
- For WP-0001, changes are limited to `.gitignore`, `docs/REPOSITORY_SECURITY.md`, and `docs/REPOSITORY_RULES.md`.

## Prohibited changes

- Do not rewrite or delete existing source code, planning evidence, or legacy directories without explicit approval.
- Do not modify Flutter screens, FastAPI endpoints, navigation, dependencies, or database schema during hygiene-only work.
- Do not create a new greenfield directory structure as part of an unrelated task.

## Database migration protection

- Treat `/02_DATABASE` as protected evidence and migration material.
- Do not edit, rename, delete, or regenerate migrations without an explicitly approved database work package.
- Review migration diffs independently before merge.

## API contract protection

- Do not change endpoint paths, request/response models, authentication behavior, or externally consumed payloads without an approved API-contract change.
- Include compatible tests when an approved API change is made.

## Codex working rules

- Inspect the repository and relevant Git history before changing files.
- Never place credential values in chat output, documentation, commits, issues, or pull-request text.
- Check tracked state before removing generated artifacts; use a separately reviewed cleanup for existing tracked output.
- List every changed file and explicitly justify every deletion.
- Keep changes focused and preserve unrelated user work.

## Branch and pull-request rules

- Branch from the approved baseline (currently `main`) and use a task-specific branch.
- Keep one coherent work package per pull request.
- Describe scope, verification, residual risk, and any deferred cleanup in the pull request.
- Obtain review before merging security-sensitive or migration-related changes.

## Test rules

- Run the narrowest relevant validation for the approved change, then broaden it when the change affects runtime behavior.
- Hygiene-only changes must at least verify the changed file set, ignore behavior, and that protected runtime paths were not modified.
- Do not claim tests passed when the required runtime or test tooling was not run.
