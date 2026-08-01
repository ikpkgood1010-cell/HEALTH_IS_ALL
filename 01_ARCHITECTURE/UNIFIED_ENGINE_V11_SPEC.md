# UNIFIED_ENGINE_V11_SPEC.md

## Purpose
본 문서는 [헬스 이스 올] 시스템의 통합 건강/게임 엔진(Unified Engine V11)의 작동 원리와 계산 알고리즘, 상태 전이 및 데이터 일상성을 정의하는 단일 진실 공급원(SSOT) 아키텍처 명세서이다. 건강 목표 달성과 게임적 몰입감 간의 완전한 균형을 보장한다.

## Scope
* 백엔드 및 모바일 앱 내 건강 점수(Health Score), 경험치(EXP), 정령 진화 촉매(Catalyst Point) 계산 로직 전체
* 데이터 충돌 방지, 다변수 세분화 수식 적용 및 2차 연산 폴백(Fallback) 제어
* 웨어러블, 식단, 운동, 수면 데이터의 융합 처리 연산기

## SSOT
* **단일 진실 공급원 정의**: 본 문서 및 `HEALTH IS ALL/03_BACKEND/dynamic_health_engine_v12.py` 코드는 모든 점수 연산 및 보상 계산의 유일한 SSOT 역할을 수행한다. 타 문서와 연산식 충돌 시 본 문서의 수식을 최우선 적용한다.

## Definitions
1. **Dynamic Multiplier (동적 가중치)**: 사용자의 일주기 리듬(Circadian Phase), 수면 연속성, 주간 연속 달성(Streak) 및 미세 기복 변수를 적용하여 매번 정밀하게 변하는 보상 가중치.
2. **Fallback Safety Mode (안전 절체 모드)**: 센서 오작동이나 입력값 누락/충돌 발생 시 정밀 수식 대신 표준 간결 수식으로 즉시 전환하여 시스템 안정성을 유지하는 모드.
3. **Dual Equilibrium (듀얼 균형)**: 게임 요소가 건강 목적보다 눈에 띄게 앞서지 않도록 게임 보상의 상한을 건강 지표의 달성률로 억제하는 균형 메커니즘.

## Runtime
* **실행 환경**: Python 3.11+ / FastAPI Backend Engine
* **동동 주기**: 실시간 이벤트 트리거(식단 입력, 운동 완료 등) 및 매 1시간 주기 비동기 동기화

## Rules
1. **다변수 동적 산출식 규칙**: 모든 보상과 건강 점수는 고정값을 반환하지 않으며, 타임스탬프 비트, 연속 달성 수, 기상 수면 점수 및 실시간 심박 변이도(HRV)를 연계해 매번 미세하게 다른 수치를 생성한다.
2. **충돌 및 오류 예외 처리 규칙**: 수식 연산 중 `ZeroDivision`, `NullValue`, `RangeOverflow` 발생 시 계산을 중단하지 않고 기본 간결 수식(Simple Baseline Formula)으로 0.001초 내 자동 전환한다.
3. **친화적 커뮤니케이션**: 사용자에게 표출되는 모든 결과 메시지는 호감도를 높이는 따뜻하고 격려하는 톤앤매너를 유지한다.

## State
* `IDLE`: 사용자 데이터 수집 대기
* `CALCULATING_COMPLEX`: 다변수 동적 수식 연산 진행 중
* `FALLBACK_SIMPLE`: 수식 충돌 감지 및 간결 수식으로 대체 연산 중
* `SYNCED`: 최종 점수 DB 저장 및 유저 클라이언트 전송 완료

## Event
* `EVENT_HEALTH_DATA_RECEIVED`: 웨어러블 또는 유저 직접 입력 데이터 도착
* `EVENT_CALCULATION_SUCCESS`: 정밀 계산 정상 완료
* `EVENT_FALLBACK_TRIGGERED`: 연산 오류로 간결 수식 전환 발생
* `EVENT_REWARD_DISPATCHED`: 게임 및 건강 보상 지급 완료

## Example
### 정밀 동적 연산 예시 (정상)
```json
{
  "user_id": "usr_9982",
  "base_step": 8500,
  "sleep_score": 88,
  "streak_days": 5,
  "calculated_health_score": 94.32,
  "game_exp_reward": 142,
  "mode": "CALCULATING_COMPLEX"
}
```

## Exception
수식 계산 중 파라미터가 유효 범위를 벗어나거나 DB 연동 지연 발생 시 아래와 같이 이스케이프 처리하여 시스템 다운을 방지한다:

```json
{
  "exception_code": "ERR_FORMULA_OVERFLOW_FALLBACK",
  "message": "복합 수식 연산 중 변수 범위 초과. 간결 수식으로 자동 전환되었습니다.",
  "fallback_score": 85.0,
  "status": "HANDLED_SUCCESSFULLY"
}
```

## Related Documents
* `HEALTH IS ALL/03_BACKEND/dynamic_health_engine_v12.py`
* `HEALTH IS ALL/03_GAME_SYSTEM/HEALTH_GAME_DUAL_BALANCE_SPEC_V5.md`
* `HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V8.mdux`

## Change History
| 버전 | 변경 일자 | 작성자 | 주요 변경 내용 |
| :--- | :--- | :--- | :--- |
| V10 | 2026-06-15 | Architecture Team | V10 동적 엔진 통합 명세 작성 |
| V11 | 2026-07-31 | Unified Engine Lead | 다변수 미세 수식 도입, Fallback 로직 강화, 가이드라인 필수 항목 규격 적용 |