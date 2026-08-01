# UNIFIED_ENGINE_V9_SPEC.md

## Purpose
본 문서는 'HEALTH IS ALL' 앱의 핵심엔진인 통합 건강-게임 Dual Engine v9의 아키텍처와 로직을 정의합니다. 건강 관리의 정확성과 몰입감 높은 RPG 게임성을 동시에 최고 수준으로 유지하도록 보장합니다.

## Scope
* 모바일 프론트엔드와 백엔드 API 간의 실시간 건강-게임 데이터 동기화
* 다변수 기반 동적 건강/영양/운동/정령(Spirit) 계산 엔진
* 오프라인 상태 처리 및 멱등성(Idempotency) 보장 통합 메카닉

## SSOT
* **경로**: `HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V9_SPEC.md`
* **소유팀**: Core System Architecture Team

## Definitions
* **Dual Engine**: 건강 지표(운동, 식단, 수면)와 게임 지표(EXP, 정령 성장, 퀘스트)를 1:1 정밀 대칭으로 연동하는 통합 처리부.
* **Fallback Formula**: 복잡한 다변수 연산 시 에러나 데이터 누락 발생 시 즉각 전환되는 안정형 간결 수식.

## Runtime
* **실행 환경**: Python 3.11+ / Flutter 3.x Cross-Platform
* **동기화주기**: 실시간 센서 수집 및 5분 단위 백그라운드 동기화

## Rules
1. 건강 데이터의 정확성을 훼손하지 않으면서 RPG 성장 경험을 제공한다.
2. 모든 수치는 정적 계산이 아닌 사용자 생체 및 시간 변수를 결합하여 매번 유기적으로 다르게 산출한다.
3. 시스템 장애 시 유저 데이터 손실 없이 간결한 1단계 폴백 수식으로 자동 전환한다.

## State
* `INIT`: 엔진 초기화 상태
* `SYNCING`: 건강 데이터 및 센서 수집 상태
* `CALCULATING`: 동적 수식 연산 상태
* `IDLE`: 연산 완료 및 결과 대기 상태

## Event
* `ON_HEALTH_DATA_RECEIVED`: 새로운 생체/식단 데이터 수집
* `ON_CALCULATION_SUCCESS`: 계산 완료 및 결과 전달
* `ON_ENGINE_FALLBACK`: 연산 오류 발생 시 폴백 수식 실행

## Example
* 사용자가 찜 요리로 식단을 입력하고 30분 산책을 완료하면, 체내 대사 가중치 및 활동 변수가 적용되어 단순 칼로리 차감이 아닌 정령 속성 성장과 일일 활력 수치가 다차원 연산되어 반영됨.

## Exception
* 센서 데이터 부정확성: 이동평균 필터(SMA) 적용 후 보정치 산출
* 네트워크 단절: Local Database 저장 후 재연결 시 Outbox 패턴으로 복구

## Related Documents
* `HEALTH IS ALL/03_BACKEND/dynamic_health_engine_v9.py`
* `HEALTH IS ALL/03_GAME_SYSTEM/HEALTH_GAME_DUAL_BALANCE_SPEC_V2.md`
* `HEALTH IS ALL/05_AI/HEALTH_FEEDBACK_INTELLIGENCE_SPEC_V8.md`

## Change History
* **v9.0.0 (2026-07-31)**: V8 대비 다변수 동적 계산식 도입, 정령 감성 반응 강화, 표준 가이드라인 전면 적용.