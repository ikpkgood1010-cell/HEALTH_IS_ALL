CQRS_USAGE_GUIDE

Purpose
본 문서는 명령(Command: CUD)과 조회(Query: Read)의 책임 및 데이터 모델을 분리하는 CQRS(Command Query Responsibility Segregation) 패턴의 적용 기준과 오용 방지 가이드라인을 정의하는 SSOT이다.

Scope
시스템 내 모든 API 요청 처리 파이프라인 및 DB 조회/명령 모델 설계에 적용된다.

SSOT
CQRS 적용 영역과 비적용 영역을 구분하는 판단 기준의 단일 진실 출처이다.

Rules
1. Applicable Areas: 
◦ 메인 대시보드(Dashboard) 종합 정보 조회
◦ 월간/주간 건강 통계(Statistics) 및 추이 리포트
◦ 복합 히스토리(History) 검색 및 타임라인
◦ AI 엔진 분석용 빅데이터 집계(Analytics)
2. Non-Applicable Areas: 
◦ 단일 엔티티 대상의 단순 CRUD (예: 사용자 프로필 수정, 습관 명칭 변경)
◦ 트랜잭션 즉시성(Strong Consistency)이 필수적인 작업
3. Model Separation: 
◦ Command Side: Aggregate 중심, 도메인 무결성 검증, Write DB 사용.
◦ Query Side: DTO 중심, Read-Optimized View/Projection, Read DB/Cache 사용.

Runtime Impact
• 읽기 요청 과부하가 쓰기 트랜잭션 성능에 영향을 주지 않으며, 복잡한 대시보드 조회 속도가 획기적으로 향상된다.

Forbidden
• 단순 단건 조회 기능에 불필요하게 Read Model과 비동기 프로젝션 파이프라인을 구축하는 CQRS 남용 행위 금지.

Related Documents
• 03_BACKEND/DDD/READ_MODEL_POLICY.md
• 03_BACKEND/TRANSACTION_POLICY.md

Change History
• v1.0.0 (2026-07-31): CQRS Usage Guide initial release.