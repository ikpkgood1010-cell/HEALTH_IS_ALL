# \# EVENT\_SEPARATION\_SPEC.md

# 

# \## Purpose

# 도메인 핵심 로직을 담당하는 Domain Event와 사용자 행동 패턴 및 비즈니스 지표를 측정하는 Analytics Event를 명확히 분리하여 결합도를 낮추고 데이터 신뢰성을 확보한다.

# 

# \## Scope

# \* 백엔드 DDD Domain Event Publisher

# \* 프론트엔드 및 백엔드 Analytics Telemetry Collection Engine

# 

# \## SSOT

# \* \*\*SSOT Document\*\*: `HEALTH IS ALL/06\_ANALYTICS/EVENT\_SEPARATION\_SPEC.md`

# \* \*\*Authority\*\*: Data Analytics \& Backend Architecture Team

# 

# \## Definitions

# \* \*\*Domain Event\*\*: 도메인 상태 변경을 의미하며 트랜잭션 일관성 보장 및 시스템 내 비즈니스 유스케이스 이행에 필수적인 이벤트.

# \* \*\*Analytics Event\*\*: 사용자 UX 분석, A/B 테스트, 퍼널 분석을 위해 비동기로 전달되는 지표 수집용 이벤트.

# 

# \## Runtime

# \* \*\*Domain Event Pipeline\*\*: In-Memory Event Bus / Outbox Pattern

# \* \*\*Analytics Pipeline\*\*: Asynchronous HTTP Collector / Mixpanel / BigQuery Data Pipeline

# 

# \## Rules

# 1\. \*\*명칭 규칙 분리\*\*: Domain Event는 과거분사형(예: `QuestCompletedEvent`), Analytics Event는 `snake\_case`(예: `click\_quest\_complete\_button`)를 사용한다.

# 2\. \*\*독립성 보장\*\*: Analytics Event 수집 실패가 DB 트랜잭션에 영향을 미치지 않아야 한다.

# 3\. \*\*식별자 분리\*\*: Analytics Event에는 PII를 직접 포함할 수 없으며 난수화된 `analytics\_id`만 사용한다.

# 

# \## State

# \* `DOM\_EMITTED`: 도메인 이벤트 발생 및 Outbox 저장 완료

# \* `ANA\_DISPATCHED`: 분석 이벤트 비동기 전송 완료

# 

# \## Related Documents

# \* `HEALTH IS ALL/03\_BACKEND/DDD/DOMAIN\_EVENT\_CATALOG.md`

# 

# \## Change History

# \* \*\*v1.0.0 (2026-07-31)\*\*: PATCH-005 최초 작성.

