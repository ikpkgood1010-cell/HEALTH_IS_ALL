# DYNAMIC_NUTRITION_FORMULA_SPEC.md

## Purpose
본 문서는 유저가 매일 동일하고 지루한 고정 칼로리 수치에 피로감을 느끼지 않도록, 기초대사량(BMR), 음식물 소화 흡수 열량(TEF), 운동 후 추가 산소 소비량(EPOC), 정령 친밀도 및 미세 생체 변수를 결합한 다변수 정밀 영양 수식 체계를 정의한다.

## Scope
1. Mifflin-St Jeor 기반 기초대사량(BMR) 동적 보정 수식
2. 섭취 3대 영양소(탄수화물, 단백질, 지방) 비율별 식이성 열효과(TEF) 정밀 산출
3. 운동 강도(METs) 및 EPOC 지수를 반영한 동적 칼로리 소모 공식
4. 정령 친밀도(Spirit Affinity) 수치에 따른 미세 성장 경험치 배율
5. 센서/데이터 입력 누락 시 하리스-베네딕트(Harris-Benedict) 간이 Fallback 수식 연동

## SSOT
본 문서는 백엔드 영양 계산 엔진(`backend/dynamic_nutrition_calculator.py`) 및 프론트엔드 영양 트래커 UI(`lib/dynamic_nutrition_tracker_widget.dart`)의 최상위 **SSOT(Single Source of Truth)**로 기능한다.

## Definitions
- **TEF (Thermic Effect of Food)**: 음식 소화 및 대사 과정에서 소비되는 열량 (단백질: 20~30%, 탄수화물: 5~10%, 지방: 0~3%).
- **EPOC (Excess Post-exercise Oxygen Consumption)**: 고강도 운동 후 휴식 상태에서도 지속되는 고대사 반응 소모 칼로리.

## Runtime
- 프론트엔드(Flutter): 실시간 대사량 그래프 표시, 친근하고 따뜻한 식단 피드백 팝업 출력.
- 백엔드(FastAPI/Python): 동적 영양소 분해, TEF 및 EPOC 정밀 산출, 정령 친밀도 반영 로직 실행.

## Rules
1. **정밀성과 다변수화**: 동일한 음식 및 운동을 기록하더라도 수면 회복 지수, 정령 친밀도, 당일 활동 패턴에 따라 매일 $1 \sim 5\%$ 내외의 정밀한 수치 변화를 제공하여 유저의 호기심과 재미를 유발한다.
2. **안전성 절차 (Fallback)**: 세부 영양 정보가 부족한 음식 입력 시 계산 오류를 예방하기 위해 표준 단백질/탄수화물 대사 비율 기반 간이 수식으로 안전하게 전환한다.
3. **호감형 대화 문구**: 칼로리 초과나 부족 시 부정적 경고 대신 "정령이 오늘 아주 건강한 에너지 원료를 공급받았어요! ✨", "조금 더 편안하게 휴식을 취해도 괜찮아요 🌿"와 같이 긍정적이고 호감 가는 인터페이스 문구를 사용한다.

## State
- `weight_kg`, `height_cm`, `age`, `gender`, `spirit_affinity_level`
- `protein_g`, `carbs_g`, `fat_g`, `workout_intensity_mets`, `workout_duration_min`
- `calculated_bmr`, `calculated_tef`, `calculated_epoc`, `total_dynamic_expenditure`

## Event
- `ON_MEAL_LOGGED`: 식단 영양소 입력 및 TEF 실시간 산출
- `ON_WORKOUT_LOGGED`: 운동 입력 및 EPOC 가중치 계산
- `ON_DYNAMIC_CALORIE_CALCULATED`: 일일 최종 동적 대사량 도출 및 정령 상태 업데이트

## Example
$$\text{BMR}_{\text{dynamic}} = (10 \times W + 6.25 \times H - 5 \times A + S) \times (1.0 + (\text{SpiritAffinity} \times 0.005)) \times \text{Jitter}$$
$$\text{TEF} = (\text{Protein}_{\text{kcal}} \times 0.25) + (\text{Carbs}_{\text{kcal}} \times 0.08) + (\text{Fat}_{\text{kcal}} \times 0.025)$$

## Exception
- 입력된 체중이 30kg 미만이거나 250kg 초과인 경우 정상 데이터 범주로 보정하여 표준 가이드라인을 제공한다.

## Related Documents
- `01_ARCHITECTURE/RECOVERY_BALANCE_SPEC.md`
- `01_ARCHITECTURE/SPIRIT_DIET_CATALYST_SPEC.md`
- `01_ARCHITECTURE/GUILD_CHALLENGE_SPEC.md`

## Change History
- 2026-07-31 (PATCH_012): 다변수 정밀 영양 및 대사 수식 명세 신규 작성 (SSOT 규격 준수).