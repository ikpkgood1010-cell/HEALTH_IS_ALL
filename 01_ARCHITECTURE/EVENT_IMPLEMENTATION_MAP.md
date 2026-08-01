# EVENT_IMPLEMENTATION_MAP

- Version: 1.0
- Status: Active
- Last Updated: 2026-08-01
- Purpose: Event SSOT와 실제 구현 경로를 연결한다.

| Event ID | Producer | Consumer | Actual Code Path | Implemented | Notes |
|---|---|---|---|---|---|
| `EVT_USER_LOG_RECORDED` | User action / API | Progression, Health score, habit tracking | `backend/main.py` POST `/api/v1/health/record` | Partial | 저장/보상은 동작하나 명시적 event object 발행 없음 |
| `EVT_HEALTH_SCORE_UPDATED` | Health engine | Dashboard, Emotion engine | `backend/health_calculator.py` + `backend/ai_agent_service.py` 간접 | Partial | 상태 갱신은 계산 결과 반환 방식, 이벤트 계층 없음 |
| `EVT_AI_EMOTION_CHANGED` | AI feedback layer | UI / audio | `backend/ai_agent_service.py`, `lib/widgets/health_i_widget.dart` | Partial | 감정 문자열은 전달되지만 이벤트 버스 미구현 |
| `EVT_DAILY_RESET_TRIGGERED` | Scheduler | Quest, memory, reset | 문서만 확인, 활성 스케줄러 미확인 | No | 런타임 구현 부족 |
| `EVT_SYNC_OFFLINE_QUEUE` | Sync manager | Backend DB / conflict resolver | `backend/offline_sync_engine.py` 후보 | Partial | 엔진 파일 존재, 연결 경로 미검증 |
| `EVT_DOM_HABIT_COMPLETED` | Habit aggregate | Quest, companion | 도메인 카탈로그 문서만 확인 | No | Aggregate/event 구현체 미확인 |
| `EVT_DOM_WORKOUT_RECORDED` | Workout aggregate | Exp, Health score | `backend/main.py` + `backend/progression_engine.py` 간접 | Partial | 개념상 연결되나 명시적 도메인 이벤트 없음 |
| `EVT_DOM_MEAL_ANALYZED` | Meal aggregate | Health score, Quest | `backend/diet_calculator.py` 간접 | Partial | API/스토리지와의 명시적 이벤트 연결 없음 |
| `EVT_DOM_GOAL_COMPLETED` | Quest aggregate | Economy, Notification | 활성 경로 미확인 | No | 문서만 존재 |
| `EVT_DOM_COMPANION_LEVEL_UP` | Companion aggregate | UI, audio | `backend/main.py` level 계산, UI 표현 | Partial | 이벤트 object 없음, 계산만 존재 |

## Summary
- 이벤트는 대부분 "문서상 정의 + 함수 호출 기반 간접 연결" 상태다.
- PATCH-005 기준으로 explicit event bus / outbox / consumer registry는 미완성이다.
- 운영 전에는 최소한 `event_id`, `producer`, `occurred_at`, `payload` 구조를 갖는 공통 이벤트 모델이 필요하다.
