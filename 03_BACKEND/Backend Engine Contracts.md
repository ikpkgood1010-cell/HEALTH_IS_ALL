Backend Engine Contracts (백엔드 엔진 간 통신 규격 및 API 명세)

1. 개요
본 문서는 HEALTH IS ALL 백엔드의 5대 핵심 엔진(Health Engine, Exercise Engine, Spirit Engine, Progression Engine, AI Recommendation Engine) 간 비동기 이벤트 바인딩 규격 및 REST/gRPC API 인터페이스 계약(Contract)을 정의합니다. 본 계약은 서비스의 데이터 일관성과 CQRS 파이프라인의 안정성을 보장하는 절대적 기준입니다.

───

2. 엔진 간 비동기 이벤트 계약 (Event Bus Payloads)

특정 도메인 이벤트 발생 시 Event Bus(Redis Pub/Sub 또는 RabbitMQ)를 통해 타 엔진으로 전파되는 메시지 스키마 규격입니다.

2.1. ExerciseCompletedEvent
• 발행처: Exercise Engine
• 수신처: Progression Engine, Spirit Engine, AI Recommendation Engine

json
{
  "event_id": "evt_ex_1029384",
  "event_type": "ExerciseCompleted",
  "timestamp": "2026-07-30T11:15:00Z",
  "payload": {
    "user_id": "usr_998811",
    "record_id": "rec_773322",
    "exercise_code": "RUNNING_OUTDOOR",
    "duration_minutes": 30,
    "burned_calories": 280,
    "met_value": 8.0
  }
}