# ECONOMY BALANCE MASTER SPEC

## Purpose
게임 내 보상 시스템과 실제 건강 관리(운동, 식단) 노력 간의 완벽한 평형을 유지하여, 게임 요소가 건강 본질을 압도하거나 반대로 게임이 허접해지지 않도록 최고 수준의 밸런스를 보장합니다.

## Scope
- 인게임 재화 획득 공식
- 상점 및 정령 성장 경제 구조
- 안티 그라인드(Anti-Grind) 정책 연동

## SSOT
- `HEALTH IS ALL/03_GAME_SYSTEM/ECONOMY_BALANCE_MASTER_SPEC.md`

## Definitions
- **실행 기반 가치 (Execution-Based Value):** 실제 운동 시간 및 식단 준수도에 비례하여 재화가 지급되는 비율.
- **인플레이션 방지 계수 (Inflation Control Factor):** 장기 플레이 시 재화 가치 하락을 막기 위한 동적 회수 메커니즘.

## Runtime
- 매일 자정 리셋 및 활동 데이터 제출 시 실시간 반영.

## Rules
1. 게임 내 재화는 반드시 실질적인 건강 활동(운동, 식단 기록)을 통해서만 효율적으로 획득할 수 있어야 합니다.
2. 어뷰징이나 반복 입력(무한 노가다)을 방지하기 위해 일일 획득 상한선 및 동적 감소 계수가 적용됩니다.

## State
- `economy_tier`: Tier-1 Balanced
- `inflation_rate`: 0.02%

## Event
- `REWARD_DISTRIBUTED`
- `ECONOMY_BALANCE_CHECK`

## Example
- 운동 30분 완료 시: 기본 경험치 + 동적 건강 기여도 기반 코인 지급.

## Exception
- 비정상적인 대량 데이터 입력 시 트랜잭션 차단 및 관리자 로그 기록.

## Related Documents
- `HEALTH IS ALL/03_GAME_SYSTEM/ANTI_GRIND_POLICY.md`
- `HEALTH IS ALL/03_GAME_SYSTEM/ECONOMY_MASTER.md`

## Change History
- v1.0 (2026-01-20): 초기 경제 모델 설계
- v2.0 (2026-07-31): 건강-게임 기여도 동적 밸런스 알고리즘 전면 개편