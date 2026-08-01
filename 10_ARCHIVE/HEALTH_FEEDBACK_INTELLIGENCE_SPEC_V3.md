# HEALTH_FEEDBACK_INTELLIGENCE_SPEC_V3.md

## Purpose
사용자에게 친근하고 동기부여를 제공하는 AI 건강 피드백 텍스트 생성 시스템 규칙을 규정합니다.

## Scope
* 식단 기록 후 AI 피드백 메시지, 정령 대화 팝업 문구, 일일 요약 보고서 톤앤매너.

## SSOT
* `HEALTH IS ALL/05_AI/HEALTH_FEEDBACK_INTELLIGENCE_SPEC_V3.md`

## Definitions
* **Friendly Coach Voice**: 기계적인 지시문이 아닌, 따뜻하고 공감하는 피어(Peer) 스타일의 대화체.

## Runtime
* 온디바이스 AI 텍스트 생성기 / 백엔드 AI 에이전트 서비스

## Rules
1. 전문 용어는 최소화하고, 직관적인 표현을 사용한다. (예: BMR 달성 -> "오늘 숨만 쉬어도 타는 에너지를 알차게 채웠어요!")
2. 건강 개선점 전달 시 반드시 긍정적 칭찬을 먼저 배치하는 '샌드위치 피드백' 구조 적용.

## State
* `GENERATING_TEXT`, `TEXT_READY`

## Event
* `ON_HEALTH_FEEDBACK_REQUEST`

## Example
* "오늘 당류 섭취가 적절했어요! 저녁에 약간의 단백질만 더해주면 정령도 한층 더 힘을 낼 거예요!"

## Exception
* AI 피드백 생성 실패 시 사전 정의된 표준 응원 문구 상자에서 즉시 반환.

## Related Documents
* `HEALTH IS ALL/05_AI/COMPANION_PERSONALITY_V3_SPEC.md`

## Change History
* **V2.0**: 피드백 기본 로직 구축.
* **V3.0 (2026-07-31)**: 호감적 대화체 가이드라인 고도화 및 샌드위치 피드백 패턴 표준화.