# DYNAMIC REWARD CALCULATOR SPECIFICATION

## Purpose
본 문서는 사용자의 일일 건강 활동(걸음, 운동, 식단 기록)에 대해 인게임 재화(골드, 포인통), 경험치 및 길드 포인트를 지급하는 동적 보상 산출 체계를 정의한다.

## Scope
- 일일 건강 행동별 기본 보상 및 다변수 가속 계수
- 과도한 노가다/어뷰징을 방지하는 점증 감쇄 법칙(Anti-Grind Decreasing Returns)
- 길드원 간 시너지 보너스 합산 공식

## SSOT (Single Source of Truth)
- 본 문서는 게임 시스템 보상 및 경험치 산출 로직의 유일한 SSOT이다.

## Definitions
- **Diminishing Multiplier**: 특정 운동이나 걸음 수가 일일 정상 범주를 초과할 경우 보상 효율을 낮추는 감쇄 계수.
- **Guild Health Synergy**: 길드원 전체의 평균 건강 달성률에 따른 추가 보너스 비율.

## Runtime
- 백엔드 `progression_engine.py` 및 인게임 퀘스트 모듈 내 실행.

## Rules
1. **건강 보호형 감쇄**: 일일 25,000보 초과 시 무리한 운동 방지를 위해 걸음 수당 EXP 지급률이 50% 감쇄된다.
2. **식단 완벽 보상**: 정제당/튀김/음주가 없는 클린 식단을 3끼 연속 작성 시 '클린 가디언 보너스' (+30% EXP)를 지급한다.

## State
- `RewardState`: `daily_exp_accumulated`, `step_reward_tier`, `anti_grind_active` (boolean).

## Event
- `ON_REWARD_CALCULATED`: 보상 지급 및 팝업 안내 생성.

## Example
- **보상 계산 공식**:
  - `Base_Gold` = (Workout_Minutes * 10) + (Steps / 100)
  - `Health_Balance_Factor` = (Clean_Meal_Score / 100) * 0.5 + 0.8
  - `Final_Gold` = Base_Gold * Health_Balance_Factor * AntiGrindFactor

## Exception
- 부정 입력(비정상 속도의 걸음 수 센서 반응) 감지 시 보상 지급을 멈추고 안전 확인 안내 메시지를 출력한다.

## Related Documents
- `HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V5.md`
- `HEALTH IS ALL/03_GAME_SYSTEM/ANTI_GRIND_POLICY.mdux`

## Change History
- v1.0.0 (2026-07-31): 동적 보상 계산 공식 및 길드 시너지, 어뷰징 방지 정책 명세화.