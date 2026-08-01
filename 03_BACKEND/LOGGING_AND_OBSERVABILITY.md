LOGGING_AND_OBSERVABILITY

Purpose
본 문서는 운영 환경에서 앱과 백엔드의 상태를 추적하고 장애 발생 시 신속히 원인을 규명하기 위한 구조화된 로깅(Structured Logging) 및 모니터링 표준을 정의한다.

Scope
Frontend(Flutter), Backend(API/Workers), AI Engine 등 시스템 전반의 로그 및 메트릭 수집에 적용된다.

SSOT
로깅 포맷, 로그 레벨, Trace ID 전파 및 PII 마스킹 규칙의 단일 진실 출처이다.

Rules
1. JSON Structured Log: 모든 시스템 로그는 검색 분석이 용이한 JSON 포맷으로 출력한다.
2. Mandatory Header Context: 모든 로그에는 다음 Context Key가 반드시 포함되어야 한다: 
◦ trace_id: 요청 전체 트레이싱 ID (FE 

◦  BE 

◦  AI 전파)
◦ request_id: 단일 HTTP/RPC 요청 ID
◦ user_id: 사용자 식별 ID (비인증 시 anonymous)
◦ event_id: 관련 이벤트 ID
1. Log Levels: 
◦ TRACE: 상세 디버그 (개발 환경 전용)
◦ DEBUG: 주요 변수 및 비즈니스 흐름
◦ INFO: 주요 유스케이스 완료 및 상태 변경
◦ WARN: 시스템 복구 가능한 예외 및 경고
◦ ERROR: 비즈니스 처리 실패, 외부 API 오류
◦ FATAL: 프로세스 중단 및 데이터 파손 위기
2. PII Masking Policy (개인정보 보호) : 
◦ 비밀번호, 인증 토큰: 전체 마스킹 (***)
◦ 사용자 이름/이메일: 앞 2자리 제외 마스킹 (ab***@domain.com)
◦ 민감 식단/생체 메모: 로그 출력 금지 ([REDACTED])

Runtime Impact
• 분산 추적이 가능해져 장애 발생 시 원인 분석 시간이 몇 시간에서 수 분 이내로 단축된다.

Forbidden
• 민감 개인정보(PII)나 인증 키를 일반 평문(Plaintext)으로 로그에 출력하는 행위 엄금.

Related Documents
• 03_BACKEND/ERROR_HANDLING_STANDARD.md

Change History
• v1.0.0 (2026-07-31): Logging and Observability standard defined.