# TEST_TRACEABILITY_MATRIX

- Version: 1.0
- Status: Active
- Last Updated: 2026-08-01
- Purpose: 테스트가 어떤 SSOT와 코드를 검증하는지 추적한다.

| Test | Document | Code | Type | Status |
|---|---|---|---|---|
| `test/progression_engine_test.py::test_daily_exp_cap` | `03_GAME_SYSTEM/EXP_RULE.md` | `backend/progression_engine.py` | Unit | PASS |
| `test/progression_engine_test.py::test_anti_farming_10min_rule` | `03_GAME_SYSTEM/EXP_RULE.md` | `backend/progression_engine.py` | Unit | PASS |
| `test/progression_engine_test.py::test_dynamic_workout_calorie_calculation` | `03_BACKEND/HEALTH_ENGINE.md` | `backend/health_calculator.py` | Unit | PASS |
| `test/system_integration_test.py::test_full_health_to_game_pipeline` | `01_ARCHITECTURE/FORMULA_REGISTRY.md`, `03_GAME_SYSTEM/EXP_RULE.md` | `backend/health_calculator.py`, `backend/diet_calculator.py`, `backend/ai_agent_service.py`, `backend/quest_engine.py`, `backend/progression_engine.py` | Integration | PASS |
| `03_BACKEND/tests/test_dynamic_health_engine_v13.py::test_dynamic_multi_mode_success` | `01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V8.md` | `03_BACKEND/dynamic_health_engine_v13.py` | Unit | PASS |
| `03_BACKEND/tests/test_dynamic_health_engine_v13.py::test_fallback_simple_mode_on_missing_param` | `01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V8.md` | `03_BACKEND/dynamic_health_engine_v13.py` | Unit | PASS |
| `tests/test_backend.py::test_health_check` | `03_BACKEND/API_SPECIFICATION.md` | `backend/main.py` | API | PASS |
| `tests/test_backend.py::test_default_health_i_status` | `00_PROJECT/CANONICAL_CONSTANTS.md` | `backend/main.py`, `backend/models.py` | API | PASS |
| `tests/test_backend.py::test_record_health_activity` | `03_GAME_SYSTEM/EXP_RULE.md`, `03_BACKEND/API_SPECIFICATION.md` | `backend/main.py`, `backend/progression_engine.py` | API | PASS |
| `scripts/check_canonical_constants.py` | `00_PROJECT/CANONICAL_CONSTANTS.md` | `backend/config.py`, `.env.example`, `backend/models.py`, `lib/mock_data_provider.dart` | Static verification | PASS |
| `scripts/check_patch005_integrity.py` | `00_PROJECT/CANONICAL_NAMING.md`, `03_GAME_SYSTEM/EXP_RULE.md` | `backend/config.py`, `backend/models.py` | Static verification | PASS |

## Gaps
- Flutter widget test와 실제 활성 화면 연결 테스트가 부족하다.
- Event / scheduler / offline sync / orphan classification 관련 자동 테스트가 없다.

## PATCH-006 검증 세션에서 새로 확인된 사실 (2026-08-01)
- **`test/*.dart` 7개 전부가 `lib/`를 import하지 않고 있었다.** 각 파일이 테스트 대상 위젯을 자체적으로
  재정의한 mock 클래스(예: `AISpiritCardWidget`, `HabitTileWidget`)로 검증하고 있어, 실제
  `lib/home_screen.dart`, `lib/habit_routine_screen.dart` 등이 깨지거나 바뀌어도 테스트는 항상
  통과하는 구조였다. `test/main_navigation_widget_test.dart`는 이번 세션에서 실제
  `lib/main_navigation_screen.dart`를 pumpWidget하도록 재작성했다(실제 라벨 '건강 홈'/'퀘스트'/
  '건강이 상점' 검증 + 탭 전환 검증). 나머지 6개(`ai_spirit_widget_test.dart`,
  `app_theme_test.dart`, `habit_routine_test.dart`, `habit_routine_widget_test.dart`,
  `meal_exercise_logger_test.dart`, `settings_profile_test.dart`)는 동일한 문제가 있으나
  이번 세션에서는 수정하지 못했다. Flutter SDK가 없는 환경이라 재작성 후 실행 검증이
  불가능했고, 검증 없이 대량 수정하는 것이 더 위험하다고 판단해 범위를 좁혔다.
- **`pubspec.yaml`이 프로젝트에 존재하지 않았다.** `flutter pub get`부터 실패하므로
  `.github/workflows/flutter_ci.yaml` 전체가 항상 실패하는 상태였다. 이번 세션에서
  `lib/`, `test/`가 실제로 사용하는 패키지(provider, flutter_riverpod, hive_flutter)를
  전수조사하여 새로 생성했다. Flutter SDK가 없어 `flutter pub get` 자체 실행 검증은
  못 했다.
- **`lib/main.dart`에 존재하지 않는 `Colors.black80` API가 2곳 사용되고 있었다.**
  Flutter `Colors`에는 `black87`만 존재한다(다른 화면 파일들은 모두 `black87`을
  올바르게 사용 중이었음). `Colors.black87`로 수정했다. 이 상태로는 `flutter analyze`가
  실패했을 것이다.
- 위 3가지는 Dart/Flutter 실행 환경이 없는 채로 이전 패치에서 반복적으로 넘어간
  항목으로 보인다. 다음 담당자는 Flutter SDK가 있는 환경에서 `flutter pub get` →
  `flutter analyze` → `flutter test`를 최우선으로 1회 실행해 이 수정들이 실제로
  유효한지 확인해야 한다.
