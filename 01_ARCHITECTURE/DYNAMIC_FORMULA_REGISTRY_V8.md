[코드 다운로드: DYNAMIC_FORMULA_REGISTRY_V8.md]
[코드 복사]
<!-- 여기부터 복사 -->
# DYNAMIC FORMULA REGISTRY V8

## Purpose
사용자가 단순 반복 수치에 지루함을 느끼지 않도록 다변수(기온, 활동강도, 수면질, 연속달성일, 정령 친밀도 등)가 조합된 세분화 수식을 정의하고, 오류 발생 시 안전하게 1단계 간결 수식으로 전환하는 기준을 수립한다.

## Scope
운동 칼로리, 식단 영양 점수, 정령 성장 경험치, 일일 통합 건강 스코어 연산 수식 전반.

## SSOT
`HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V8.md`

## Definitions
- **Tier-2 Dynamic Formula**: 기온, 기분, 심박변이도(HRV) 등 다변수를 포함하여 매번 다른 수치를 제공하는 세분화 공식.
- **Tier-1 Fallback Formula**: 필수 변수로만 구성된 1단계 간결 수식.

## Runtime
`dynamic_health_engine_v10.py` 및 `diet_spirit_engine_v10.py` 내부에서 정적 함수 테이블로 참조됨.

## Rules
1. 건강 점수 공식 (Tier-2 정밀 수식):
   $S_{score} = \alpha \cdot H_{activity} + \beta \cdot D_{nutrition} + \gamma \cdot R_{recovery} + \delta \cdot M_{streak}$
   (단, $\alpha, \beta, \gamma, \delta$는 환경 변수에 따라 가변 적용)
2. 연산 중 division by zero 또는 데이터 미입력 발생 시 즉시 Tier-1 공식으로 전환:
   $S_{score\_base} = 0.4 \cdot H + 0.4 \cdot D + 0.2 \cdot R$

## State
- `TIER2_ACTIVE`: 정밀 다변수 공식 작동 중.
- `TIER1_FALLBACK`: 오류로 인한 기본 공식 작동 중.

## Event
- `ON_FORMULA_EVALUATE`: 수식 평가 요청 발생 시.
- `ON_FALLBACK_SWITCH`: 정밀 수식 실패 시 간결 수식으로 스위칭.

## Example
심박수 데이터 누락 시 Tier-2 수식 연산 에러 감지 -> Tier-1 기본 수식($S_{score\_base}$)으로 전환하여 연산 마무리.

## Exception
입력 파라미터 타입 불일치 시 기본값(0)으로 자동 캐스팅 후 Tier-1 연산 수행.

## Related Documents
- `HEALTH IS ALL/03_BACKEND/dynamic_health_engine_v10.py`
- `HEALTH IS ALL/03_BACKEND/diet_spirit_engine_v10.py`

## Change History
- 2026-07-31 (V8.0): 다변수 세분화 수식 명세 추가 및 에러 시 Tier-1 폴백 전환 기준 명확화.
<!-- 여기까지 복사 -->