# FORMULA_IMPLEMENTATION_MAP

- Version: 1.0
- Status: Active
- Last Updated: 2026-08-01
- Purpose: Formula Registry와 실제 코드/테스트 연결을 추적한다.

| Formula ID | Formula Name | Owner Document | Active Code | Test Coverage | Verified | Notes |
|---|---|---|---|---|---|---|
| F-001 | Overall Health Score | `01_ARCHITECTURE/FORMULA_REGISTRY.md` | `backend/health_calculator.py` | `test/system_integration_test.py` | Partial | 전용 `health_score_engine.py`는 없고 계산 책임이 `DynamicHealthCalculator`에 분산됨 |
| F-002 | Dynamic Emotion Value | `01_ARCHITECTURE/FORMULA_REGISTRY.md` | `backend/ai_agent_service.py` | `test/system_integration_test.py` 간접 검증 | Partial | 별도 EmotionEngine 파일 없이 AI 피드백 로직에 내장 |
| F-003 | EXP Reward Calculation | `03_GAME_SYSTEM/EXP_RULE.md` | `backend/progression_engine.py`, `backend/quest_engine.py` | `test/progression_engine_test.py`, `tests/test_backend.py` | Yes | Daily cap 300, anti-farming 10분, Exp 표준화 PATCH-005 반영 |
| F-004 | Memory Recall Score | `01_ARCHITECTURE/FORMULA_REGISTRY.md` | `backend/spirit_album_engine.py` 후보 | 없음 | No | 코드 파일은 있으나 F-004와의 명시적 바인딩/테스트 없음 |
| F-005 | Micro Spark Probability | `03_GAME_SYSTEM/MICRO_REWARD_SYSTEM.md` | 활성 코드 미확인 | 없음 | No | 문서 등록만 존재, 구현 상태 불명확 |

## Implementation Notes
1. PATCH-005에서 F-003 경로는 테스트 가능한 상태로 정리했다.
2. F-001/F-002는 구현은 있으나 Formula ID를 코드 상수나 주석으로 고정하지 않아 추적성이 약하다.
3. F-004/F-005는 `Planned or Orphan Candidate`로 취급하고 후속 분류가 필요하다.

## Required Next Action
- 각 구현 파일 상단 또는 함수 주석에 Formula ID를 명시한다.
- 테스트 이름에도 Formula ID를 반영해 역추적 시간을 줄인다.
