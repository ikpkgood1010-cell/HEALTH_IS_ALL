# Codex Handover — WP-0004

## Scope

Work only on `codex/wp-0004-env-example`, compared with `main`. This is a documentation and safe-template work package; only the five paths listed in the WP-0004 specification may change.

## Source-of-truth rules

Inspect tracked code, README files, CI files when present, and compose configuration. Treat an explicit environment-key lookup or configuration declaration as evidence. Do not inspect, copy, or emit local environment values.

Use blank values for variables that accept sensitive values. A URL placeholder may be used only when it is clearly non-production and contains no secret material. Do not include a key merely because it is conventional.

## Required records

`docs/ENVIRONMENT_TEMPLATE_IMPLEMENTATION.md` must identify the evidence path for every included variable and explain its safe example value. `docs/WP-0004_RESULT.md` must report validation results and any `UNKNOWN` candidates.

## Handoff gate

Before committing, verify the allowed file list and `git diff --check`. Run both required scripts without modifying configuration or generated files. Push a Draft PR to `main`, verify the working tree is clean, and stop for review.
