# RECOVERY_BALANCE_SPEC.md

## Purpose
본 문서는 스마트워치 및 웨어러블 센서로부터 수집되는 수면 데이터(깊은 수면, REM 수면, 총 수면 시간), HRV(심박 변동성) 및 근육 피로도를 바탕으로 유저의 일일 회복 지수(Recovery Score, $RS$)를 정밀 산출하고, 오버트레이닝 방지 및 정령의 '휴식 스킬(Rest Skill)' 보상 로직을 정의한다.

## Scope
1. 수면 단계별(Deep, REM, Light) 가중치 기반 수면 효율성($SE$) 산출
2. HRV(심박 변동성) 정상범위 대비 편차 분석 및 회복 지수($RS$) 계산
3. 회복 지수에 따른 AI 맞춤형 권장 운동 강도(Rest / Light / Moderate / High) 도출
4. 회복 지수 저조 시 오버트레이닝 경고 및 '휴식 스킬(Rest Aura)' 발동을 통한 성취감 보존
5. 수면/HRV 데이터 누락 시 자가 피로도 설문(1~10) 기반 Fallback 수식 연동

## SSOT
본 문서는 백엔드 회복 AI 엔진(`backend/recovery_ai_engine.py`) 및 프론트엔드 회복 위젯(`lib/recovery_balance_widget.dart`)의 최상위 **SSOT(Single Source of Truth)**로 기능한다.

## Definitions
- **Recovery Score ($RS$)**: 수면 질, HRV, 누적 피로도를 종합 평가한 0~100점 회복 상태 지표.
- **Deep Sleep Ratio**: 전체 수면 시간 중 깊은 수면(N3 단계)이 차지하는 비율 (권장 15~25%).
- **Rest Skill Aura**: 유저의 회복 지수가 높거나 권장 휴식을 이행했을 때 정령에게 부여되는 회복형 버프 패시브 스킬.

## Runtime
- 프론트엔드(Flutter): 수면 분석 결과 시각화, 당일 권장 운동 강도 가이드라인 및 휴식 스킬 게이지 출력.
- 백엔드(FastAPI/Python): 센서 데이터 파싱, 회복 지수 정밀 계산, AI 코칭 처방전 도출 및 DB 동기화.

## Rules
1. **건강 중심 본위 원칙**: 회복 지수가 저조($RS < 40$)함에도 고강도 운동을 강행할 경우, 정령이 '피로 과부하(Exhaustion)' 상태가 되어 획득 경험치가 50% 감쇄되며, 가벼운 스트레칭이나 휴식 취득 시 '휴식 스킬' 보너스가 지급된다.
2. **다변수 정밀 계산**: 수면 시간뿐만 아니라 깊은 수면 비율, HRV 지수, 주간 피로 누적치 및 미세 난수 인자($0.95 \sim 1.05$)가 종합 적용되어 매일 고유한 회복 수치를 산출한다.
3. **Fallback 정책**: 수면 센서 미착용 등으로 데이터가 누락된 경우, 유저의 자가 피로도 점수(1~10) 및 최근 7일 평균 수면 시간을 이용한 간이 Fallback 수식으로 즉시 전환한다.

## State
- `sleep_duration_hours`, `deep_sleep_ratio`, `rem_sleep_ratio`, `hrv_ms`, `subjective_fatigue`
- `recovery_score`, `recommended_intensity` (REST, LIGHT, MODERATE, HIGH)
- `rest_skill_active`, `spirit_stamina_buff`

## Event
- `ON_SLEEP_DATA_RECEIVED`: 수면 및 HRV 텔레메트리 수신
- `ON_RECOVERY_SCORE_CALCULATED`: 일일 회복 지수 확정 및 AI 코칭 생성
- `ON_REST_RECOMMENDED`: 고피로 상태 진입 시 휴식 미션 우선 전환
- `ON_RECOVERY_FALLBACK_USED`: 데이터 유실 시 자가 평가 Fallback 발동

## Example
$$SE = \left(\frac{\text{DeepSleepMin} \times 1.5 + \text{REMMin} \times 1.2 + \text{LightMin} \times 0.8}{\text{TotalSleepMin}}\right) \times 100$$
$$RS = \left( (SE \times 0.4) + \left(\min(100, \frac{\text{HRV}}{60} \times 100) \times 0.4\right) + ((10 - \text{Fatigue}) \times 2.0) \right) \times \text{Jitter}$$

## Exception
- 수면 수집 데이터가 1시간 미만이거나 18시간 초과인 경우 측정 오류로 간주하여 직전 3일간의 평균 회복 지수($RS$)로 자동 보정한다.

## Related Documents
- `01_ARCHITECTURE/SPIRIT_DIET_CATALYST_SPEC.md`
- `01_ARCHITECTURE/RAID_QUEST_SPEC.md`
- `01_ARCHITECTURE/WEARABLE_HEARTRATE_SPEC.md`

## Change History
- 2026-07-31 (PATCH_011): AI 수면-회복 지수 및 휴식 스킬 시스템 명세 신규 작성 (SSOT 규격 준수).