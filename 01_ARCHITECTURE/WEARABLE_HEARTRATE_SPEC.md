# WEARABLE_HEARTRATE_SPEC.md

## Purpose
본 문서는 스마트워치(Apple Health, Health Connect) 등 웨어러블 디바이스로부터 수집되는 실시간 심박수(BPM) 텔레메트리 데이터를 분석하여, 심박 구간(Heart Rate Zone 1~5), EPOC 기반 동적 칼로리, 정령의 아우라 버프 수치를 정밀 산출하는 시스템 명세를 정의한다.

## Scope
1. Tanaka 공식을 활용한 연령별 최대 심박수($HR_{\text{max}}$) 및 Target HR Zone 분류
2. Keytel 수식 기반 성별/체중/심박수/시간 다변수 동적 칼로리 산출
3. 고강도 운동(Zone 4~5) 지속 시간에 따른 EPOC(Excess Post-exercise Oxygen Consumption) 칼로리 추가 보상 수식
4. 웨어러블 센서 이탈 또는 데이터 유실 시 METs(운동대사량) 기반 Fallback 전환 로직

## SSOT
본 문서는 백엔드 심박수 엔진(`backend/heartrate_calorie_engine.py`) 및 프론트엔드 심박 위젯(`lib/heartrate_spirit_widget.dart`)의 최상위 **SSOT(Single Source of Truth)**로 기능한다.

## Definitions
- **Heart Rate Zone (HR Zone)**: 최대 심박수 대비 현재 심박수 비율에 따른 5단계 운동 강도 구간 (Zone 1: 회복, Zone 2: 지방 연소, Zone 3: 유산소, Zone 4: 무산소, Zone 5: 극한).
- **EPOC Bonus**: Zone 4 이상에서의 운동 종료 후 추가 산소 소비에 의해 발생하는 동적 신진대사 칼로리 추가점수.
- **Spirit Aura Buff**: 현재 HR Zone에 따라 정령의 능력치가 일시적으로 증폭되는 특수 아우라 효과.

## Runtime
- 프론트엔드(Flutter): HealthKit/Health Connect SDK 연동, 1초 단위 BPM 수신, 심박 구간 UI 및 정령 아우라 이펙트 갱신.
- 백엔드(FastAPI/Python): 센서 노이즈 필터링, EPOC 다변수 수식 검증 및 유저 일일 대사량 칼로리 DB 동기화.

## Rules
1. **건강 중심 원칙**: 무리한 고심박 유지를 방지하기 위해 Zone 5(극강 구간)가 10분 이상 지속될 경우 '안전 경고Notification'를 즉시 발동하고 정령의 아우라 과부하(Overheat) 상태를 유도하여 휴식을 권장한다.
2. **정밀 다변수 산출**: 단순 평균 심박수가 아닌 시초 단위 심박 변동성(HRV) 지표와 미세 난수 인자가 적용되어 매번 정밀한 소비 칼로리 값을 도출한다.
3. **Fallback 정책**: 웨어러블 착용 해제 등으로 심박 데이터가 끊길 경우, 기존 운동 종목의 표준 METs 기반 칼로리 수식으로 즉시 교체되어 기록 연속성을 유지한다.

## State
- `user_age`, `user_weight_kg`, `user_gender`, `current_bpm`, `target_hr_zone`
- `epoc_accumulated_cal`, `spirit_aura_state` (IDLE, WARMUP, FAT_BURN, AEROBIC, ANAEROBIC, OVERHEAT)

## Event
- `ON_HEARTRATE_STREAM_RECEIVED`: 실시간 BPM 수신 및 Zone 계산
- `ON_ZONE_CHANGED`: 심박 구간 이동에 따른 정령 아우라 변환
- `ON_SAFETY_WARNING_TRIGGERED`: Zone 5 과도 지속 시 안전 휴식 알림
- `ON_HEARTRATE_SENSOR_LOST`: 심박 데이터 유실 시 METs Fallback 전환

## Example
$$HR_{\text{max}} = 208 - (0.7 \times \text{Age})$$
$$\text{Calorie (Male)} = \left[ (-55.0969 + (0.6309 \times \text{HR}) + (0.1988 \times \text{Weight}) + (0.2017 \times \text{Age})) / 4.184 \right] \times 60 \times \text{Hours}$$
$$\text{EPOC Bonus} = \text{Zone 4 Min} \times 1.8 + \text{Zone 5 Min} \times 3.2$$

## Exception
- BPM 측정값이 30 미만 또는 230 초과인 경우 이상치(Outlier)로 간주하고 이전 직전 5초 간의 이동 평균값(Moving Average)으로 보정한다.

## Related Documents
- `01_ARCHITECTURE/SPIRIT_DIET_CATALYST_SPEC.md`
- `01_ARCHITECTURE/RAID_QUEST_SPEC.md`
- `03_BACKEND/HEARTRATE_ENGINE.mdux`

## Change History
- 2026-07-31 (PATCH_010): 실시간 웨어러블 심박수 분석 및 동적 칼로리/정령 아우라 명세 신규 작성 (SSOT 규격 준수).