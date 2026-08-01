DAILY_RESET_POLICY

Purpose
본 문서는 일일 퀘스트, 리셋, 건강 요약 생성 및 기억 저장이 일어나는 매일 초기화 정책을 정의한다.

Local Time Criteria
• 서버의 UTC 시간이 아닌 사용자 디바이스의 Local Time (00:00:00) 을 기준으로 일일 리셋을 실행한다.
• 해외 이동 등으로 타임존 변경 시, 이전 타임존에서의 24시간이 경과하지 않았으면 조기 리셋을 방지하는 보정 로직을 가동한다.

Daily Reset Pipeline Execution Order
1. 00:00:00 Trigger: EVT_DAILY_RESET_TRIGGERED 발생.
2. Habit Streak Assessment: 당일 습관 달성 여부 최종 평가 및 콤보 보정.
3. Memory Summary: 당일의 주요 기록 및 감정 요약본을 MemoryEngine 장기 기억으로 이관.
4. Daily Quest Reset: 새로운 일일 퀘스트 3종 무작위 할당.
5. AI Plan Refresh: 당일의 AI 코칭 플랜 재계산.

Related Documents
• 05_AI/MEMORY_ENGINE.md
• 01_ARCHITECTURE/EVENT_TRIGGER_MASTER.md