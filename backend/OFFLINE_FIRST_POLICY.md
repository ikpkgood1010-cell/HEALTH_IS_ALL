OFFLINE_FIRST_POLICY

Purpose
본 문서는 인터넷 연결이 불안정하거나 끊긴 오프라인 환경에서도 앱의 핵심 기능(특히 운동 기록 및 게임 인터랙션)이 100% 정상 작동하도록 보장하는 전략을 정의한다.

Key Rules
1. 100% Offline Exercise Guarantee: 운동 기록, 식단 작성, 건강이와의 기본 대화는 오프라인 상태에서 네트워크 요청 없이 로컬 DB(SQLite/Hive)에 즉시 완료 기록되어야 한다.
2. Local Queue Strategy: 오프라인 중 발생한 이벤트는 Local Sync Queue에 FIFO 순서로 저장된 후, 네트워크 재연결 시 SyncManager에 의해 오프라인 큐 동기화가 진행된다.
3. UI Instant Responsiveness: 사용자는 오프라인 상태임을 인지하지 못할 정도로 빠른 딜레이 없이 UI 피드백과 보상 연출을 받아야 한다.

Related Documents
• 03_BACKEND/SYNC_CONFLICT_POLICY.md
• 01_ARCHITECTURE/RUNTIME_STATE_MATRIX.md