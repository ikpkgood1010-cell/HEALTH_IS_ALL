# Repository Path Classification

## Classification rule

Classifications are based on observed runtime evidence, not directory names. `UNKNOWN` means the repository did not provide enough evidence for a reliable conclusion.

| 경로 | 분류 | 역할 | 수정 가능 여부 | 판정 근거 | 확인 상태 |
| --- | --- | --- | --- | --- | --- |
| `/lib` | ACTIVE | Flutter application runtime | 불가 (WP-0002) | `lib/main.dart` is the Flutter `main`/`runApp` entry. It builds `MaterialApp` and starts `MainNavigationScreen`; active screens use `ApiDataProvider`. | CONFIRMED |
| `/backend` | ACTIVE | FastAPI application and ORM-backed server runtime | 불가 (WP-0002) | `Dockerfile` and `scripts/run_all.sh` start `uvicorn backend.main:app`. `backend/main.py` creates FastAPI, serves the paths used by `lib/api_client.dart`, and uses database/session dependencies. | CONFIRMED |
| `/02_DATABASE` | UNKNOWN | SQL migration candidate | 불가 (WP-0002) | SQL migration files are present, but no active import, startup command, migration-tool configuration, or runner linking this directory to the runtime was found. | INSUFFICIENT EVIDENCE |
| `/test` | SUPPORTING | Flutter/Dart and Python test sources | 불가 (WP-0002) | Flutter test files import `flutter_test`; Python tests import backend engines. These test active code but are not a runtime entry point. | CONFIRMED |
| `/tests` | SUPPORTING | FastAPI endpoint tests | 불가 (WP-0002) | `tests/test_backend.py` imports `backend.main.app` through FastAPI `TestClient` and calls the active API paths. | CONFIRMED |
| `/scripts` | SUPPORTING | Development launcher and repository validation | 불가 (WP-0002) | `scripts/run_all.sh` launches `uvicorn backend.main:app` and `flutter run`; the Python scripts perform read-only integrity checks. | CONFIRMED |
| `/00_PROJECT` | REFERENCE | Project planning and execution evidence | 불가 (WP-0002) | Contents are planning Markdown files. Some documents describe commands, but no source import or executable configuration consumes this directory. | CONFIRMED |
| `/01_ARCHITECTURE` | REFERENCE | Architecture and design evidence | 불가 (WP-0002) | Contents are Markdown/MDUX architecture specifications; no runtime import or startup configuration references were found. | CONFIRMED |
| `/07_PRODUCT` | REFERENCE | Product-policy and product-language evidence | 불가 (WP-0002) | Contents are product Markdown documents; no runtime import or startup configuration references were found. | CONFIRMED |

## Notes

- `/02_DATABASE` is deliberately not labelled `LEGACY`: there is no confirmed replacement or execution history that proves it is superseded.
- The confirmed database runtime is in `/backend` (`backend/database.py`); this does not by itself prove how, or whether, the SQL files in `/02_DATABASE` are applied.
- Existing generated artifacts were not classified or changed by this WP; generated-file handling remains outside this documentation-only scope.
