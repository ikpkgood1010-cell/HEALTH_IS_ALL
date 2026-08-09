# Render–Supabase Environment Mapping

| Variable | Use | Render input owner | Rule |
| --- | --- | --- | --- |
| `SQLALCHEMY_DATABASE_URL` | First backend URL override in `backend/config.py` | Developer in Render Dashboard before deployment | Preferred single approved Supabase session-pooler value; never document or commit it. |
| `DATABASE_URL` | Fallback URL override | Developer | Do not set alongside the approved primary override unless a separate precedence decision requires it. |
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | Component fallback only | Developer | Do not use when the approved URL override is supplied. |
| `DEBUG`, app/runtime limit variables | Backend optional configuration | Developer | Non-secret runtime settings only when explicitly needed. |

All are Render runtime Environment Variables, never Docker build arguments. Flutter `API_BASE_URL` is excluded.
