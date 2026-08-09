# WP-0004 Result

## Scope completed

Created the root `.env.example` and the WP-0004 documentation. No code, API, database, migration, `.env`, `.gitignore`, dependency, lock file, or generated file was changed.

## Template contents

- Backend application and runtime-limit keys observed in `backend/config.py`.
- Backend database connection keys observed in `backend/config.py` and compose configuration.
- PostgreSQL container-initialization keys observed in compose configuration.
- Flutter `API_BASE_URL`, observed as a compile-time define in Flutter code and README launch documentation.

All potentially sensitive or deployment-specific values are blank. Only the non-sensitive `DAILY_EXP_CAP`, `ANTI_FARMING_INTERVAL_MINUTES`, and `DEBUG` safe defaults are populated.

## Unknowns

- Automatic `.env` loading is UNKNOWN: no loader was found.
- CI-only environment variables are UNKNOWN: no CI configuration files were present.
- Production secret injection owner and mechanism are outside the available repository evidence.

## Required validation

| Check | Result |
| --- | --- |
| `git diff --check` | PASS — initial verification passed; staged verification is also required before commit. |
| `scripts/check_patch005_integrity.py` | PASS |
| `scripts/check_canonical_constants.py` | PASS |
| Allowed-file scope | PASS — initial verification found only the five allowed WP-0004 files. |
