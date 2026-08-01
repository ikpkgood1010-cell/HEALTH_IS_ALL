# HEALTH_DYNAMIC_TIP_FEEDER_SPEC_V1.md

## Purpose
본 문서는 사용자 개인별 생체 정보, 당일 영양/운동 기록, 수면 및 정령 상태 등의 다중 변수를 기반으로 1~3줄 분량의 호감형·이용자 친화적 건강/식단/운동 꿀팁을 동적으로 산출하고 제공하는 AI 피더(Feeder) 엔진 및 인터페이스 사양을 정의함을 목적으로 한다.

## Scope
1. 백엔드 `user_friendly_dialogue_manager_v2.py` 및 `HEALTH_TIPS_TRICKS_FEEDER_V2.md` 연동 로직
2. 1~3줄 맞춤형 건강/식단/운동 꿀팁의 세분화/정밀화된 동적 계산 수식 적용
3. 계산식 충돌/예외 발생 시 간결한 표준 계산식으로의 Fallback 제어 로직
4. 게임성(정령 대화, 친밀도, 보상)과 건강성(영양, 수면, 운동)의 최고 수준 듀얼 밸런스 UI/UX 표현 규칙

## SSOT (Single Source of Truth)
* **시스템 아키텍처 SSOT**: `HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V10_SPEC.md`
* **대화 및 팁 제어 SSOT**: `HEALTH IS ALL/05_AI/HEALTH_FEEDBACK_INTELLIGENCE_SPEC_V9.md`
* **게임-건강 밸런스 SSOT**: `HEALTH IS ALL/03_GAME_SYSTEM/HEALTH_GAME_DUAL_BALANCE_SPEC_V3`

## Definitions
* **Dynamic Tip Index (DTI)**: 복합 생체 지수와 당일 영양 달성률을 반영하여 출력할 꿀팁 카테고리 및 톤앤매너를 결정하는 동적 지표.
* **Fallback Safety Engine (FSE)**: 고차원 변수 수식 연산 중 데이터 누락 또는 오버플로우 발생 시, 1단계 단순화된 검증 수식으로 즉각 전환하여 시스템 중단을 방지하는 안전장치.
* **Dual Balance HUD**: 건강 데이터(탄단지, 칼로리, 심박수)와 게임 요소(정령 대사, 경험치 획득)가 서로 가려지지 않고 공존하는 최상위 UI 오버레이.

## Runtime
* **실행 시점**: 
  1. 앱 메인 화면 진입 시 (일일 최초 1회 또는 4시간 간격 갱신)
  2. 식단 등록 / 운동 기록 완료 즉시 (이벤트 기반 갱신)
  3. 정령 캐릭터 터치 및 퀘스트 완료 시
* **실행 환경**: 백엔드 Python FastAPI (`user_friendly_dialogue_manager_v2.py`) 및 프론트엔드 Flutter (`interactive_spirit_widget_v2.dart`) 오버레이 연동.

## Rules
1. **분량 제한**: 사용자 가독성을 극대화하기 위해 출력 문구는 반드시 **1~3줄 이내(최대 120자)**로 제한한다.
2. **어조 및 호감도**: 친근하고 격려하며, 딱딱한 명령조가 아닌 따뜻한 조언자 및 게임 속 정령 파트너의 어조를 유지한다.
3. **듀얼 밸런스 원칙**: 게임성이 시각적으로 너무 가볍게 튀지 않도록, 건강 데이터 표현과 정령 인터랙션의 화면 비중을 5:5로 정밀 조정한다.
4. **동적 변수화**: 사용자가 매번 동일한 문구를 보지 않도록 당일 칼로리 소모량, 수면 점수, 현재 시간대, 정령 친밀도 변수를 수식에 조합한다.

## State
* `TIP_STATE_IDLE`: 꿀팁 생성 대기 상태.
* `TIP_STATE_CALCULATING`: 정밀 변수 연산 중.
* `TIP_STATE_FALLBACK`: 변수 오류 발생으로 간결 수식 전환 상태.
* `TIP_STATE_DISPLAYED`: UI 화면 표출 및 정령 반응 수행 중.

