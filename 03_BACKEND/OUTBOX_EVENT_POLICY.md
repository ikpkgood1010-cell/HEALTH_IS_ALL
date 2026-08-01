OUTBOX_EVENT_POLICY

Purpose
본 문서는 분산 트랜잭션 환경에서 비즈니스 데이터 업데이트와 도메인 이벤트 발행 간의 원자성(Atomicity)을 보장하기 위한 Transactional Outbox Pattern의 표준을 규정한다.

Scope
백엔드 데이터베이스 Outbox 테이블, Event Relayer, Dead Letter Queue(DLQ) 및 이벤트 메시징 시스템에 적용된다.

SSOT
Outbox 패턴 구현, 재시도, Dead Letter 및 이벤트 순서 보장 정책의 단일 진실 출처이다.

Rules
1. Outbox Dual Write: 메인 비즈니스 데이터 저장 시, 동일한 DB 트랜잭션 안에서 OUTBOX_EVENT 테이블에 이벤트를 PENDING 상태로 함께 저장한다.
2. Relayer Polling & CDC: Outbox Relayer는 주기에 따라 PENDING 이벤트를 순서대로 조회하여 Message Broker로 발행 후 PUBLISHED 상태로 변경한다.
3. Retry & Backoff Formula: 이벤트 발행 실패 시 Exponential Backoff 수식을 적용하여 최대 5회 재시도한다:

1. 
2. Dead Letter Queue (DLQ) : 5회 재시도 실패 시 해당 이벤트는 DEAD_LETTER 상태로 전환되고 DLQ 테이블에 격리되며, 운영 알림(Alert)을 발생시킨다.
3. Retention & Cleanup: PUBLISHED 완료된 이벤트는 7일 보관 후 크론잡(Cron Job)에 의해 자동 삭제(Cleanup)된다.

Outbox Table Schema Structure
• event_id (UUID, PK)
• aggregate_type (VARCHAR)
• aggregate_id (VARCHAR)
• payload (JSONB)
• status (PENDING, PUBLISHED, DEAD_LETTER)
• retry_count (INT)
• created_at (TIMESTAMP)

Runtime Impact
• 네트워크 장애나 MQ 다운 시에도 도메인 이벤트 유실이 0%로 보장된다.

Forbidden
• Outbox 테이블을 거치지 않고 직접 In-Memory Event Bus로 이벤트를 발행하여 DB 저장과 이벤트 발행 트랜잭션을 분리하는 행위 금지.

Related Documents
• 03_BACKEND/TRANSACTION_POLICY.md
• 03_BACKEND/DDD/DOMAIN_EVENT_CATALOG.md

Change History
• v1.0.0 (2026-07-31): Outbox Event Policy established.