[코드 다운로드: UNIFIED_ENGINE_V10_SPEC.md]
[코드 복사]
<!-- 여기부터 복사 -->
# UNIFIED ENGINE V10 SPECIFICATION

## Purpose
HEALTH IS ALL 프로젝트의 핵심 연산 엔진으로서 건강 지표 연산과 게임적 요소(정령, 퀘스트, 보상)를 통합 관리하며, 게임성이 건강 목적을 가리지 않도록 듀얼 밸런스(Dual-Balance)를 조율하는 중앙 제어 시스템의 명세이다.

## Scope
백엔드 연산 엔진 전체(`dynamic_health_engine`, `diet_spirit_engine`, `wearable_sync_engine` 등)와 프론트엔드 상태 동기화 영역을 포함한다.

## SSOT
`HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V10_SPEC.md`

## Definitions
- **Dual-Balance Engine**: 건강 측정치와 게임적 재미 요소의 비중을 5:5로 정밀 유지하며 주객전도를 방지하는 메커니즘.
- **Dynamic Formula Cascade**: 세분화된 변수를 적용하되 연산 오류 시 1단계 간결 수식으로 자동 전환되는 폴백 체계.

## Runtime
서버 백엔드 실행 시 상시 백그라운드 스레드 및 API 응답 루프에서 호출됨.

## Rules
1. 게임 보상은 사용자의 실체적 건강 활동(운동, 식단기록, 수면)에 기반해서만 지급한다.
2. 게임 요소(애니메이션, 팝업, 이펙트)가 건강 수치 시각화 화면을 가리거나 주객전도되지 않도록 UI 레이어 순서를 보장한다.
3. 건강 점수 계산 시 다변수 수식을 우선 사용하고, 변수 누락/연산 에러 시 Tier-1 기본 수식으로 즉시 전환한다.

## State
- `IDLE`: 사용자 요청 대기 상태.
- `CALCULATING`: 건강 및 정령 시너지 다변수 연산 수행 중.
- `FALLBACK_TRIGGERED`: 오류 발생으로 인한 1단계 간결 수식 적용 상태.

## Event
- `EVT_HEALTH_DATA_RECEIVED`: 웨어러블/입력 데이터 수신 시 연산 가동.
- `EVT_CALCULATION_ERROR`: 세분화 수식 처리 실패 시 발생.

## Example
사용자의 심박수 및 식단 수치 수신 -> 정밀 시너지 수식 계산 진행 -> 데이터 이상 감지 시 간결 수식(기본 칼로리/점수 연산)으로 안전 처리 후 결과 반환.

## Exception
모든 데이터 값이 NULL이거나 범위를 벗어날 경우 기본 보정치(Default Baseline)를 할당하여 앱 튕김 현상을 방지한다.

## Related Documents
- `HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V8.md`
- `HEALTH IS ALL/03_GAME_SYSTEM/HEALTH_GAME_DUAL_BALANCE_SPEC_V3.md`

## Change History
- 2026-07-31 (V10.0): 게임성-건강의 최고 상태 유지 듀얼 밸런스 규칙 강화 및 다변수 수식 안전 폴백 구조 적용.
<!-- 여기까지 복사 -->