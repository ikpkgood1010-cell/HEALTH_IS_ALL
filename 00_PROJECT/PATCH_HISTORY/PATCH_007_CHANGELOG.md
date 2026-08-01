# PATCH_007_CHANGELOG.md

## Purpose
Patch 007에서 추가, 변경, 개선된 전체 시스템 명세와 아키텍처 변경 이력을 단일 진실 공급원(SSOT) 기준으로 기록합니다.

## Scope
* Unified Engine V7 통합 수식 및 오프라인 동기화 프로토콜
* 수면 및 피로도 기반 Recovery Balance V3 엔진
* 백엔드 dynamic_health_engine_v7, diet_spirit_engine_v7, offline_sync_engine_v7
* 프론트엔드 Dynamic Nutrition UI V7 및 AI Health Feedback V7

## SSOT
* 본 문서는 Patch 007에 포함된 모든 변경 사항의 단일 최상위 기록 문서입니다.

## Definitions
* **Patch 007**: 다변수 정밀 건강 수식과 게임 리워드 가중치가 상호 작용하도록 고도화된 통합 업데이트.
* **Soft Clamp**: 계산식의 극단적 결과값으로 인한 오류를 방지하기 위해 상하한선을 안전하게 제어하는 기법.

## Runtime
* Execution Context: Flutter 3.x Frontend / Python 3.11 FastAPI Backend / PostgreSQL 15 + Redis.

## Rules
1. 게임 요소가 건강 관리의 본질적 목적을 가리지 않도록 UI 및 보상 비중을 5:5 밸런스로 유지한다.
2. 모든 수식 계산 시 변수 이상값 입력 시 1단계 간결 공식(Fallback Formula)으로 자동 전환한다.

## State
* Status: APPLIED (Patch 007 반영 완료)

## Event
* `EVENT_PATCH_007_APPLIED`: 패치 007 시스템 적용 완료 이벤트.

## Example
* HRV 및 수면 효율 지표가 가중 적용되어 당일 수령 경험치와 스피릿 컨디션이 실시간 조정됨.

## Exception
* 계산 파라미터 누락 시 기본 표준치(BMR 표준값 등)로 대체 계산 수행.

## Related Documents
* `HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V7_SPEC.md`
* `HEALTH IS ALL/00_PROJECT_START/DEVELOPMENT_ROADMAP_V7.md`

## Change History
| 날짜 | 버전 | 작성자 | 변경 내용 |
| :--- | :--- | :--- | :--- |
| 2026-07-31 | V7.0.0 | System Architecture | Patch 007 통합 이력 최초 작성 및 V7 사양 확정 |