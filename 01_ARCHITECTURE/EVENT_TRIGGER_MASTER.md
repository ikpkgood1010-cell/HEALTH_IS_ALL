EVENT_TRIGGER_MASTER

Purpose
본 문서는 프로젝트 내에서 발생하는 모든 이벤트(Domain, UI, AI, Runtime, Schedule, User, System)의 명명 규칙, 조건, 처리 결과 및 재시도/취소 정책을 관리하는 단일 진실 출처(SSOT)이다.

Event Naming Convention
• EVT_[DOMAIN]_[ACTION]_[STATUS/TARGET]
◦ 예: EVT_USER_EXERCISE_COMPLETED, EVT_AI_EMOTION_CHANGED

Event Trigger Master Table


Event ID
Domain
Trigger Source
Condition
Result
Consumer
Retry Policy
Cancel Condition

EVT_USER_LOG_RECORDED
User
UI User Action
필수 데이터 입력 완료
건강 데이터 저장 및 점수 계산 이벤트 발행
HealthScoreEngine, HabitTracker
Max 3 (Exponential Backoff)
화면 이탈 시 입력 취소

EVT_HEALTH_SCORE_UPDATED
AI
HealthScoreEngine
점수 계산 완료
UI Dashboard 갱신 및 AI 감정 업데이트
RenderEngine, EmotionEngine
Immediate Retry 1
이전 계산값과 동일 시 캔슬

EVT_AI_EMOTION_CHANGED
AI
EmotionEngine
감정 수치 임계점 도달
3D 모델 애니메이션 & 대사 변경
UI View, AudioEngine
None (Event Sourcing)
새로운 감정 우선 발생 시

EVT_DAILY_RESET_TRIGGERED
Schedule
Local Scheduler
Local Time 00:00:00
일일 퀘스트, 리셋 처리, 리포트 생성
QuestEngine, MemoryEngine
Max 5
디바이스 시간 조작 감지 시

EVT_SYNC_OFFLINE_QUEUE
Backend
SyncManager
Network Online 감지
로컬 큐 데이터 서버 전송 및 충돌 해결
SyncEngine, Database
Unlimited (Periodic)
네트워크 재오프라인 전환 시



Rules
1. 모든 이벤트 수신자는 Idempotency(단등성)을 보장해야 하며, 동일 이벤트 중복 수신 시 1회만 처리한다.
2. 이벤트 페이로드(Payload)는 전송 효율성을 위해 가급적 엔티티의 ID와 변경된 델타 수치만 포함한다.

Related Documents
• 01_ARCHITECTURE/EVENT_DEPENDENCY_MATRIX.md
• 01_ARCHITECTURE/RUNTIME_STATE_MATRIX.md