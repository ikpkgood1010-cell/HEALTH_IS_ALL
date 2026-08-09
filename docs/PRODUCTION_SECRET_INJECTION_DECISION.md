# Production Secret Injection Decision

## Decision

**Status: UNKNOWN — no production secret-injection mechanism or accountable owner is proven by the repository.**

The repository contains compose environment declarations and application environment lookups, but neither demonstrates how production values are stored, injected, rotated, audited, or approved. No CI configuration or secret-management integration is tracked.

## Confirmed boundaries

- FastAPI reads settings from the process environment in `backend/config.py`.
- Docker/compose files declare environment entries for backend and PostgreSQL services.
- Flutter receives `API_BASE_URL` via compile-time `--dart-define`, not a proven `.env` loader.
- WP-0004 supplies a placeholder-only example on its own branch; it does not inject a value.

## What remains unproven

| Decision area | Status | Required deciding role |
| --- | --- | --- |
| Production secret store or platform facility | UNKNOWN | Deployment/platform owner with security review |
| Injection path to backend and database containers | UNKNOWN | Deployment/platform owner |
| Injection path for Flutter build-time values | UNKNOWN | Mobile/web release owner |
| Rotation, access control, audit trail, and incident response | UNKNOWN | Security owner and service owner |
| Named repository owner or `CODEOWNERS` governance | UNKNOWN | Repository maintainer |
| CI-backed protected variable mechanism | CI 미구성 또는 저장소 근거 없음 | Repository maintainer and deployment owner |

## Possible choices, not a selection

A future approved deployment decision may evaluate a managed platform secret store, protected CI/CD variables, or container-orchestrator secret facilities. This WP does not select, configure, or create any of them. The decision must be made by the named deployment/platform owner with security approval and recorded in a separately approved work package.
