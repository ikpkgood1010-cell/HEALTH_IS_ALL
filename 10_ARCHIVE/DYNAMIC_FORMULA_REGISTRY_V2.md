# DYNAMIC FORMULA REGISTRY V2

## Purpose
사용자가 매번 동일한 수치나 단조로운 계산 결과에 지루함을 느끼지 않도록, 운동, 식단, 건강 상태 및 정령 성장에 다중 변수(심박수 변동성, 수면 효율, 식단 클린도 등)가 복합적으로 작용하는 정밀 동적 계산식을 정의합니다.

## Scope
- 백엔드 엔진 계산 모듈 (`dynamic_health_engine.py`, `diet_spirit_engine.py`)
- 프론트엔드 실시간 수치 반영 위젯

## SSOT
- `HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V2.md`

## Definitions
- **변수 가중치 (Variable Weight):** 사용자 생체 데이터 및 행동 로그가 계산 결과에 미치는 영향도 계수.
- **시너지 멀티플라이어 (Synergy Multiplier):** 클린 식단(당/밀가루/튀김 제외, 찜 요리 등)과 고강도 활동이 결합될 때 발생하는 추가 보너스 계수.

## Runtime
- 사용자가 운동/식단 로그를 제출하거나 웨어러블 데이터가 동기화되는 즉시 실행됩니다.

## Rules
1. 동일한 조건이 반복되더라도 미세한 생체 변수(예: ±2% 이내의 컨디션 변동)를 반영하여 결과값이 매번 다이내믹하게 산출되어야 합니다.
2. 계산식 내에서 0으로 나누기 오류나 오버플로 위험이 감지될 경우, 즉시 한 단계 간결한 백업 산술식으로 자동 전환됩니다.
3. 게임 요소와 건강 요소의 가치가 상호 침해하지 않도록 균형을 유지합니다.

## State
- `formula_version`: v2.0
- `active_variables`: [heart_rate, sleep_score, meal_cleanliness_index, consecutive_days]

## Event
- `FORMULA_CALCULATION_TRIGGERED`
- `DYNAMIC_VARIANCE_APPLIED`

## Example
- 건강 점수 계산식: $Score = (Base_{Cal} \times 0.4) + (Sleep_{Eff} \times 0.3) + (Diet_{Clean} \times 0.3) \times Multiplier$

## Exception
- 센서 데이터 누락 시 기본값(Baseline)을 적용하고 로그에 경고를 기록합니다.

## Related Documents
- `HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_NUTRITION_FORMULA_SPEC.md`
- `HEALTH IS ALL/01_ARCHITECTURE/HEART_RATE_CALORIE_SPEC.md`

## Change History
- v1.0 (2026-01-15): 초기 고정 계산식 도입
- v2.0 (2026-07-31): 다중 변수 동적 수식 및 예외 처리 로직 고도화