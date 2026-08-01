EVENT_DEPENDENCY_MATRIX

Purpose
본 문서는 이벤트 간 발행(Producer) 및 소비(Consumer)의 의존 관계, 처리 우선순위를 정의하고 무한 순환 이벤트 루프(Event Loop)를 예방한다.

Event Dependency Mapping Table


Producer Domain
Event ID
Consumer Domain
Priority
Retry Max
Secondary Event Triggered

User Action
EVT_USER_LOG_RECORDED
HealthScoreEngine
High (1)
3
EVT_HEALTH_SCORE_UPDATED

Health Engine
EVT_HEALTH_SCORE_UPDATED
EmotionEngine
High (2)
1
EVT_AI_EMOTION_CHANGED

Emotion Engine
EVT_AI_EMOTION_CHANGED
RenderEngine / UI
Medium (3)
0
None

Schedule
EVT_DAILY_RESET_TRIGGERED
SyncEngine / Memory
Critical (0)
5
EVT_MEMORY_SUMMARY_CREATED



Strict Anti-Event-Loop Rules
1. No Circular Triggering: A 이벤트의 Result로 발행된 B 이벤트가 어떠한 가공을 거쳐 다시 A 이벤트를 직접/간접 재발행하는 구조를 엄격히 금지한다.
2. Max Chain Depth: 하나의 유저 행동으로부터 촉발되는 연속 이벤트 체인의 깊이(Depth)는 최대 4단계를 초과할 수 없다.

Related Documents
• 01_ARCHITECTURE/EVENT_TRIGGER_MASTER.md