# HEALTH FEEDBACK INTELLIGENCE SPEC

## Purpose
사용자의 식단 기록(당/밀가루/튀김 제외 여부, 찜 요리 선호 등)과 운동 성과를 분석하여, 이용자 친화적이고 호감 넘치는 대화 및 동기부여 피드백을 제공하는 AI 지능형 스펙을 정의합니다.

## Scope
- AI 컴패니언 대화 정책
- 건강 피드백 팝업 및 알림 메시지 생성

## SSOT
- `HEALTH IS ALL/05_AI/HEALTH_FEEDBACK_INTELLIGENCE_SPEC.md`

## Definitions
- **공감형 코칭 (Empathic Coaching):** 사용자의 피로도와 식단 노력을 먼저 인정하고 긍정적인 방향으로 유도하는 대화 톤.

## Runtime
- 식단 및 운동 완료 로그가 시스템에 등록된 직후 실행.

## Rules
1. 지시적이거나 강압적인 말투를 배제하고, 따뜻하고 매력적인 컴패니언 페르소나를 유지합니다.
2. 클린 식단 성과나 운동 지속성에 대해 구체적인 수치를 언급하며 칭찬합니다.

## State
- `ai_mood`: Encouraging & Supportive
- `response_latency`: < 1.2s

## Event
- `AI_FEEDBACK_REQUESTED`
- `COMPANION_DIALOGUE_TRIGGERED`

## Example
- "오늘도 당과 밀가루를 멀리하고 담백한 찜 요리로 건강을 지키셨군요! 정령도 함께 기뻐하고 있어요."

## Exception
- AI 응답 지연 시 사전 정의된 친화적 예비 메시지 출력.

## Related Documents
- `HEALTH IS ALL/05_AI/COMPANION_PERSONALITY.md`
- `HEALTH IS ALL/05_AI/DIALOGUE_POLICY.md`

## Change History
- v1.0 (2026-01-25): 초기 AI 대화 룰 정의
- v2.0 (2026-07-31): 식단 및 건강 맞춤형 공감 코칭 알고리즘 통합