# Render Deployment Readiness

## Confirmed backend service candidates

| Render setting | Candidate | Evidence | Status |
| --- | --- | --- | --- |
| Repository branch | User-selected deployment branch | Render connects to GitHub; no `render.yaml` is tracked to fix a branch. | UNKNOWN until GUI selection |
| Root directory | Repository root | `Dockerfile`, `requirements.txt`, and `backend/main.py` are at the root-relative paths used by the launch configuration. | CONFIRMED candidate |
| Runtime | Docker Web Service | Root `Dockerfile` has a `CMD` invoking `uvicorn` for `backend.main:app`. | CONFIRMED candidate |
| Docker build command | Render Docker build | Dockerfile contains the build instructions; no separate Render build command is evidenced. | CONFIRMED candidate |
| Start command | Dockerfile `CMD` using `uvicorn backend.main:app` | `Dockerfile`; `scripts/run_all.sh` uses the same application target. | CONFIRMED candidate |
| Port | `8000` candidate | Dockerfile command specifies port `8000`; local script uses the same port. Whether Render injects a `PORT` variable is not handled by code. | CONFIRMED code port / UNKNOWN Render adaptation |
| Health check | `/healthz` | `backend/main.py` declares a GET health endpoint. | CONFIRMED |

## Database and frontend scope

- `backend/database.py` creates a SQLAlchemy engine from configuration; `backend/config.py` supports URL overrides and component DB settings. A production database is therefore required for durable backend operation.
- Render PostgreSQL versus an external PostgreSQL service is **UNKNOWN**: no Render configuration or production database decision is tracked.
- Flutter is excluded from this backend Web Service scope. `lib/main.dart` is a separate Flutter entry point and no backend Dockerfile evidence builds or serves Flutter assets.

## Missing implementation before deployment

- Render-aware port handling if the service must honor a platform-injected `PORT`.
- A selected production database provider and approved connection configuration.
- A Render-specific deployment descriptor only if the team chooses infrastructure-as-code; no `render.yaml` exists today.
- Production CORS/origin policy review: current backend middleware is not a deployment approval.
