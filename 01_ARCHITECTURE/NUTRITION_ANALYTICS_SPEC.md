# NUTRITION_ANALYTICS_SPEC.md

## Purpose
본 문서는 유저의 일일 식단 기록을 바탕으로 탄수화물, 단백질, 지방 등 대량 영양소뿐만 아니라 식이섬유, 수분 등 미량 요소의 결핍을 탐지하고, 유저 선호 조리법(찜, 클린 식단)에 맞춘 다정한 맞춤형 레시피를 추천하는 AI 영양 분석 엔진 규격을 정의한다.

## Scope
1. 영양 결핍 지수($Nutritional Deficiency Index, NDI$) 계산 알고리즘
2. 알코올, 당류, 정제 밀가루, 튀김류 배제 및 건강한 섭취 위주의 AI 맞춤 레시피 필터링
3. 식단 개선 시 정령 속성(특히 풀/빛 속성) 추가 경험치 부여 로직
4. 분석 결과를 유저 친화적이고 다정한 어조의 인터페이스 카드로 변환
5. 식단 데이터 누락 시 기본 권장 영양 가이드를 제공하는 Fallback 처리

## SSOT
본 문서는 영양 분석 백엔드 엔진(`backend/nutrition_analytics_engine.py`) 및 프론트엔드 분석 위젯(`lib/nutrition_analytics_widget.dart`)의 최상위 **SSOT(Single Source of Truth)**로 기능한다.

## Definitions
- **Nutritional Deficiency Index ($NDI$)**: 권장 섭취량 대비 부족한 영양소 수치를 종합한 결핍 지수($0.0 \sim 1.0$).
- **Clean Recipe Recommendation**: 정제당 및 튀김을 배제하고 원물 식재료의 조리 방식을 우선하는 건강 추천 식단.

## Runtime
- 프론트엔드(Flutter): 영양소 밸런스 레이더/프로그레스 차트, 다정한 레시피 카드, 정령 조언 팝업 출력.
- 백엔드(FastAPI/Python): 영양 성분 파싱, $NDI$ 산출, 결핍 영양소 보충형 클린 식단 매칭.

## Rules
1. **건강 중심 본위 원칙**: 게임적 보상만을 위해 과도한 칼로리 섭취를 유도하지 않으며, 영양 밸런스가 충족되었을 때만 정령의 '빛 속성' 성장을 극대화한다.
2. **긍정적이고 따뜻한 대화**: "영양 불균형 심각"이라는 표현을 피하고 "오늘 식단에 푸른 야채나 깔끔하게 삶은 단백질을 조금 더해주시면 정령이 더욱 건강해질 거예요 🌿"라는 어조를 유지한다.
3. **변수 세분화 수식**: Target 칼로리 대비 섭취율, 단백질 충족도, 식이섬유 비중 및 $0.97 \sim 1.03$ 난수를 승산 적용한다.

## State
- `target_kcal`, `consumed_kcal`
- `protein_gap_g`, `fiber_gap_g`
- `deficiency_index`, `recommended_recipe_title`

## Event
- `ON_MEAL_ANALYSIS_REQUESTED`: 식단 데이터 분석 요청
- `ON_RECIPE_RECOMMENDED`: 부족한 영양소 보충 레시피 매칭
- `ON_BALANCED_MEAL_ACHIEVED`: 영양 밸런스 달성 및 정령 경험치 지급

## Example
$$NDI = \left( \frac{\text{ProteinGap}}{TargetP} \times 0.45 + \frac{\text{FiberGap}}{TargetF} \times 0.55 \right) \times \text{Jitter}$$

## Exception
- 입력된 음식 칼로리가 0 이하이거나 영양 데이터 정보가 유실된 경우 기본 밸런스 가이드 모드로 안전하게 자동 전환한다.

## Related Documents
- `01_ARCHITECTURE/SPIRIT_EVOLUTION_SPEC.md`
- `01_ARCHITECTURE/NUTRITION_QUEST_SPEC.md`

## Change History
- 2026-07-31 (PATCH_015): AI 영양 심화 분석 & 레시피 추천 시스템 명세 신규 작성 (SSOT 규격 준수).