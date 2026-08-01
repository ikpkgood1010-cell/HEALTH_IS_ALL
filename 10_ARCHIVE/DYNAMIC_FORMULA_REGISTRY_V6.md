# DYNAMIC_FORMULA_REGISTRY_V6.md

## Purpose
앱 내 모든 건강, 영양, 정령 성장 및 게임 보상 연산에 사용되는 정밀 수학 공식을 등록하고 관리합니다.

## Scope
* BMR, TDEE, 정령 시너지 보상, 퀘스트 EXP, 수면 부채 반영 수식 전체.

## SSOT
* `HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V6.md`

## Definitions
* **Dynamic Active BMR ($BMR_{dyn}$)**: 표준 BMR에 수면 연속성 지수 및 일주기 변화량을 곱한 값.

## Runtime
* 수학적 연산은 파이썬 NumPy/Flutter Dart Math 라이브러리로 실행.

## Rules
1. **Dynamic BMR**:
   $$BMR_{dyn} = (10 \times W + 6.25 \times H - 5 \times A + S) \times (0.95 + 0.1 \times \sin(HRV_{norm}))$$
2. **Dynamic Reward EXP**:
   $$EXP_{gain} = BaseEXP \times \frac{ActualCal}{TargetCal} \times (1.0 + 0.05 \times SpiritAffinity)$$
3. **Fallback Formula**:
   $$BMR_{base} = 10 \times W + 6.25 \times H - 5 \times A + S$$

## State
* `FORMULA_VALIDATED`, `FORMULA_DEPRECATED`

## Event
* `FORMULA_UPDATE_EVENT`

## Example
* 체중 70kg, 키 175cm, 나이 30세, 남성(S=+5), $HRV_{norm}=0.8$ 시 $BMR_{dyn} \approx 1792.4$ kcal.

## Exception
* $HRV_{norm}$ 연산 불가능 시 $BMR_{base}$ 사용.

## Related Documents
* `HEALTH IS ALL/03_BACKEND/dynamic_health_engine_v6.py`

## Change History
* **V5.0**: 기본 가중치 등록.
* **V6.0 (2026-07-31)**: 삼각함수 및 HRV 기반 수치 다변화 수식 추가, 폴백 수식 표준화.