RUNTIME_STATE_MATRIX

Purpose
본 문서는 클라이언트 앱 및 시스템의 10대 런타임 상태(State)와 상태 전이(State Transition) 규칙, 타임아웃, 예외 복구 정책을 정의하는 SSOT이다.

10 Major Runtime States
1. Idle: 기본 대기 상태 (메인 화면)
2. Recording: 사용자가 식단/운동/수면 기록 입력 중
3. Processing: AI 계산 및 데이터 내부 연산 중
4. Waiting: 서버 응답 또는 외부 비동기 작업 대기 중
5. Rewarding: 보상 팝업 및 미세 연출 출력 중
6. Completed: 연산/트랜잭션 정상 완료
7. Failed: 연산/네트워크 실패
8. Syncing: 오프라인 큐 동기화 진행 중
9. Offline: 네트워크 미연결 로컬 동작 상태
10. Suspended: 백그라운드 전환 또는 앱 일시정지

State Transition Rules & Matrix
[Idle] ---> [Recording] ---> [Processing] ---> [Rewarding] ---> [Completed] ---> [Idle]
|              |                |                 |
|              v                v                 v
+---------> [Offline] <---> [Syncing] <------> [Failed] ---> [Suspended]
Forbidden Transitions
• Recording

• Rewarding (Processing 및 데이터 검증 없이 즉시 보상 지급 금지)
• Suspended

• Completed (백그라운드에서 직접 완료 처리 금지, 복귀 후 처리)
• Failed

• Rewarding (실패 상태에서 보상 연출 호출 금지)

Timeout & Recovery Policy
• Processing / Waiting 상태 타임아웃: 

• 초 초과 시 자동으로 Offline 또는 Failed 상태로 전환 후 로컬 캐시 데이터 반환.

Related Documents
• 01_ARCHITECTURE/EVENT_TRIGGER_MASTER.md
• 03_BACKEND/OFFLINE_FIRST_POLICY.md