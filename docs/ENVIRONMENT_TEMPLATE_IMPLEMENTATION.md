# Environment Template Implementation

## Implemented file

`.env.example` is a tracked, placeholder-only configuration contract. It contains no real secret, token, password, or production address. Local `.env` files remain ignored by `.gitignore`.

## Included variables and evidence

| Variable | Evidence path | Safe example treatment |
| --- | --- | --- |
| `APP_NAME` | `backend/config.py` explicit environment lookup | Empty; application metadata is deployment-specific. |
| `APP_VERSION` | `backend/config.py` explicit environment lookup | Empty; release metadata is deployment-specific. |
| `DEBUG` | `backend/config.py` explicit environment lookup; both compose files declare it | `false`, a safe non-secret boolean. |
| `DAILY_EXP_CAP` | `backend/config.py` explicit environment lookup | `300`, the non-sensitive repository default required by the existing integrity check. |
| `ANTI_FARMING_INTERVAL_MINUTES` | `backend/config.py` explicit environment lookup | `10`, the non-sensitive repository default required by the existing integrity check. |
| `SQLALCHEMY_DATABASE_URL` | `backend/config.py` explicit environment lookup | Empty; it can contain sensitive connection information. |
| `DATABASE_URL` | `backend/config.py` explicit environment lookup | Empty; it can contain sensitive connection information. |
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | `backend/config.py` lookups; `docker-compose.yml` and `deploy/docker-compose.web.yml` environment declarations | Empty; the component values are deployment-specific and may be sensitive. |
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | `docker-compose.yml` and `deploy/docker-compose.web.yml` environment declarations | Empty; container-initialization values are deployment-specific and may be sensitive. |
| `API_BASE_URL` | `lib/api_config.dart`, `lib/api_config_io.dart`, `lib/api_config_web.dart`, `lib/api_client.dart`, and README launch documentation | Empty. It is a `--dart-define` compile-time setting, not a proven `.env` loader input. |

## Exclusions and unknowns

- No CI configuration files were found, so no CI-only environment variable was added.
- No `.env` loader (`dotenv`, `load_dotenv`, or equivalent) was found. Whether local `.env` is consumed automatically is **UNKNOWN**.
- No variable name was added solely because it is conventional. The template includes only names observed in code, README, or compose configuration.
- Compose structural keys such as `context` and `dockerfile` are not environment variables and were excluded.

## Usage boundary

Use `.env.example` as a name-and-placeholder reference. Do not copy deployment values into it. For Flutter, pass `API_BASE_URL` explicitly with `--dart-define` unless a separately approved runtime change introduces an environment loader.
