# CODE_TRACEABILITY_MATRIX

- Version: 1.0
- Status: Active
- Last Updated: 2026-08-01
- Purpose: SSOT 문서와 실제 코드, 테스트의 연결점을 추적한다.

| Document | Primary Code | Secondary Code / UI | Test / Verification |
|---|---|---|---|
| `00_PROJECT/CANONICAL_CONSTANTS.md` | `backend/config.py` | `backend/models.py`, `lib/mock_data_provider.dart`, `.env.example` | `scripts/check_canonical_constants.py`, `scripts/check_patch005_integrity.py` |
| `00_PROJECT/CANONICAL_NAMING.md` | `backend/config.py` | `backend/progression_engine.py`, `lib/shop_screen.dart`, `lib/quest_screen.dart`, `lib/diet_screen.dart`, `lib/workout_screen.dart` | PATCH-005 naming scan, manual review |
| `03_GAME_SYSTEM/EXP_RULE.md` | `backend/progression_engine.py` | `backend/main.py`, `backend/quest_engine.py`, `lib/mock_data_provider.dart` | `test/progression_engine_test.py`, `tests/test_backend.py` |
| `01_ARCHITECTURE/FORMULA_REGISTRY.md` | `backend/health_calculator.py` | `backend/progression_engine.py`, `03_BACKEND/dynamic_health_engine_v13.py`, `backend/quest_engine.py` | `test/system_integration_test.py`, `03_BACKEND/tests/test_dynamic_health_engine_v13.py` |
| `01_ARCHITECTURE/EVENT_TRIGGER_MASTER.md` | `backend/main.py` | `backend/offline_sync_engine.py`, `03_BACKEND/api_tip_feeder_router_v3.py` | manual trace review |
| `01_ARCHITECTURE/RUNTIME_STATE_MATRIX.md` | `backend/main.py` | `lib/main_navigation_screen.dart`, `04_FRONTEND/health_tip_ui_controller_v1.py` | `03_BACKEND/test_full_pipeline_v3.py`, manual runtime review |
| `03_BACKEND/DDD/DOMAIN_EVENT_CATALOG.md` | `backend/main.py` | `backend/database.py`, `backend/quest_engine.py` | manual mapping only |
| `03_BACKEND/OUTBOX_EVENT_POLICY.md` | `backend/database.py` | `backend/offline_sync_engine.py` | not yet automated |
| `06_ANALYTICS/ANALYTICS_EVENT_SPEC.md` | no direct active emitter verified | `06_ANALYTICS/*` documentation only | gap: implementation trace missing |
| `03_BACKEND/HEALTH_ENGINE.md` | `backend/health_calculator.py` | `backend/diet_calculator.py` | `test/progression_engine_test.py`, `test/system_integration_test.py` |
| `03_BACKEND/QUEST_ENGINE.md` | `backend/quest_engine.py` | `lib/quest_screen.dart` | `test/system_integration_test.py` |
| `03_BACKEND/API_SPECIFICATION.md` | `backend/main.py` | `backend/models.py` | `tests/test_backend.py` |

## Traceability Gaps
1. Formula ID(F-001~F-005)가 코드 주석/상수에 직접 박혀 있지 않다.
2. Event ID가 코드 이벤트 객체로 정착되지 않아 문서 ↔ 런타임 추적이 약하다.
3. Analytics, Memory, Offline Sync는 설계 문서 대비 자동 검증 연결이 부족하다.
