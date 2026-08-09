# Repository Runtime Map

## Scope and method

This map is based on executable configuration, imports, entry points, HTTP paths, and database setup observed on `codex/wp-0002-canonical-runtime-map`. It does not classify a directory from its name alone. No credential values are recorded.

## Confirmed runtime flow

```text
Flutter entry
  lib/main.dart
    -> MaterialApp(home: MainNavigationScreen)
      -> lib/main_navigation_screen.dart
        -> Home / Quest / Shop screens and Home sub-screen navigation
      -> screen state: ApiDataProvider
        -> lib/api_data_provider.dart
          -> HealthIApiClient
            -> lib/api_client.dart
              POST /api/v1/health/record
              GET  /api/v1/health-i/status/{user_id}
                -> FastAPI app: backend/main.py (app)
                  -> route functions using get_db()
                    -> HealthIAgentService, DynamicHealthCalculator, ProgressionEngine
                    -> backend/database.py (SQLAlchemy engine, SessionLocal, ORM models)
                      -> configured database URL

Database migration candidate
  02_DATABASE/*.sql
    -> no import, startup command, or migration runner connection confirmed
```

## Evidence ledger

| Flow segment | Confirmed paths | Evidence |
| --- | --- | --- |
| Flutter entry | `pubspec.yaml`, `lib/main.dart` | `pubspec.yaml` declares Flutter; `main.dart` contains `void main`, `runApp`, `MaterialApp`, and `home: MainNavigationScreen`. |
| Navigation | `lib/main_navigation_screen.dart`, `lib/home_screen.dart` | `MainNavigationScreen` imports Home, Quest, and Shop and builds a `BottomNavigationBar`; `home_screen.dart` uses `Navigator.of(context).push(MaterialPageRoute(...))`. No declarative router configuration was found. |
| Screen and state | `lib/home_screen.dart`, `lib/diet_screen.dart`, `lib/workout_screen.dart`, `lib/shop_screen.dart`, `lib/spirit_screen.dart`, `lib/api_data_provider.dart` | These screens use `ApiDataProvider` through Provider APIs. `ApiDataProvider` calls its `HealthIApiClient` for status and activity operations. |
| API client | `lib/api_client.dart`, `lib/api_config.dart`, `lib/api_config_io.dart`, `lib/api_config_web.dart` | `HealthIApiClient` uses `package:http`; it constructs the two `/api/v1` paths above and resolves a platform-aware base URL. |
| FastAPI entry | `Dockerfile`, `scripts/run_all.sh`, `backend/main.py` | Both executable launch definitions invoke `uvicorn backend.main:app`; `backend/main.py` constructs `FastAPI` and registers the matching GET and POST routes. |
| Service and engine | `backend/main.py`, `backend/ai_agent_service.py`, `backend/health_calculator.py`, `backend/progression_engine.py` | `backend/main.py` imports and instantiates these three classes and uses them from the endpoint flow. |
| DB connection | `backend/config.py`, `backend/database.py`, `backend/main.py` | `database.py` derives an SQLAlchemy engine from configured settings, supplies `SessionLocal` through `get_db`, and initializes ORM tables. `main.py` calls `init_db()` and injects `get_db` into both API routes. |
| DB migration candidate | `02_DATABASE/04_schema_migration_v4.sql`, `02_DATABASE/06_schema_migration_v6.sql`, `02_DATABASE/08_schema_migration_v8.sql` | SQL migration files exist, but no import, startup command, migration tool configuration, or runner connecting this directory to the confirmed runtime was found. |

## Canonical runtime determination

- **Flutter runtime:** `lib/`, entered by `lib/main.dart`.
- **FastAPI runtime:** `backend/`, entered by `backend.main:app` through Docker and the development launcher.
- **Runtime database access:** `backend/database.py` and `backend/config.py`; the application initializes its SQLAlchemy metadata at startup.
- **Migration runtime:** **UNKNOWN**. `02_DATABASE/` contains SQL evidence, but the repository does not provide a confirmed execution relationship from the active application or launch configuration.

## Safe validation run

| Command | Result | Notes |
| --- | --- | --- |
| Bundled Python running `scripts/check_patch005_integrity.py` | PASS | Read-only integrity check completed successfully. |
| Bundled Python running `scripts/check_canonical_constants.py` | FAIL | The check expects `.env.example`, which is absent on the `main` baseline. This WP did not create it because environment-file changes are out of scope. |

Flutter test or build commands were not run because they can refresh tracked generated output in this repository. This documentation-only WP did not modify generated files.
