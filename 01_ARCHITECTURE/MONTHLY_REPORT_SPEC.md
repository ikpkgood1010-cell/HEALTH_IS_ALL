# MONTHLY_REPORT_SPEC.md

## Purpose
본 문서는 유저의 한 달간 운동량(유산소/근력), 식단 밸런스(탄단지 및 미량 영양소), 정령 성장 히스토리를 종합하여 한 눈에 시각화하고 다정한 응원 메시지를 전달하는 월간 힐링 리포트 엔진 규격을 정의한다.

## Scope
1. 30일간의 일일 운동/영양/수분 섭취 데이터 자동 집계 및 가중 평균 계산
2. 월간 건강 개선 지수($Monthly Health Improvement Index, MHII$) 산출
3. 건강 변화에 따른 수호 정령의 성장 궤적 및 힐링 코멘트 생성
4. 유저 친화적 다정한 요약 카드 UI 연동

## SSOT
본 문서는 월간 리포트 백엔드 엔진(`backend/monthly_report_engine.py`) 및 프론트엔드 리포트 위젯(`lib/monthly_report_widget.dart`)의 최상위 **SSOT(Single Source of Truth)**로 기능한다.

## Definitions
- **Monthly Health Improvement Index ($MHII$)**: 월간 총 걸음 수, 영양 균형 유지율, 수분 달성률, 정령 친밀도를 종합 산출한 $0.0 \sim 100.0$ 점수.
- **Spirit Healing Summary**: 한 달간 유저의 노력을 정령의 시선에서 따뜻하게 격려하는 대화형 텍스트.

## Runtime
- 프론트엔드(Flutter): 월간 성과 차트, 정령 배지, 다정한 힐링 코멘트 팝업 출력.
- 백엔드(FastAPI/Python): 30일간의 로그 파싱, $MHII$ 계산, 월간 성장 요약 도출.

## Rules
1. **건강 본위와 게임 요소의 균형**: 단순히 게임 레벨업만을 보여주는 것이 아니라, 실질적인 혈당/체중/영양 밸런스 개선 성과가 정령의 성장에 어떻게 기여했는지 상호 연동한다.
2. **다정한 어조 유지**: 목표 미달 수치가 있더라도 "부족함" 대신 "다음 달에는 조금 더 따스한 햇살을 쬐어볼까요? 🌿"와 같은 호감형 문구를 사용한다.
3. **세분화 동적 수식**: 30일간의 데이터 변동성과 $0.97 \sim 1.03$ 난수 지터를 조합하여 정밀 수식을 적용한다.

## State
- `monthly_avg_steps`, `monthly_nutri_score`
- `monthly_water_avg_ml`, `mhii_score`
- `spirit_summary_text`

## Event
- `ON_MONTHLY_REPORT_GENERATED`: 월말 시점 리포트 자동 생성 이벤트
- `ON_MONTHLY_BADGE_AWARDED`: 월간 달성 배지 및 정령 특수 스킨 지급

## Example
$$MHII = \left( \frac{\text{AvgSteps}}{10000} \times 35 + \text{AvgNutri} \times 0.45 + \frac{\text{AvgWater}}{2000} \times 20 \right) \times \text{Jitter}$$

## Exception
- 30일 중 기록된 데이터가 7일 미만인 경우, '데이터 모으는 중' 모드로 안전 전환하여 부족한 데이터로 인한 착시 수치 생성을 방지한다.

## Related Documents
- `01_ARCHITECTURE/NUTRITION_ANALYTICS_SPEC.md`
- `01_ARCHITECTURE/GUILD_CHALLENGE_SPEC.md`

## Change History
- 2026-07-31 (PATCH_016): 글로벌 월간 힐링 리포트 명세서 신규 작성 (SSOT 규격 준수).