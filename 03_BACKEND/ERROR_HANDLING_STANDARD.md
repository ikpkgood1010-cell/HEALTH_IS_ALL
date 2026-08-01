ERROR_HANDLING_STANDARD

Purpose
본 문서는 Frontend, Backend, AI Engine 시스템 전반에서 발생하는 모든 에러 응답 구조와 에러 코드를 통일하고 사용자에게 안전한 메시지를 전달하기 위한 SSOT이다.

Scope
앱 전체 예외 처리기(Global Exception Handler), API 에러 응답 및 클라이언트 에러 핸들러에 적용된다.

SSOT
프로젝트 표준 에러 코드 체계 및 사용자/개발자 메시지 분리 규칙의 단일 진실 출처이다.

Standard Error Code Schema
• Format: ERR_[DOMAIN]_[TYPE]_[CODE]
• Domains: USER, WORKOUT, MEAL, COMPANION, QUEST, AI, SYS
• Types: NOT_FOUND, INVALID_INPUT, UNAUTHORIZED, CONFLICT, INTERNAL

Standard JSON Error Response Payload
json
{
  "errorCode": "ERR_WORKOUT_INVALID_INPUT_4001",
  "userMessage": "운동 기록 형식이 올바르지 않습니다. 입력값을 확인해 주세요.",
  "developerMessage": "Duration minutes must be greater than zero. Received: -5",
  "timestamp": "2026-07-31T04:19:22Z",
  "traceId": "trc_8839102938"
}


Rules
1. Zero Stack Trace Exposure: 클라이언트(유저) 응답으로 시스템 Stack Trace나 DB 에러 전문을 절대로 노출하지 않는다. 상세 스택 트레이스는 오직 서버 측 JSON 로그에만 저장한다.
2. User-Friendly Message: userMessage는 개발자 용어가 아닌 유저가 즉시 조치할 수 있는 친절한 문구로 작성한다.
3. Global Mapping: HTTP Status Code는 에러 타입과 1:1 매핑한다 (400 Bad Request, 401 Unauthorized, 404 Not Found, 409 Conflict, 500 Internal Error).

Runtime Impact
• 시스템 내부 스키마 및 보안 취약점 노출을 완벽 차단하며 클라이언트 에러 복구 로직이 단순화된다.

Forbidden
• 클라이언트 화면에 NullPointerException이나 SQLSyntaxErrorException 등 개발자용 원문 에러 코드를 직접 출력하는 행위 엄금.

Related Documents
• 03_BACKEND/LOGGING_AND_OBSERVABILITY.md

Change History
• v1.0.0 (2026-07-31): Unified Error Handling Standard established.