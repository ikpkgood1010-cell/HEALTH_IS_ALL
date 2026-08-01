# [중복문서-덮어쓰기, 교체] Spirit Evolution Expansion Specification

## Purpose
건강 관리 활동(식단 준수, 운동, 수면)이 정령의 진화 및 상호작용에 미치는 영향력을 확장하여, 게임의 몰입감을 극대화합니다.

## Scope
- 정령 진화 단계, 촉매 반응식, 스킨 및 속성 변화 규칙

## SSOT
- 정령 성장 및 진화 시스템의 단일 진실 공급원(SSOT)

## Definitions
- **Diet Catalyst**: 설탕/밀가루/튀김 제한 식단을 실천했을 때 정령에게 부여되는 특수 성장 에너지.
- **Evolution Resonance**: 누적된 건강 점수가 특정 임계점을 넘을 때 발생하는 연출 및 능력치 개방.

## Runtime
- 사용자가 식단/운동을 로깅하고 서버 동기화가 완료되는 시점에 즉시 판정.

## Rules
1. 건강 요소를 소홀히 하면 정령의 성장 속도가 감소하되, 게임 오버나 가혹한 페널티 대신 따뜻한 격려 팝업과 함께 회복 기회를 제공합니다.
2. 진화 시 다변수 통계를 기반으로 고유한 시각적 효과와 타이틀이 부여됩니다.

## State
- 정령 상태는 `SpiritState` 모델에 동기화되며 로컬에 캐시됩니다.

## Event
- `EVENT_SPIRIT_EVOLVED`: 진화 조건 충족 시 발생.

## Example
- 식단 클린도 100점 3일 연속 달성 시 -> '청정의 정령'으로 진화 촉발.

## Exception
- 데이터 유실 시 마지막 백업 시점의 정령 경험치로 무손실 복구.

## Related Documents
- `HEALTH IS ALL/03_BACKEND/diet_spirit_engine_v3.py`
- `HEALTH IS ALL/01_ARCHITECTURE/SPIRIT_EVOLUTION_SPEC.md`

## Change History
- v3.0 (2026-07-31): 식단 클린도 연동 진화 촉매 시스템 구체화