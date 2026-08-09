# Supabase DB Implementation Guide

- Set only `DATABASE_URL` as the approved Render runtime Environment Variable. The FastAPI config no longer constructs a URL from component credential fields.
- SQLAlchemy creates the engine only when `DATABASE_URL` exists, with `pool_pre_ping=True` and TLS `sslmode=require`, which supports a Supabase session-pooler URL.
- `/healthz` remains unchanged. `/readyz` reports `not_ready` when the URL is absent without revealing a value. DB-dependent endpoints return HTTP 503 with a generic message.
- Run `python scripts/run_migrations.py --dry-run` to list candidate SQL migrations. It never executes SQL. Applying migrations is blocked until a separate ordering review because `/02_DATABASE` ordering/application evidence remains UNKNOWN.
- Do not put a URL, ref, key, password, or project identifier in Git or this guide.
