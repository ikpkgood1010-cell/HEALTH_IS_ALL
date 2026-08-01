# QA_TEST_STRATEGY_V6.md

## Purpose
V6 패치에 적용된 다변수 동적 연산의 정확성과 예외 발생 시 폴백 메커니즘의 안정성을 검증합니다.

## Scope
* 단위 테스트(Unit Test), 통합 연산 검증, 모바일 UI 글자 잘림 방지 테스트.

## SSOT
* `HEALTH IS ALL/06_QA/QA_TEST_STRATEGY_V6.md`

## Definitions
* **Boundary Dynamic Testing**: HRV=0, 수면시간=0, 체중=0 등 극단적 경계값 입력 시 시스템 정상 작동 여부 검증.

## Runtime
* PyTest (Backend) / Flutter Test Runner (Frontend)

## Rules
1. 모든 dynamic 수식은 null 또는 0 이하 입력 시 오류 없이 0.05초 이내에 Fallback 모드로 전환되어야 한다.
2. 모바일 디바이스 350px 해상도 환경에서 텍스트 잘림 현상이 전혀 없어야 한다.

## State
* `TEST_PLANNED`, `TEST_EXECUTING`, `TEST_PASSED`

## Event
* `ON_QA_SUITE_COMPLETE`

## Example
* PyTest 실행: `pytest backend/test_dynamic_health_v6.py` -> 100% Pass 필수.

## Exception
* 연산 오차범위가 ±1% 초과 시 빌드 실패 처리.

## Related Documents
* `HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V6_SPEC.md`

## Change History
* **V5.0**: V5 QA 전략 수립.
* **V6.0 (2026-07-31)**: V6 다변수 수식 검증 및 폴백 테스트 자동화 시나리오 추가.