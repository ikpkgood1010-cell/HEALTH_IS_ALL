MEMORY_ENGINE

Purpose
본 문서는 AI 건강이가 사용자의 건강 데이터, 습관, 대화 이력을 단기/장기 기억으로 저장, 압축, 회상(Recall)하는 기억 엔진 규칙을 정의하는 단일 진실 출처(SSOT)이다.

Scope
• Session, Daily, Weekly, Long-term 4단계 기억 계층 구조
• 감정 가중치 기반 기억 회상 점수 수식 및 만료/압축(Compression) 알고리즘
• 사용자 개인정보 보호(Privacy) 및 기억 삭제 정책

SSOT
본 문서는 건강이의 기억 데이터 구조 및 회상 알고리즘에 대해 최상위 권한을 가진다.

Definitions
• Memory Item: (Timestamp, Category, Context_Vector, Emotional_Weight, Recall_Count)로 구성된 최소 기억 단위.
• Memory Compression: 오래된 세부 데이터들을 주간/월간 단위의 요약 텍스트 및 통계 수치로 압축하여 저장 용량을 최적화하는 과정.

Rules
1. 4단계 기억 계층 구조: 
◦ Session Memory: 현재 앱 실행 중 발생한 대화 및 입력 (앱 종료 시 요약 후 파기).
◦ Daily Memory: 당일 식단, 운동, 수면, 감정 상태 (24시간 유지).
◦ Weekly Memory: 주간 목표 달성률, 주요 습관 이행 여부 (7일 유지 후 압축).
◦ Long-term Memory: 사용자의 특정 취향(예: 샐러드 선호), 장기 성과(예: 3개월간 체중 유지), 기념일.

1. 기억 회상 점수(Recall Score) 수식:

◦ : 기억 형성 시의 감정 강도 (

◦ )

◦ : 기억 감쇄 계수 (

◦ , 

◦ )

◦ : 기억 저장 후 경과 일수

◦ : 해당 기억이 언급/회상된 횟수

1. 기억 압축 규칙: 
◦ 단기 기억 슬롯이 유저당 500개를 초과할 경우, 

◦ 가 가장 낮은 상위 

◦  데이터를 주간 요약("X월 Y주차: 주 4회 운동 완료, 단백질 섭취 양호") 형태로 요약 생성 후 원본 데이터는 소멸시킨다.

1. 개인정보 보호: 
◦ 개인 식별 정보(실명, 민감한 개인 의료 병력)는 기억 엔진에 평문으로 저장하지 않으며, 오직 건강 행동 통계 및 기호(Preference) 데이터만 인코딩하여 저장한다.

Runtime
• AI 대사 생성 시 MemoryEngine.query(current_context)가 호출되어 

•  상위 3개의 기억 아이템을 프롬프트 컨텍스트에 주입한다.

Examples
• 3개월 전 아침 운동을 시작했던 사용자가 오늘 아침 운동을 기록하면:
Long-term Memory에서 "3개월 전 아침 운동 개시" 항목이 높은 

• 로 회상되어 "작년에는 아침 운동이 힘드시다고 했는데, 벌써 3개월째 완벽하게 이어가고 계시네요!"라는 대사를 생성한다.

Forbidden
• 사용자의 삭제 요청이 있는 기억 데이터를 서버 백업에 영구 보존하는 행위.
• 1회성 무의미한 에러 로그나 시스템 메시지를 Long-term Memory에 저장하는 행위.

Related Documents
• 05_AI/EMOTION_ENGINE.md
• 05_AI/COMPANION_PERSONALITY.md
• 05_AI/DIALOGUE_POLICY.md

Change History
• 2026-07-31: PATCH-002 최초 작성 (Gemini)