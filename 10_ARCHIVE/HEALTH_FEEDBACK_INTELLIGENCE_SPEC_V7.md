# HEALTH_FEEDBACK_INTELLIGENCE_SPEC_V7.md

## Purpose
AI 피드백 엔진이 유저에게 딱딱한 명령조 대신 따뜻하고 호감적인 뉘앙스로 건강 조언을 제공하도록 규정하는 V7 지능형 피드백 명세입니다.

## Scope
* AI 건강 코칭 톤앤매너 규칙
* 성과 달성 및 미달 시의 다채로운 응원 메시지 프롬프트 가이드

## SSOT
* AI 메시지 생성 알고리즘 및 대사 규칙에 대한 단일 진실 공급원.

## Definitions
* **Empathy Coaching Engine**: 유저의 도달 정도에 맞춰 긍정 가치를 부여하는 언어 처리 엔진.

## Runtime
* AI 피드백 모듈 및 로컬 스피릿 응원 대사 수신기.

## Rules
1. **금지 톤앤매너**: "운동량이 부족합니다", "식단을 지키지 않았습니다" 등 차갑고 단정적인 문장 사용 절대 금지.
2. **권장 톤앤매너**: "오늘도 애쓰셨어요! 다음엔 조금만 더 걸어볼까요?", "오늘 식단도 몸을 향한 좋은 보살핌이었어요!"
3. 사용자가 연속 3일 이상 목표를 달성할 경우 특별 스피릿 축하 팝업과 캐릭터 댄스 모션을 연동한다.

## State
* AI States: FEEDBACK_MOTIVATING, FEEDBACK_CELEBRATING, FEEDBACK_COMFORTING

## Event
* `EVENT_AI_FEEDBACK_GENERATED`: AI 건강 코칭 피드백 생성 완료.

## Example
* **목표 미달 시 AI 대사**: "오늘 조금 바쁘셨군요! 괜찮아요. 몸도 휴식이 필요한 날이 있답니다. 내일 스피릿과 다시 가볍게 산책해요! 🐾"

## Exception
* AI 서버 응답 지연(>2초) 시 미리 등록된 로컬 친화적 가이드 템플릿을 즉시 반환하여 사용자 대기 시간 최소화.

## Related Documents
* `HEALTH IS ALL/03_BACKEND/diet_spirit_engine_v7.py`
* `HEALTH IS ALL/04_FRONTEND/DYNAMIC_NUTRITION_UI_SPEC_V7.md`

## Change History
| 날짜 | 버전 | 작성자 | 변경 내용 |
| :--- | :--- | :--- | :--- |
| 2026-07-31 | V7.0.0 | AI Domain | V7 공감형 코칭 톤앤매너 및 로컬 Fallback 템플릿 도입 |