# Environment Template Decision

## Decision

**A tracked `.env.example` is needed as a configuration-governance template, but it is not currently present and is not a proven runtime loader.**

The template is needed to publish the names and placeholder-only expectations of backend and container environment inputs without committing local values. Creating it is intentionally deferred because WP-0003 is investigation-only.

## Evidence

| Evidence path | Observed evidence | Decision impact |
| --- | --- | --- |
| `.gitignore` | Ignores `.env` and `.env.*`, while explicitly allowing `!.env.example`. | Shows the repository is prepared to track a safe example template. |
| `backend/config.py` | Reads database connection settings from environment-key names, including `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, and URL override keys. | A documented configuration contract is needed for backend and container setup. |
| `backend/database.py` | Builds the SQLAlchemy engine from configured settings. | Confirms those backend settings affect runtime database connectivity. |
| `docker-compose.yml` and `deploy/docker-compose.web.yml` | Declare backend and database-service environment sections. | Confirms environment-driven container configuration. |
| `lib/api_config.dart`, `lib/api_config_io.dart`, `lib/api_config_web.dart`, `lib/api_client.dart` | Reference `API_BASE_URL` as a Dart compile-time define. | This is not evidence that Flutter loads `.env`; document it separately as a launch-time define. |
| Git tracked-file and history checks | No `.env.example` path is currently tracked or found in reachable history. | Confirms the template is absent and must not be represented as existing. |

## Management standard for a future approved template

- The file name must be `.env.example`; local `.env` and `.env.*` remain ignored.
- Include variable names and non-sensitive placeholders only; never copy a local, deployment, database, or service credential value.
- Cover backend/container database configuration keys as a contract, with one documented precedence rule for URL overrides versus component keys.
- Do not imply that `API_BASE_URL` is loaded from `.env`; it is a `--dart-define` launch setting unless a future approved runtime change adds a loader.
- Assign a configuration owner or review group before the template is introduced; the current repository evidence does not identify one.

## Unknowns

- **Runtime `.env` loader:** UNKNOWN. No `dotenv`, `load_dotenv`, or equivalent loader was found in the inspected backend, Flutter, Docker, or deployment paths.
- **Configuration owner:** UNKNOWN. No `CODEOWNERS` or configuration responsibility declaration was found.
- **Required production injection mechanism:** UNKNOWN. The repository shows container environment sections but no approved production secret-management procedure.

WP-0003 does not create or modify `.env`, `.env.example`, or any runtime configuration file.
