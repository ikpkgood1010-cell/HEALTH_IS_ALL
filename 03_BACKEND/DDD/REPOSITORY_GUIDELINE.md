REPOSITORY_GUIDELINE

Purpose
본 문서는 도메인 모델의 영속성(Persistence)을 담당하는 Repository의 인터페이스 및 구현 기준을 정의하여 도메인 레이어의 기술 종속성을 차단하는 SSOT이다.

Scope
모든 Aggregate Root의 Persistence Repository 및 Query Repository 구현체에 적용된다.

SSOT
Repository 인터페이스 설계, 영속성 처리, 조회/명령 저장소 분리 규칙의 단일 진실 출처이다.

Rules
1. Aggregate Root Center: Repository는 오직 Aggregate Root 단위로만 존재한다. (하위 Entity나 VO를 위한 별도 Repository 생성 금지).
2. Interface Separation: 도메인 레이어에는 순수 Java/Dart 인터페이스만 두고, JPA/SQL/Hive 구현체는 Infrastructure 레이어에 배치한다.
3. No Business Logic: Repository 내부에서 비즈니스 조건 검증이나 데이터 가공을 수행할 수 없다.

Standard Methods Specification
• save(AggregateRoot aggregate): Aggregate 전체 상태 영속화.
• findById(AggregateId id): Aggregate Root 단일 조회 (없을 경우 DomainException 발생).
• delete(AggregateRoot aggregate): Aggregate 삭제 또는 Soft Delete 처리.

Runtime Impact
• 데이터 저장소 기술(RDB, NoSQL, In-Memory DB)이 변경되어도 도메인 비즈니스 로직에 영향이 전혀 없다.

Forbidden
• Repository 메서드에 비즈니스 판단 규칙(예: findUsersEligibleForLevelUp())을 복잡한 SQL/JPQL 로직으로 매몰시키는 행위 금지. (Specification 패턴 사용).

Related Documents
• 03_BACKEND/DDD/AGGREGATE_BOUNDARY.md
• 03_BACKEND/DDD/CQRS_USAGE_GUIDE.md

Change History
• v1.0.0 (2026-07-31): Repository Guideline initial release.