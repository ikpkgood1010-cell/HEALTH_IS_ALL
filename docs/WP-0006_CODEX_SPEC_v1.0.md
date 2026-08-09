# WP-0006 — Secret Operation Governance

## Purpose

Establish documentation-only operating standards for MVP and long-term production secret handling. Do not create a secret, configure a platform, or change deployment behavior.

## Required documents

- `docs/PRODUCTION_SECRET_OPERATION_STANDARD.md`
- `docs/SECRET_LIFECYCLE_AND_ACCESS_POLICY.md`
- `docs/WP-0006_RESULT.md`

## Decisions supplied for this WP

- Choose Render, Railway, AWS, or GCP only immediately before MVP deployment.
- Store MVP secrets in the chosen platform's Environment Variables.
- Use GitHub Secrets only for CI work after CI is actually configured.
- Use AWS Secrets Manager or GCP Secret Manager for long-term secret management.
- The current owner is the developer; long-term ownership transfers to DevOps/infrastructure or security.

## Constraints

Only WP-0006 documentation may change. Never create or disclose actual secrets, tokens, passwords, connection strings, CI files, platform settings, environment files, or runtime changes.
