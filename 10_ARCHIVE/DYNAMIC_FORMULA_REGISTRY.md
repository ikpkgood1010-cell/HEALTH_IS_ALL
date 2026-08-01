# DYNAMIC_FORMULA_REGISTRY.md

## Purpose
본 문서는 'HEALTH IS ALL' 시스템 내에서 사용되는 모든 건강, 식단, 운동, RPG 경험치(EXP), 정령 호감도 및 리워드 계산 수식을 단일 진실 공급원(SSOT)으로 정의한다. 정적이고 단순한 반복 수치를 지양하고, 사용자의 신체 조건, 운동 강도 자각도, 일일 상태 변수 및 미세 변동 요소를 결합하여 매번 유기적이고 역동적인 결과를 제공하는 것을 목적으로 한다.

## Scope
1. 신체 기초대사량(BMR) 및 일일 활동 대사량(TDEE) 동적 계산
2. 운동 강도(Heart Rate / RPE) 기반 칼로리 및 RPG 경험치(EXP) 산출
3. 연쇄 달성(Streak), 정령 호감도(Spirit Affinity), 무작위 보상 변동성 공식
4. 데이터 미비 시 차선책(Fallback) 계산 규칙

## SSOT
본 문서는 모든 백엔드 계산 엔진(`backend/dynamic_health_engine.py`) 및 프론트엔드 실시간 계산기(`lib/dynamic_health_calculator.dart`) 수식 로직의 **최상위 SSOT(Single Source of Truth)**로 기능한다.

## Definitions
- **BMR (Basal Metabolic Rate)**: 미플린-스지올(Mifflin-St Jeor) 공식을 기반으로 한 기초대사량.
- **RPE (Rating of Perceived Exertion)**: 주관적 운동 자각도 (1~10 단계).
- **PAL (Physical Activity Level)**: 일일 활동 계수.
- **Affinity Multiplier**: 정령과의 교감도에 따라 부여되는 리워드 가중치 ($0.9 \sim 1.3$).
- **Fluctuator**: 몰입감을 높이기 위한 미세 난수 변동 인자 ($0.95 \sim 1.05$).

## Runtime
- 프론트엔드(Flutter): 사용자 입력 시 로컬 실시간 계산 및 UI 즉시 반영 (오프라인 상태 지원).
- 백엔드(Python/FastAPI): 서버 동기화 및 퀘스트 완료 검증 시 재검증 수행.

## Rules
1. **건강-게임 상호 기여 법칙**: 모든 건강 활동은 정량적 수치로 변환되어 게임 EXP 및 정령 성장에 기여하되, 게임 요소가 건강 데이터의 직관적 인지를 방해해서는 안 된다.
2. **동적 변동성 적용**: 동일한 운동과 식단을 기록하더라도 연속 달성일, 당일 자각 강도, 정령 호감도에 의해 최종 획득 경험치 및 칼로리 소모 보정치가 소폭 다르게 산출된다.
3. **안전망 규칙(Fallback Rule)**: 심박수 데이터 또는 상세 수치가 누락된 경우, METs 표준 기반 간결 계산식으로 자동 전환되어 시스템 오류나 결합 충돌을 방지한다.

## State
- `user_weight`: 체중 (kg)
- `user_height`: 신장 (cm)
- `user_age`: 연령 (세)
- `user_gender`: 성별 (M/F)
- `streak_days`: 연속 출석 및 습관 달성 일수
- `spirit_affinity_level`: 정령 호감도 단계 (1~50)

## Event
- `ON_EXERCISE_LOGGED`: 운동 기록 작성 이벤트 발생 시 경험치 및 칼로리 동적 계산
- `ON_MEAL_LOGGED`: 식단 기록 작성 시 영양소 밸런스 및 정령 상태 변환
- `ON_FALLBACK_TRIGGERED`: 필수 정밀 변수 누락 시 표준 MET 수식으로 강제 전환

## Example
### 1. 동적 BMR 수식 (Mifflin-St Jeor)
- 남성: $BMR = 10 \times \text{weight} + 6.25 \times \text{height} - 5 \times \text{age} + 5$
- 여성: $BMR = 10 \times \text{weight} + 6.25 \times \text{height} - 5 \times \text{age} - 161$

### 2. 동적 운동 EXP 산출식
$$\text{Base EXP} = \text{Duration(min)} \times \text{MET} \times 1.5$$
$$\text{Streak Bonus} = 1.0 + \ln(1 + \text{StreakDays}) \times 0.05$$
$$\text{Final EXP} = \lfloor \text{Base EXP} \times \text{IntensityRatio(RPE)} \times \text{Streak Bonus} \times \text{AffinityMultiplier} \times \text{Fluctuator} \rfloor$$

## Exception
- 입력 파라미터가 음수이거나 비정상적 수치(예: 체중 200kg 초과, 신장 30cm 미만)일 경우, 기본 안전값(Safety Default: 남성 70kg/175cm, 여성 55kg/162cm)으로 자동 교정 후 계산한다.

## Related Documents
- `01_ARCHITECTURE/FORMULA_REGISTRY.md`
- `03_BACKEND/EXERCISE_ENGINE.mdux`
- `03_GAME_SYSTEM/EXP_RULE.mdux`

## Change History
- 2026-07-31 (PATCH_006): SSOT 가이드라인 표준 규격 반영, 동적 수식 및 Fallback 정책 명세 체계화.