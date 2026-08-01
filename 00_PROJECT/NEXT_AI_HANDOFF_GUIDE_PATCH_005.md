# NEXT_AI_HANDOFF_GUIDE_PATCH_005

## 한 줄 요약
PATCH-005는 새 설계 문서 추가 단계가 아니라, SSOT ↔ 코드 ↔ 테스트를 실제로 연결하는 검증층을 구축한 패치다.

## 이번 패치에서 실제로 변경한 것
### 1) 테스트 가능 상태 복구
- `conftest.py` 추가
- `pytest.ini` 추가
- `backend/__init__.py` 추가
- 결과: import 오류 제거, `pytest -q` 전체 통과(9 passed)

### 2) 사용자 표기 정렬
- active backend/UI 코드에서 `Exp.` → `Exp` 정리
- 손상된 Dart 문자열 보간(`$`` 오염, 백틱 혼입) 복구
- 수정 파일 예시:
  - `backend/config.py`
  - `backend/progression_engine.py`
  - `backend/health_calculator.py`
  - `backend/habit_sleep_calculator.py`
  - `lib/home_screen.dart`
  - `lib/quest_screen.dart`
  - `lib/shop_screen.dart`
  - `lib/diet_screen.dart`
  - `lib/workout_screen.dart`
  - `lib/widgets/health_i_widget.dart`

### 3) 계산 정확도 보정
- `03_BACKEND/dynamic_health_engine_v13.py`
- `int(...)` → `int(round(...))`
- 목적: 테스트 기대값 966 일치

### 4) Verification & Traceability Layer 생성
- `00_PROJECT/IMPLEMENTATION_STATUS_MATRIX.md`
- `00_PROJECT/CODE_TRACEABILITY_MATRIX.md`
- `01_ARCHITECTURE/FORMULA_IMPLEMENTATION_MAP.md`
- `01_ARCHITECTURE/EVENT_IMPLEMENTATION_MAP.md`
- `00_PROJECT/SSOT_VERIFICATION_CHECKLIST.md`
- `03_BACKEND/ORPHAN_MODULE_REGISTER.md`
- `00_PROJECT/FEATURE_COMPLETION_TRACKER.md`
- `06_QA/TEST_TRACEABILITY_MATRIX.md`
- `00_PROJECT/CONFIG_REGISTRY.md`
- `00_PROJECT/ADR/IMPLEMENTATION_DECISION_LOG.md`

## 검증 결과
- `scripts/check_canonical_constants.py`: PASS
- `scripts/check_patch005_integrity.py`: PASS
- `pytest -q`: PASS (9 passed)

## 아직 남은 핵심 리스크
1. Event는 문서 정의 대비 explicit event bus/outbox 구현이 약함
2. Main navigation에 미연결 화면이 많음
3. Provider/Riverpod 혼재가 남아 있음
4. orphan 후보가 실제 이동되지 않았고 문서 분류 단계에 머물러 있음
5. `datetime.utcnow()` deprecation warning이 남아 있음

## 다음 AI가 절대 놓치면 안 되는 파일
1. `00_PROJECT/PATCH_005_EXECUTION_REPORT.md`
2. `00_PROJECT/IMPLEMENTATION_STATUS_MATRIX.md`
3. `00_PROJECT/CODE_TRACEABILITY_MATRIX.md`
4. `03_BACKEND/ORPHAN_MODULE_REGISTER.md`
5. `00_PROJECT/NEXT_AI_WORK_INSTRUCTION_PATCH_005.md`

## 권장 작업 순서
1. Event 구현 범위 결정
2. Navigation 연결 범위 결정
3. Orphan 실제 이동
4. Flutter 테스트 확장
5. UTC warning 정리
