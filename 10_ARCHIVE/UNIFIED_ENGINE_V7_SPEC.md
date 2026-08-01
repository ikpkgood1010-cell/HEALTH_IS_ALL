# UNIFIED_ENGINE_V7_SPEC.md

## Purpose
건강 데이터(식단, 운동, 수면, 심박수) 분석과 게임 보상 메커니즘을 완벽하게 통합하는 Unified Engine V7의 사양을 정의합니다.

## Scope
* 백엔드 및 프론트엔드 공통 연산 로직
* 신체 상태 기반 동적 리워드 산출 공식
* 건강-게임 상호작용 규칙

## SSOT
* 본 문서는 V7 엔진의 계산 방식 및 통합 로직에 대한 단일 진실 공급원입니다.

## Definitions
* **TDEE (Total Daily Energy Expenditure)**: 일일 총 에너지 소비량.
* **Health Synergy Factor ($S_h$)**: 당일 건강 목표 달성도에 따라 보상 가율을 결정하는 $0.8 \sim 1.5$ 범위의 계수.

## Runtime
* 백엔드 Python 연산 모듈 및 프론트엔드 Dart 로컬 오프라인 계산 엔진 내 동시 작동.

## Rules
1. **정밀 TDEE 계산 공식**:
   $$TDEE = BMR \times ActivityLevel \times (1 + StressFactor - SleepFatiguePenalty)$$
   * $BMR$ (Mifflin-St Jeor): $10 \times weight + 6.25 \times height - 5 \times age + s$ ($s$: 남성 +5, 여성 -161)
   * $StressFactor$: 심박수 평균 대비 가중치 ($0.0 \sim 0.15$)
   * $SleepFatiguePenalty$: 수면 부족 비율 지수 ($0.0 \sim 0.10$)
2. 수식 계산 중 인자 오차 발생 시 기존 V6 간결 공식으로 Fallback 수행.

## State
* Active State: RUNNING_V7

## Event
* `EVENT_UNIFIED_CALCULATION_COMPLETED`: V7 통합 수식 계산 완료.

## Example
* 수면 효율 90% 이상 + 목표 식단 달성 시 $S_h = 1.35$ 적용, 퀘스트 완료 경험치 135% 획득.

## Exception
* 심박 데이터 미수집 시 $StressFactor = 0.0$으로 처리하여 수식 안전성 확보.

## Related Documents
* `HEALTH IS ALL/03_BACKEND/dynamic_health_engine_v7.py`
* `HEALTH IS ALL/01_ARCHITECTURE/RECOVERY_BALANCE_SPEC_V3.md`

## Change History
| 날짜 | 버전 | 작성자 | 변경 내용 |
| :--- | :--- | :--- | :--- |
| 2026-07-31 | V7.0.0 | Engine Team | V7 다변수 건강 수식 및 보상 통합 알고리즘 반영 |