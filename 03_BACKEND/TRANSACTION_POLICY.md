TRANSACTION_POLICY

Purpose
본 문서는 데이터베이스 트랜잭션의 시작, 범위, 격리 수준(Isolation Level) 및 외부 API 통신 시의 트랜잭션 분리 원칙을 정의하는 SSOT이다.

Scope
백엔드 모든 서비스 메서드 및 데이터베이스 커넥션 관리에 적용된다.

SSOT
트랜잭션 경계 설정 및 시스템별 트랜잭션 포함 여부의 단일 진실 출처이다.

Rules & Transaction Boundary Matrix


System Action
DB Transaction Inclusion
Isolation Level
Max Execution Time
Execution Policy

운동 기록 저장
INCLUDED
READ_COMMITTED

Aggregate 저장 + Outbox 저장 단일 DB Tx

식단 기록 저장
INCLUDED
READ_COMMITTED

Aggregate 저장 + Outbox 저장 단일 DB Tx

Goal / Habit 완료
INCLUDED
READ_COMMITTED

Habit 상태 변경 + Outbox 저장

Exp / Reward 지급
EXCLUDED (Async)
READ_COMMITTED

Outbox 이벤트를 수신한 독립 Tx에서 처리

Quest 완료 처리
EXCLUDED (Async)
READ_COMMITTED

Outbox 이벤트를 수신한 독립 Tx에서 처리

Notification 발송
EXCLUDED (Async)
N/A
N/A
Non-blocking Async I/O (No DB Tx)

AI 연산 및 분석
STRICTLY EXCLUDED
N/A
N/A
DB Tx 밖에서 실행 (외부 HTTP 호출)



CRITICAL RULE: AI Call Separation
• LLM/Vision AI 연산 및 external API 호출은 절대로 @Transactional 블록 내부에서 실행되어서는 안 된다.
• 외부 통신 지연 시 DB Connection Pool 고갈 및 Deadlock을 초과 유발하므로, '선 AI 연산 완료 \rightarrow 후 단기 DB 트랜잭션 저장' 패턴을 강제한다.

Runtime Impact
• DB 커넥션 점유 시간이 극단적으로 줄어들어 스파이크 트래픽 발생 시에도 시스템 붕괴를 완벽히 차단한다.

Forbidden
• External HTTP Call / AI Prompt Request를 데이터베이스 트랜잭션 안에서 동기 호출하는 행위 엄금.

Related Documents
• 03_BACKEND/DDD/APPLICATION_SERVICE_GUIDE.md
• 03_BACKEND/OUTBOX_EVENT_POLICY.md

Change History
• v1.0.0 (2026-07-31): Transaction Policy defined with strict AI Call separation rule.