# EXP_RULE

- Document Name: EXP_RULE.md
- Version: 2.0
- Status: Active
- Owner: PATCH-004 Implementation Governance
- Last Updated: 2026-08-01
- Purpose: Exp 산출, soft cap, anti-farming, 성장 반영 정책의 SSOT를 정의한다.
- Implementation Status: Implemented
- Source of Truth: Documentation + Config + Code
- Verification:
  - Last Verified Date: 2026-08-01
  - Verified By: PATCH-004 governance pass
  - Test Reference: `test/progression_engine_test.py`, `backend/progression_engine.py`

## Scope
- 식단, 운동, 습관 등 활동의 Exp 반영
- 일일/주간 cap 정책
- streak 보너스
- anti-farming 규칙

## Definitions
- Base Exp: 활동별 기본 지급량
- Daily Soft Cap: 하루 성장 반영 최대치
- Weekly Soft Cap: 주간 기준 관리치
- Anti-Farming Interval: 연속 입력 악용 방지 시간

## Canonical Policy
1. 프로젝트 전체 표기는 `Exp`로 통일한다.
2. Daily Cap은 `300`을 기준으로 한다.
3. Weekly Soft Cap은 `2100`을 기준으로 한다.
4. 건강 행동 기록 자체는 막지 않되, 성장 경제는 soft cap으로 보호한다.

## Base Exp Rule
- Meal Log: 30 Exp
- Workout Log: 50 Exp
- Habit Complete: 20 Exp
- Unknown/Generic Health Action: 15 Exp fallback

## Streak Rule
1. streak bonus는 이틀째부터 적용한다.
2. 계산식: `min((streak_days - 1) * 0.02, 0.20)`
3. 최대 streak bonus는 20%다.

## Daily Soft Cap Rule
1. 일일 성장 반영 최대치는 300 Exp다.
2. 300에 도달하면 추가 행동은 기록할 수 있으나 성장 보상은 기본적으로 0 또는 감쇄 정책에 따른다.
3. 현재 런타임 구현은 300 도달 시 추가 Exp 0을 적용한다.
4. 향후 soft-cap-after-300 정책을 도입할 경우 별도 실험과 문서 갱신이 필요하다.

## Weekly Soft Cap Rule
1. 운영 관리 기준은 2100 Exp다.
2. 주간 분석/경제 모니터링 기준으로 사용한다.
3. 주간 cap은 현재 런타임에 강제되지 않더라도 밸런스 관측 지표로 유지한다.

## Anti-Farming Rule
1. 동일 사용자 연속 기록 간 최소 간격은 10분이다.
2. 10분 이내 재입력 시 데이터 저장 정책과 Exp 지급 정책을 분리해서 판단할 수 있다.
3. 현재 런타임 구현은 10분 이내 재입력 시 Exp 0, 안내 메시지 반환이다.

## Rationale
1. HEALTH IS ALL은 과도한 플레이 시간을 유도하는 게임이 아니다.
2. 성장 경제를 보호하되, 건강 행동 기록과 통계 축적은 계속 허용해야 한다.
3. 따라서 hard stop보다 “기록은 허용, 성장 반영은 제한” 구조가 적합하다.

## Runtime Alignment Notes
- `backend/config.py` -> `DAILY_EXP_CAP=300`
- `.env.example` -> `DAILY_EXP_CAP=300`
- `backend/models.py` -> `daily_exp_cap=300`
- `lib/mock_data_provider.dart` -> `_dailyExpCap=300`

## Forbidden
- 클라이언트가 Exp를 직접 계산해 서버 지급값으로 강제하는 행위
- SSOT 결정 없이 문서와 코드 중 한쪽만 수정하는 행위
- `XP`, `EXP`, `Experience Point`로 사용자 표기를 새로 추가하는 행위

## Related Source Files
- `backend/config.py`
- `backend/progression_engine.py`
- `backend/main.py`
- `backend/models.py`
- `lib/mock_data_provider.dart`
- `test/progression_engine_test.py`

## Validation Method
- Unit Test
- Integration Test
- Compile Check
- Runtime Verification
