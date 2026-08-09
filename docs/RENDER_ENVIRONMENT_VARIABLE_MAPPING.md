# Render Environment Variable Mapping

| Variable/group | Use location | Required for Render | Value input owner | Build/runtime | Notes |
| --- | --- | --- | --- | --- | --- |
| `APP_NAME`, `APP_VERSION`, `DEBUG` | `backend/config.py` | Optional code defaults exist | Developer now; future platform/security owner | Runtime | Add only if production override is approved. |
| `DAILY_EXP_CAP`, `ANTI_FARMING_INTERVAL_MINUTES` | `backend/config.py` | Optional code defaults exist | Developer now | Runtime | Non-secret policy overrides. |
| `SQLALCHEMY_DATABASE_URL` or `DATABASE_URL` | `backend/config.py`, `backend/database.py` | Required when using a production DB URL | Developer enters in Render Dashboard before deployment | Runtime | Select one approved URL path; never document value. |
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | `backend/config.py` | Required only when URL overrides are absent | Developer enters in Render Dashboard before deployment | Runtime | Component alternative to URL configuration. |
| `POSTGRES_*` | Compose PostgreSQL service only | UNKNOWN for Render backend-only service | UNKNOWN pending DB choice | Runtime if a self-managed compatible service exists | Not consumed by FastAPI configuration. |
| `API_BASE_URL` | Flutter `String.fromEnvironment` | Not for this backend service | Flutter release owner | Build-time Flutter define | Frontend excluded. |

No Docker build argument may receive a secret. Configure secret values only as Render runtime Environment Variables; do not place them in Dockerfile, build args, source, logs, or documentation.
