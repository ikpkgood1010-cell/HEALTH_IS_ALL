READ_MODEL_POLICY

Purpose
본 문서는 CQRS의 Query Side에서 사용하는 Read Model(프로젝션)의 생성, 캐싱, 무효화 및 동기화 정책을 규정하는 SSOT이다.

Scope
백엔드 Read Model, Redis 캐시, Materialized View 및 동기화 프로젝터(Projector) 서비스에 적용된다.

SSOT
Read Model의 라이프사이클 및 캐시 무효화 규칙의 단일 진실 출처이다.

Rules
1. Event-Driven Projection: Read Model은 Domain Event를 구독(Subscribe)하는 Async Projector에 의해 비동기로 갱신된다.
2. Cache Invalidation & TTL: 
◦ 대시보드 요약 Read Model: TTL 1시간 + 관련 도메인 이벤트 수신 시 즉시 Invalidation/Refresh.
◦ 통계 Read Model: Daily Reset 시점에 일괄 계산 후 캐싱.
3. Version & Schema Evolution: Read Model DTO 변경 시 v1, v2 버저닝을 적용하여 이전 앱 버전과의 호환성을 유지한다.

Read Model Refresh Formula
캐시 적중률 최적화를 위한 갱신 지연 계산:

Runtime Impact
• DB Read Load를 80% 이상 절감하며 UI 응답 속도를 50ms 이내로 보장한다.

Forbidden
• Read Model 프로젝션 과정에서 오류가 발생했을 때 Command 쓰기 트랜잭션을 롤백시키는 행위 금지 (결과적 일관성 준수).

Related Documents
• 03_BACKEND/DDD/CQRS_USAGE_GUIDE.md
• 03_BACKEND/OUTBOX_EVENT_POLICY.md

Change History
• v1.0.0 (2026-07-31): Read Model Policy established.