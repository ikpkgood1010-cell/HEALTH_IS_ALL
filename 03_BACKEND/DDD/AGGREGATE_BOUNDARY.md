AGGREGATE_BOUNDARY

Purpose
본 문서는 백엔드 도메인 주도 설계(DDD)의 핵심인 Aggregate의 경계를 명확히 정의하고, 도메인 모델 간의 무분별한 직접 참조 및 데이터 불일치를 방지하는 SSOT 표준이다.

Scope
백엔드 도메인 레이어의 모든 Aggregate Root, Entity, Value Object(VO) 설계 및 수정에 적용된다.

SSOT
본 문서는 시스템 내 모든 Aggregate의 구성 요소 및 참조 규칙의 단일 진실 출처이다.

Rules
1. Direct Reference Restriction: Aggregate 간 직접 객체 참조는 엄격히 금지하며, 오직 AggregateId (Value Object)만을 통해 참조한다.
2. Single Transaction Boundary: 1개의 DB 트랜잭션 내에서는 오직 1개의 Aggregate만 수정(Save/Update)할 수 있다. 타 Aggregate의 변경은 Domain Event를 통한 비동기 결과적 일관성(Eventual Consistency)으로 처리한다.
3. Aggregate Size Limit: Aggregate 내 Entity 개수는 최대 5개를 초과할 수 없다. 커다란 Aggregate는 성능 저하 및 Lock 경쟁을 유발하므로 즉시 분리한다.

Aggregate Specification Table


Aggregate
Aggregate Root
Owns (Entities & VOs)
Reference Only (By ID)

UserAggregate
User
UserProfile (Entity), UserPreference (VO)
CompanionId, GoalId

WorkoutAggregate
WorkoutRecord
ExerciseSet (Entity), CalorieBurn (VO)
UserId, QuestId

MealAggregate
MealRecord
FoodItem (Entity), NutrientBreakdown (VO)
UserId

CompanionAggregate
HealthCompanion
CompanionEmotion (VO), CompanionStat (VO)
UserId

QuestAggregate
Quest
QuestCondition (VO), RewardItem (VO)
UserId

HabitAggregate
Habit
HabitLog (Entity), StreakInfo (VO)
UserId



Runtime Impact
• 데이터베이스 락(Lock) 범위가 단일 Aggregate로 제한되어 Concurrent Write 성능이 극대화된다.

Examples
java
// Correct: Reference by ID
public class WorkoutRecord extends AggregateRoot<WorkoutId> {
    private UserId userId; // ID만 참조
    private List<ExerciseSet> exerciseSets; // 내부에 포함된 Entity
}

// Incorrect: Direct Object Reference (FORBIDDEN)
public class WorkoutRecord extends AggregateRoot<WorkoutId> {
    private User user; // 금지!
}


Forbidden
• ​2개 이상의 Aggregate Root를 하나의 트랜잭션 안에서 동시에 저장/수정하는 행위 금지.
• ​Aggregate 간 순환 참조(Circular Dependency) 생성 금지.
​Related Documents
• ​03_BACKEND/TRANSACTION_POLICY.md
• ​03_BACKEND/DDD/DOMAIN_EVENT_CATALOG.md
​Change History
• ​v1.0.0 (2026-07-31): Initial DDD Aggregate Boundary declaration.