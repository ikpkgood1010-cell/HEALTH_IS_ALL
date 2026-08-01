# UNIFIED_ENGINE_V6_SPEC.md

## Purpose
건강 데이터와 게임 요소를 결합한 V6 통합 엔진의 아키텍처 및 작동 규칙을 정의합니다.

## Scope
* 건강 계산(BMR, 활동 칼로리, 영양소 매칭) 및 게임 보상(EXP, 정령 Affinity, 퀘스트 승점)의 일치성 보장.

## SSOT
* `HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V6_SPEC.md`

## Definitions
* **Circadian Modifier ($C_m$)**: 사용자의 활동 시간에 따른 생체 리듬 가중치 (0.9 ~ 1.15).
* **HRV Volatility Index ($V_{hrv}$)**: 심박 변동성에 따른 컨디션 가수치.

## Runtime
* 실행 환경: Python FastAPI Backend Service / Flutter Offline Local Engine

## Rules
1. 게임 보상 계산식은 사용자의 실제 건강 달성률과 직결된다.
2. 입력 변수에 오류나 누락이 있을 경우, 시스템 중단 없이 `Fallback_Formula`로 동적 전환한다.
3. 건강 정보는 사용자 인터페이스 상단에 항상 명확히 표시된다.

## State
* `ENGINE_READY`, `PROCESSING_DYNAMIC_METRICS`, `FALLBACK_TRIGGERED`, `COMPLETED`

## Event
* `ON_HEALTH_DATA_INPUT`, `ON_CALCULATION_SUCCESS`, `ON_FALLBACK_EXECUTE`

## Example
* 수면 부족 시 정령 소모 칼로리 효율성 보정치 $C_m = 0.92$ 적용.

## Exception
* 모든 입력 수치가 Null일 경우 기본 권장 칼로리(2000kcal) 기반 기본 보상 반환.

## Related Documents
* `HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V6.md`
* `HEALTH IS ALL/03_BACKEND/dynamic_health_engine_v6.py`

## Change History
* **V5.0**: V5 단일 가중치 로직 구축.
* **V6.0 (2026-07-31)**: 다변수 세분화 공식 추가, 지루함 방지 무작위 유기적 변수 연동, 2단계 폴백 안전 레이어 추가.