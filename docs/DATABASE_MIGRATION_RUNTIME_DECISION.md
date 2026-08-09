# Database Migration Runtime Decision

## Decision

**Status: UNKNOWN** — the repository does not provide enough executable evidence to identify a tool, command, or accountable owner that applies the SQL files in `/02_DATABASE`.

This is a decision about migration application only. It does not mean the active backend has no database runtime.

## Confirmed runtime database behavior

| Evidence path | Observed evidence | Decision impact |
| --- | --- | --- |
| `Dockerfile` | Launches `uvicorn backend.main:app`. | Confirms the FastAPI entry point. |
| `scripts/run_all.sh` | Launches `uvicorn backend.main:app`. | Confirms the development launcher reaches the same application. |
| `backend/main.py` | Calls `init_db()` during startup and supplies `get_db` to API routes. | Confirms startup ORM initialization and request-session use. |
| `backend/database.py` | Creates the SQLAlchemy engine and session factory; `init_db()` calls `Base.metadata.create_all`. | Confirms ORM-managed table initialization, not execution of `/02_DATABASE` SQL files. |
| `docker-compose.yml` and `deploy/docker-compose.web.yml` | Define backend and PostgreSQL database services. | Confirms containerized database service configuration, not migration application. |

## Migration application evidence

| Question | Result | Evidence |
| --- | --- | --- |
| Are migration SQL files present? | Yes | `/02_DATABASE` contains `01_schema_migration.sql` through `08_schema_migration_v8.sql`. |
| Is an SQL migration runner configured? | UNKNOWN | No tracked Alembic, Flyway, Liquibase, `manage.py`, migration directory, or SQL CLI execution command was found. |
| Is there a command that applies `/02_DATABASE`? | UNKNOWN | The inspected Dockerfiles, compose files, and `scripts/` contain application launch commands but no confirmed command that applies the SQL files. |
| Does backend startup apply `/02_DATABASE`? | UNKNOWN | `Base.metadata.create_all` initializes ORM metadata; no import or path reference from `backend/` to `/02_DATABASE` was found. |
| Is an accountable migration owner declared? | UNKNOWN | No `CODEOWNERS` file or execution-responsibility declaration was found. Uses of “owner” in database documents describe domain-data ownership, not a migration operator. |

## Governance conclusion

Do not treat `/02_DATABASE` as an automatically applied migration source until a separately approved change establishes all of the following:

1. the chosen migration tool or SQL application mechanism;
2. the exact invocation command and deployment stage;
3. ordering, idempotency, and rollback policy;
4. an accountable owner or review group.

This WP makes no SQL, schema, migration, code, or container-configuration change.
