# [중복문서-덮어쓰기, 교체] Dynamic Formula Registry V3

## Purpose
사용자가 매번 동일한 수치와 반복적인 보상에 지루함을 느끼지 않도록, 생체 리듬, 연속 달성 일수(Streak), 시간대별 변수, 무작위 가중치를 결합한 **고도화된 다변수 동적 계산 공식**을 정의합니다.

## Scope
- 칼로리 소모량, 식단 클린도 지수, 정령 성장 경험치, 길드 기여도 산출 공식 전체

## SSOT
- 이 문서는 모든 백엔드 및 프론트엔드 계산식 로직의 절대적인 기준(Single Source of Truth)입니다.

## Definitions
- **Dynamic Factor (DF)**: 사용자 상태와 외부 변수에 따라 매번 다르게 적용되는 가중치 계수.
- **Fatigue Diminishing Return (FDR)**: 동일 패턴 반복 시 발생하는 효율 감소 방지 보정값.

## Runtime
- 서버사이드 및 클라이언트 로컬 계산 시 실시간 적용 (오프라인 동기화 시 서버 기준 재검증).

## Rules
1. 단순 정수 계산을 지양하고, 소수점 둘째 자리까지 정밀 연산 후 UI에 반영합니다.
2. 모든 공식에는 변수 간 충돌 방지를 위한 상한선(Max Cap)과 하한선(Min Floor)을 설정합니다.

## State
- 계산기 상태 값은 실시간 캐시(`DynamicStateCache`)에 저장됩니다.

## Event
- `EVENT_FORMULA_RECALCULATED`: 활동 데이터 입력 시 윈도우 단위로 트리거됩니다.

## Example
- 기본 칼로리 공식: BaseCalories * (1 + (StreakDays * 0.02)) * RandomFactor(0.95 ~ 1.05)

## Exception
- 네트워크 단절 시 로컬 기본 수식으로 자동 전환 후 재연결 시 동기화합니다.

## Related Documents
- `HEALTH IS ALL/03_BACKEND/dynamic_health_engine_v3.py`
- `HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY.md`

## Change History
- v3.0 (2026-07-31): 다변수 무작위 가중치 및 FDR(피로도 감소 보정) 도입