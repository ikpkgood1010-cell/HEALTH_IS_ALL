# WP-0005 — Runtime Configuration and Secret Governance

## Purpose

Document evidence-backed loading locations, precedence, local value provision, production value provision, and ownership for repository environment variables. Document production secret injection only to the extent the repository proves it.

## Required deliverables

- `docs/RUNTIME_CONFIGURATION_GOVERNANCE.md`
- `docs/PRODUCTION_SECRET_INJECTION_DECISION.md`
- `docs/WP-0005_RESULT.md`

## Rules

Use only tracked code, README, Docker/compose, launch scripts, deployment documents, GitHub-related paths, `.gitignore`, and the read-only WP-0004 branch evidence. Mark missing evidence as `UNKNOWN`. Do not emit a secret, token, password, or connection string.

Do not create CI, secret-management tools, loaders, or configuration files. Do not modify `.env`, `.env.example`, code, Docker/compose, CI, GitHub settings, databases, dependencies, lock files, or generated artifacts.

## Publication

Verify cited paths and variable uses, verify no secrets in documentation, run the two required scripts, confirm documentation-only changes, then commit, push, and open a Draft PR to `main`.
