APPLICATION_SERVICE_GUIDE

Purpose
본 문서는 Application Service 레이어의 역할 및 책임 경계를 명확히 규정하여 비즈니스 로직의 오염을 방지하고 유스케이스 조율(Orchestration) 기능을 정립하는 SSOT이다.

Scope
백엔드의 모든 Application Service 및 Command/Query Handler 구현에 적용된다.

SSOT
Application Service의 구현 범위 및 금지 사항의 단일 진실 출처이다.

Rules
1. Orchestration Only: Application Service는 오직 ① Repository에서 Aggregate 로드, ② Aggregate의 도메인 메서드 호출, ③ Aggregate 변경 사항 저장, ④ Outbox Event 발행 등록 조율만을 담당한다.
2. No Domain Logic: if 문이나 수식을 통한 상태 변경 계산 로직(예: 경험치 계산, 건강 점수 산출 등)을 Application Service에 직접 작성하는 것을 금지한다. 해당 로직은 반드시 Aggregate 또는 Domain Service에 존재해야 한다.
3. Transaction Demarcation: DB 트랜잭션의 시작과 종료 경계(@Transactional)는 Application Service의 유스케이스 메서드 단위로 지정한다.

Runtime Impact
• 도메인 로직이 도메인 모델 내부로 격리되어 유닛 테스트 작성이 용이해지고, 코드 재사용성이 극대화된다.

Examples
java
// Correct: Application Service Orchestration
@Service
@Transactional
public class CompleteHabitApplicationService {
    private final HabitRepository habitRepository;
    private final OutboxEventPublisher eventPublisher;

    public void completeHabit(CompleteHabitCommand cmd) {
        Habit habit = habitRepository.findById(cmd.getHabitId());
        DomainEvent event = habit.complete(cmd.getTimestamp()); // 비즈니스 로직은 Aggregate가 수행
        habitRepository.save(habit);
        eventPublisher.publish(event); // Outbox 이벤트 저장
    }
}


Forbidden
• Application Service 내부에서 SQL Query를 직접 작성하거나 DB 스키마 객체(DAO/Entity)를 직접 조작하는 행위 금지.
• 외부 AI API 서비스 통신을 Application Service의 @Transactional 메서드 내부에서 동기 실행하는 행위 금지.

Related Documents
• 03_BACKEND/DDD/AGGREGATE_BOUNDARY.md
• 03_BACKEND/TRANSACTION_POLICY.md

Change History
• v1.0.0 (2026-07-31): Initial Application Service Guide.