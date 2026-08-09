# Supabase Connection Decision

## Current backend evidence

- `backend/database.py` uses SQLAlchemy `create_engine`, a session factory, and `pool_pre_ping=True`.
- `backend/config.py` accepts `SQLALCHEMY_DATABASE_URL` before `DATABASE_URL`; when absent it constructs configuration from component DB variables, then has a local SQLite fallback.
- `backend/main.py` calls `init_db()`, and `backend/database.py` uses `Base.metadata.create_all`. This does not apply `/02_DATABASE` SQL files; no migration runner relation is confirmed.

## Decision

Use a **Supabase session pooler connection** for the Render FastAPI service if the selected Supabase project provides it and its documented connection settings meet the selected SQLAlchemy driver requirements. FastAPI is a long-running server and Render network/IP capability is not proven in this repository; session pooling is the appropriate candidate to validate before deployment. Direct connection and transaction pooler remain **UNKNOWN/not selected** until dashboard-provided compatibility details are reviewed. Do not configure a URL in this WP.

SSL requirement and the exact SQLAlchemy URL parameter/location are **UNKNOWN** until the selected Supabase connection documentation is reviewed during implementation. A separate implementation WP must add only the approved runtime configuration and validate TLS.
