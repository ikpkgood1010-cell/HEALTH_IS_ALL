DOMAIN_EVENT_CATALOG

Purpose
본 문서는 비즈니스 상태 변화가 발생했을 때 발행되는 모든 도메인 이벤트(Domain Event)의 사양, 페이로드 구조 및 처리 규칙을 관리하는 SSOT이다.

Scope
백엔드 Domain, Application Service, Outbox Event Relayer 및 이벤트 Consumer 서비스 전반에 적용된다.

SSOT
도메인 이벤트의 명칭, 속성, Producer, Consumer 정의의 단일 진실 출처이다.

Rules
1. Naming Convention: [AggregateName][PastTenseAction]Event 형식 적용 (예: HabitCompletedEvent).
2. Payload Minimization: Event Payload에는 엔티티 전체 객체를 포함하지 않고, Event ID, 발생 시각, 관련 Aggregate ID, 변경된 최소 델타값만 포함한다.
3. Idempotency: 모든 Consumer는 동일한 Event ID를 수신했을 때 멱등(Idempotent)하게 동작해야 한다.

Domain Event Catalog Table


Event ID
Producer Aggregate
Payload Schema
Version
Default Consumer
Retry / Idempotent
Trigger Condition

EVT_DOM_HABIT_COMPLETED
HabitAggregate
habitId, userId, streakCount, timestamp
1.0.0
QuestEngine, CompanionEngine
Retry 3 / Idempotent
사용자가 습관 달성을 완료했을 때

EVT_DOM_WORKOUT_RECORDED
WorkoutAggregate
workoutId, userId, calories, duration
1.0.0
ExpEngine, HealthScoreEngine
Retry 3 / Idempotent
운동 기록 저장이 정상 완료되었을 때

EVT_DOM_MEAL_ANALYZED
MealAggregate
mealId, userId, totalCal, macroRatio
1.0.0
HealthScoreEngine, QuestEngine
Retry 3 / Idempotent
식단 AI 분석 완료 또는 로컬 등록 시

EVT_DOM_GOAL_COMPLETED
QuestAggregate
goalId, userId, rewardPoints
1.0.0
EconomyEngine, NotificationEngine
Retry 5 / Idempotent
설정된 목표 조건이 100% 충족되었을 때

EVT_DOM_COMPANION_LEVEL_UP
CompanionAggregate
companionId, userId, newLevel
1.0.0
UI/RenderEngine, AudioEngine
Retry 1 / Idempotent
건강이(Companion) 경험치가 임계점 도과 시



Runtime Impact
• 비동기 분산 이벤트를 통해 트랜잭션 격리성을 확보하고 시스템 확장성을 보장한다.

Examples
json
{
  "eventId": "evt_dom_workout_12345",
  "eventType": "WorkoutRecordedEvent",
  "aggregateId": "wrk_9982",
  "occurredOn": "2026-07-31T04:19:22Z",
  "payload": {
    "userId": "usr_7711",
    "totalCalories": 320,
    "durationMinutes": 45
  }
}


Forbidden
• ​Domain Event에 민감 정보(비밀번호, 상세 생체 데이터 등 PII)를 암호화 없이 포함하는 행위 금지.
• ​Consumer가 이벤트를 수신한 후 다른 도메인 이벤트를 다시 동기(Synchronous) 방식으로 재발행하여 순환 고리를 만드는 행위 금지.
​Related Documents
• ​03_BACKEND/DDD/AGGREGATE_BOUNDARY.md
• ​03_BACKEND/OUTBOX_EVENT_POLICY.md
​Change History
• ​v1.0.0 (2026-07-31): Initial catalog setup with standard Companion naming.