## Event
| 이벤트명 | 발생 조건 | 수행 동작 |
| :--- | :--- | :--- |
| `EVENT_MEAL_LOGGED` | 식단 입력 완료 | 당일 탄단지 비율 계산 후 1~3줄 영양 꿀팁 생성 |
| `EVENT_WORKOUT_COMPLETED` | 운동 기록 저장 | 수분 섭취 및 단백질 보충 관련 꿀팁 표출 |
| `EVENT_SPIRIT_TOUCHED` | 메인 화면 정령 클릭 | 현재 시간/수면 점수 기반 다이내믹 피드백 표출 |

## Rules & Dynamic Formulas (정밀 계산식 및 Fallback)

### 1. 정밀 동적 팁 지수 계산식 (Advanced Formula)
$$DTI = \left( \frac{\text{Calorie\_Ratio} \times 0.4 + \text{Protein\_Ratio} \times 0.3 + \text{Sleep\_Factor} \times 0.3}{\text{Activity\_Level}} \right) \times \left(1 + \sin\left(\frac{\text{Hour}}{24} \times 2\pi\right) \times 0.15\right)$$

* `Calorie_Ratio`: 당일 섭취 칼로리 / 목표 칼로리
* `Protein_Ratio`: 당일 단백질 섭취량(g) / 목표 단백질량(g)
* `Sleep_Factor`: 전날 수면점수 / 100
* `Activity_Level`: METs 기반 활동 지수 (기본값: 1.2 ~ 2.0)
* `Hour`: 현재 시간 (0 ~ 23)

### 2. Fallback 간결 계산식 (Basic Safety Formula)
고차원 변수 중 누락 또는 연산 오류 발생 시 아래 간결 수식으로 즉시 전환한다.
$$DTI_{basic} = \frac{\text{Current\_Calories}}{\text{Target\_Calories}}$$

### 3. DTI 결과에 따른 1~3줄 맞춤 꿀팁 도출 매핑
* **DTI < 0.8 (영양/에너지 부족)**:
  * "오늘 목표까지 조금 더 힘낼 수 있어요! 단백질 위주의 간식을 가볍게 챙겨볼까요? 정령도 당신의 에너지를 기다리고 있어요!"
* **0.8 <= DTI <= 1.2 (최적 균형 상태)**:
  * "완벽한 식단 밸런스예요! 영양소가 골고루 채워져 정령의 생기 에너지가 20% 상승했습니다. 지금 기분을 계속 유지해봐요!"
* **DTI > 1.2 (에너지 과다/수면 필요)**:
  * "오늘 활동량이 든든하게 채워졌네요! 가벼운 산책이나 스트레칭으로 소화를 돕고, 따뜻한 물 한 잔으로 마무리를 추천해요."

## Example
```json
{
  "user_id": "usr_9981",
  "dti_score": 1.05,
  "formula_used": "Advanced_Formula_v10",
  "tip_category": "NUTRITION_BALANCED",
  "display_text": "완벽한 식단 밸런스예요! 영양소가 골고루 채워져 정령의 생기 에너지가 20% 상승했습니다. 지금 기분을 계속 유지해봐요!",
  "spirit_emotion_state": "HAPPY",
  "reward_exp_bonus": 15
}
```

## Exception
1. **사용자 생체 데이터(BMR, 목표 칼로리 등) 미입력 시**:
   * 국가 표준 영양 가이드라인 기본값(성인 기준 2000kcal, 단백질 60g)을 자동 대입 후 Fallback 수식으로 작동.
2. **동적 계산 중 0으로 나누기(Divide by Zero) 예외 발생 시**:
   * 즉시 `TIP_STATE_FALLBACK` 상태로 변경되어 안전한 표준 꿀팁 문구 출력.

## Related Documents
* `HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V10_SPEC.md`
* `HEALTH IS ALL/03_BACKEND/user_friendly_dialogue_manager_v2.py`
* `HEALTH IS ALL/05_AI/HEALTH_TIPS_TRICKS_FEEDER_V2.md`
* `HEALTH IS ALL/04_FRONTEND/DYNAMIC_NUTRITION_UI_SPEC_V10.md`

## Change History
| 버전 | 변경 날짜 | 작성자 | 변경 상세 내용 |
| :--- | :--- | :--- | :--- |
| V1.0 | 2026-07-31 | AI Engine Team | 최초 명세서 작성. 정밀 동적 팁 계산식 및 Fallback 로직, 게임-건강 듀얼 밸런스 가이드라인 명시. |