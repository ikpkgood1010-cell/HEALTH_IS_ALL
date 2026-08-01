# DYNAMIC FORMULA REGISTRY V5 SPECIFICATION

## Purpose
본 문서는 'HEALTH IS ALL' 서비스 내 건강 데이터(BMR, TDEE, 수면/회복도, 마크로 영양 균형)와 게임 요소(EXP, 스피릿 친밀도, 촉매 드랍률)를 결합하는 세분화된 정밀 다변수 계산 공식을 정의한다. 단조로운 수치 반복을 방지하기 위해 다원적 변수를 적용하며, 센서/데이터 누락 시 안전하게 작동하는 Fallback 단계를 명시한다.

## Scope
- 사용자 신체 계측 데이터 기반 dynamic BMR/TDEE 계산식
- 심뇌혈관/심박변이도(HRV) 기반 회복 점수 및 운동 가속 지수
- 영양소(탄/단/지/식이섬유/당류) 정밀 계산 및 스피릿 시너지 포뮬러
- 예외 발생 시 Graceful Fallback 1단계 간결 공식 전환 규칙

## SSOT (Single Source of Truth)
- 본 문서는 앱 전역의 건강 및 게임 보상 동적 포뮬러에 대한 유일한 진실의 근원(SSOT)이다.

## Definitions
- **Multi-Variable Formula**: 단순 체중/활동량 외 HRV, 수면 질, 식단 밸런스, 당류 감점 요소를 동적으로 합산하는 고급 계산식.
- **Fallback Level 1**: 웨어러블 데이터나 세부 영양 성분 누락 시, 기본적인 Mifflin-St Jeor 공식 및 기본 비율로 안전하게 전환하는 로직.

## Runtime
- 백엔드 `dynamic_health_engine_v5.py` 및 클라이언트 `dynamic_health_calculator_v2.dart` 실시간 동기화 실행.

## Rules
1. **건강 지표 우월성 및 게임 완충 법칙**: 정밀 계산식은 사용자의 실제 건강 상태를 정확히 반영해야 하며, 게임 보상이 건강 지표를 왜곡하거나 가리지 않도록 밸런스를 유지한다.
2. **다변수 변동성 적용**: 매일 동일한 운동을 하더라도 수면 상태, 수분 섭취, 정제당 제한 여부에 따라 보상 수치 및 스피릿 반응에 동적 변동폭(±15%)을 부여한다.
3. **오류 안전장치**: 다변수 계산 중 `None`, `ZeroDivision`, `Out-of-Bounds` 입력 발생 시 즉시 Fallback Level 1 공식으로 자동 전환한다.

## State
- `FormulaState`: `PRECISION_MODE` | `FALLBACK_LEVEL_1` | `DEGRADED_MODE`

## Event
- `ON_HEALTH_METRIC_LOGGED`: 신체/운동/식단 데이터 수집 완료 시 포뮬러 엔진 재계산 트리거.
- `ON_FORMULA_FALLBACK_TRIGGERED`: 데이터 이상치 탐지 시 간결 공식으로 자동 전환 이벤트 발생.

## Example
- **정밀 TDEE 계산 예시**:
  - `Base_BMR` = 10 * weight(kg) + 6.25 * height(cm) - 5 * age(years) + s (성별변수)
  - `Activity_Mult` = 1.2 + (Daily_Steps / 10000) * 0.375 + (Workout_Intensity_Index * 0.2)
  - `HRV_Recovery_Factor` = clamp(Current_HRV / Baseline_HRV, 0.8, 1.2)
  - `Final_TDEE` = Base_BMR * Activity_Mult * HRV_Recovery_Factor

## Exception
- 웨어러블 심박수 데이터 누락 시: `HRV_Recovery_Factor` = 1.0 (Fallback Level 1 적용)
- 당류/식이섬유 미입력 시: 표준 마크로 비율(50:30:20) 적용 및 기본 시너지 지급.

## Related Documents
- `HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V5_SPEC.md`
- `HEALTH IS ALL/03_BACKEND/dynamic_health_engine_v5.py`
- `HEALTH IS ALL/03_GAME_SYSTEM/DYNAMIC_REWARD_CALCULATOR_SPEC.md`

## Change History
- v5.0.0 (2026-07-31): 다변수 정밀 계산식 추가, Fallback Level 1 명세 표준화, SSOT 및 챗GPT 표준 가이드라인 구조 준수.