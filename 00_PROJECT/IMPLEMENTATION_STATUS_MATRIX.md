# IMPLEMENTATION_STATUS_MATRIX

- Version: 1.0
- Status: Active
- Last Updated: 2026-08-01
- Purpose: 설계 → 코드 → 테스트 → 검증 상태를 한눈에 추적하는 PATCH-005 기준 운영 매트릭스.

## Legend
- Design: SSOT 문서 존재 여부
- Code: 런타임 코드 또는 화면/엔진 구현 여부
- Test: 자동화 테스트 존재 여부
- Verified: 스크립트/테스트/수동 스캔으로 현재 패치에서 확인했는지 여부
- 상태값: `Implemented`, `Partial`, `Planned`, `Legacy`

## Matrix
| System | Design | Code | Test | Verified | Notes |
|---|---|---|---|---|---|
| Exp / Progression | Implemented | Implemented | Implemented | Implemented | `EXP_RULE.md`, `backend/progression_engine.py`, `test/progression_engine_test.py`, `tests/test_backend.py` |
| Health Record API | Implemented | Implemented | Implemented | Implemented | `/api/v1/health/record`, `/healthz`, `/api/v1/health-i/status/{user_id}` 검증 완료 |
| Health Score | Implemented | Partial | Partial | Partial | `backend/health_calculator.py` 기반 계산은 존재하나 F-001 ID 태깅 및 별도 계약 테스트 부족 |
| Emotion / Dialogue | Implemented | Partial | Partial | Partial | `backend/ai_agent_service.py`, `lib/widgets/health_i_widget.dart` 연계. 명시적 이벤트 버스 없음 |
| Quest Reward | Implemented | Implemented | Partial | Partial | `backend/quest_engine.py`, `lib/quest_screen.dart`. UI 자동 테스트 없음 |
| Diet Logging UI | Implemented | Implemented | No | Partial | `lib/diet_screen.dart` 문자열/구문 손상 복구 완료 |
| Workout Logging UI | Implemented | Implemented | No | Partial | `lib/workout_screen.dart` 문자열/구문 손상 복구 완료 |
| Shop / Customization UI | Implemented | Implemented | No | Partial | `lib/shop_screen.dart` Exp 표기 및 보상 문구 정리 |
| Main Navigation | Implemented | Partial | Partial | Partial | 홈/퀘스트/상점만 연결. 식단/운동/설정/기타 화면 미연결. `test/main_navigation_widget_test.dart`는 PATCH-006 세션에서 실제 위젯 기준으로 재작성(이전에는 mock 라벨로 항상 통과하던 가짜 테스트였음) |
| Daily Reset Runtime | Implemented | Partial | No | No | 문서 있음, 명시적 스케줄러 연결 미확인 |
| Offline Sync | Implemented | Partial | No | No | 엔진 파일 존재, 활성 라우트/호출 연결 미확인 |
| Memory / Album | Implemented | Partial | No | No | 설계 및 엔진 파일 있으나 활성 플로우 미연결 |
| Analytics Events | Implemented | Partial | No | No | 분석 이벤트 문서 존재, 코드 이벤트 발행 추적 미약 |
| Orphan Governance | Implemented | Partial | No | Partial | PATCH-005에서 등록 문서 추가, 실제 archive 이동은 후속 결정 필요 |
| Config Registry | Implemented | Implemented | Implemented | Implemented | 상수 스크립트 + PATCH-005 integrity check 통과 |

## PATCH-005 Verification Snapshot
- `scripts/check_canonical_constants.py`: PASS
- `scripts/check_patch005_integrity.py`: PASS
- `pytest -q`: 9 passed

## PATCH-006 Re-Verification Snapshot (2026-08-01, 별도 검증 세션)
- 네트워크/Flutter SDK가 없는 환경에서 재검증 진행. 결과는 아래와 같이 부분적으로만
  직접 재현 가능했다.
- `scripts/check_canonical_constants.py`: 실제 재실행 PASS
- `scripts/check_patch005_integrity.py`: 실제 재실행 PASS
- pytest 9개 중 6개(순수 로직, fastapi 불필요): 실제 재실행 PASS
  (`test/progression_engine_test.py` 3개, `test/system_integration_test.py` 1개,
  `03_BACKEND/tests/test_dynamic_health_engine_v13.py` 2개)
- pytest 9개 중 3개(`tests/test_backend.py`, fastapi 필요): 이 세션에 fastapi/pydantic/
  sqlalchemy 설치 불가(네트워크 차단)로 실행 불가. 코드 리뷰로 로직 일치 확인, 런타임 미검증.
- Flutter/Dart 관련 전부: Flutter SDK 부재로 `flutter pub get`/`analyze`/`test` 실행 불가.
  대신 정적 검사(구문 균형, import 대상 존재 여부, API 존재 여부)만 수행.

## PATCH-006 세션에서 새로 발견하고 수정한 문제
1. **`pubspec.yaml` 부재** — 신규 생성. 이전까지 `flutter pub get`부터 실패하는 상태였다.
2. **`lib/main.dart`의 `Colors.black80`** — 존재하지 않는 API. `Colors.black87`로 수정.
3. **`test/main_navigation_widget_test.dart`가 실제 `lib/main_navigation_screen.dart`를
   import하지 않던 문제** — 재작성하여 실제 위젯을 검증하도록 수정. 나머지 6개 dart
   테스트 파일도 동일한 패턴(자체 mock 클래스로 검증)이 확인되었으나 이번 세션에서는
   미수정 (`06_QA/TEST_TRACEABILITY_MATRIX.md` Gaps 참고).

## Immediate Risks
1. 이벤트는 문서 기준으로 정의되어 있으나 코드에는 명시적 발행/소비 계층이 부족하다.
2. Provider/Riverpod 혼재가 남아 있으며 신규 화면은 Riverpod 기준으로 수렴해야 한다.
3. 미연결 UI/엔진이 많아 orphan/roadmap/archive 분류가 추가로 필요하다.
4. `test/*.dart` 중 6개가 여전히 실제 lib 코드를 검증하지 않는 가짜 테스트 상태다.
5. Flutter 빌드 자체가 이번 세션 이전까지 `pubspec.yaml` 부재로 원천적으로 불가능했다는
   사실이 PATCH-005까지 어떤 문서에도 기록되지 않았다. 다음 담당자는 Flutter SDK가
   있는 환경에서 최우선으로 `flutter pub get && flutter analyze && flutter test`를
   1회 실행해 이번 세션의 수정이 실제로 유효한지 확인해야 한다.
