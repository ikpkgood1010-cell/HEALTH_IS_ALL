# SPIRIT_EVOLUTION_SPEC.md

## Purpose
본 문서는 유저의 영양소 섭취 밸런스(탄수화물, 단백질, 지방 비율), 운동 유형(유산소, 무산소) 및 수면 회복 지수에 따라 유저의 정령이 4대 속성(불, 물, 풀, 빛)으로 동적 진화하는 AI 맞춤형 속성 진화 메카닉의 기술적 요구사항과 수식을 정의한다.

## Scope
1. 3대 영양소 및 운동 데이터 기반 정령 속성 가중치 점수($Elemental Score$) 정밀 산출
2. 4대 속성(불: 단백질/근력, 물: 수분/유산소, 풀: 식이섬유/휴식, 빛: 균형 영양/출석) 진화 트리 도출
3. 진화 단계별 정령 visual representation 및 친근한 호감형 대화 인터랙션 팝업 연동
4. 속성 균형 상실 시 특정 속성 편중 방지를 위한 동적 밸런싱 인자($Soft Cap$) 적용
5. 영양/운동 데이터 부족 시 기본 정령 형태를 유지하는 안전한 Fallback 로직 연동

## SSOT
본 문서는 정령 진화 엔진(`backend/spirit_evolution_engine.py`) 및 프론트엔드 진화 UI (`lib/spirit_evolution_widget.dart`)의 최상위 **SSOT(Single Source of Truth)**로 기능한다.

## Definitions
- **Elemental Score ($ES$)**: 유저의 건강 활동 성향에 따라 실시간으로 축적되는 속성별(Fire, Water, Earth, Light) 경험치 점수.
- **Spirit Affinity Level**: 유저와 정령 간의 호감도 단계로, 정령의 진화 조건 및 보너스 능력치 배율을 결정함.

## Runtime
- 프론트엔드(Flutter): 정령의 속성 변화 시각화, 터치 시 호감형 반응 대화창 및 진화 연출 팝업 출력.
- 백엔드(FastAPI/Python): 영양/운동 로그 파싱, 4대 속성 점수 정밀 계산, 진화 조건 검증 및 DB 동기화.

## Rules
1. **건강 중심 본위 원칙**: 단백질만 과다 섭취하거나 영양 불균형이 심할 경우, 불 속성이 비정상적으로 과열(Overheat)되어 정령이 피로 상태에 빠지므로, 전속성 균형 섭취 시 '빛 속성' 최고 진화 형태를 제공한다.
2. **유저 친화적 대화 인터페이스**: 진화 및 상태 변화 시 부정적 평가 대신 "오늘 단백질과 유산소가 정령에게 고른 에너지를 주었어요! ✨", "조금 더 상큼한 채소를 채워주시면 정령이 풀 속성으로 예쁘게 싹을 틔울 거예요 🌿"와 같이 호감 가득한 메시지를 전달한다.
3. **다변수 동적 수식**: 섭취 칼로리뿐만 아니라 영양소 비율, 수면 점수, 주간 연속 달성일 및 $0.96 \sim 1.04$ 범위의 난수 인자가 종합 작용하여 매일 유일무이한 속성 점수를 생성한다.

## State
- `fire_score`, `water_score`, `earth_score`, `light_score`
- `current_stage` (EGG, BABY, JUNIOR, SENIOR, MASTER)
- `dominant_element` (FIRE, WATER, EARTH, LIGHT, BALANCED)
- `spirit_affinity_exp`, `is_overheated`

## Event
- `ON_NUTRITION_LOGGED`: 영양소 입력에 따른 속성 점수 분배
- `ON_WORKOUT_LOGGED`: 운동 유형별 속성 가중치 부여
- `ON_EVOLUTION_TRIGGERED`: 정령 진화 조건 충족 및 진화 연출 트리거
- `ON_SPIRIT_TOUCHED`: 정령 터치 시 호감형 대화 팝업 트리거

## Example
$$ES_{\text{Fire}} = (\text{Protein}_{g} \times 2.5 + \text{StrengthMin} \times 4.0) \times \left(1.0 + \frac{\text{Affinity}}{100}\right) \times \text{Jitter}$$
$$ES_{\text{Light}} = \left(\frac{\text{BalancedDays} \times 50}{\text{UnbalanceIndex}}\right) \times \text{RecoveryScore} \times 0.1$$

## Exception
- 영양/운동 기록이 3일 이상 유실될 경우 정령은 잠시 휴식 모드(Slumber)에 돌입하며, 복귀 즉시 따뜻한 환영 팝업 메시지와 함께 기존 경험치를 안전하게 유지한다.

## Related Documents
- `01_ARCHITECTURE/DYNAMIC_NUTRITION_FORMULA_SPEC.md`
- `01_ARCHITECTURE/RECOVERY_BALANCE_SPEC.md`
- `01_ARCHITECTURE/GUILD_CHALLENGE_SPEC.md`

## Change History
- 2026-07-31 (PATCH_013): AI 맞춤형 정령 속성 진화 시스템 명세 신규 작성 (SSOT 규격 준수).