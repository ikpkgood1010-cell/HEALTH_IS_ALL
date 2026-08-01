ENGAGEMENT_DESIGN

Purpose
본 문서는 손해에 대한 공포(FOMO)가 아닌, 성취와 정서적 애착을 바탕으로 플레이어가 1년 이상 자발적으로 앱을 이용하도록 유도하는 장기 유지 전략을 정의한다.

Scope
• Daily, Weekly, Monthly, Season, Anniversary 주기별 설계
• 휴면 유저 복귀(Comeback) 보호막 및 친구 공유 없이도 유지되는 독립적 장기 구조

SSOT
본 문서는 플레이어의 장기 리텐션 및 휴면 케어 정책의 단일 진실 출처(SSOT)이다.

Rules
1. 주기별 리텐션 설계: 
◦ Daily: 가벼운 체크인과 건강이와의 소소한 인사를 통한 일상화.
◦ Weekly: 주간 리포트를 통한 발전 확인 및 챌린지 성과급.
◦ Monthly: 새로운 시즌 테마 도감 오픈 및 월간 칭호 지급.
◦ Anniversary: 앱 사용 100일, 1년 차에 전달되는 건강이의 감사 손편지 및 기념 3D 오브젝트.

1. FOMO(놓치면 손해) 없는 디자인 및 복귀(Comeback) 보호: 
◦ 몇 달 만에 접속하더라도 건강이가 죽거나 레벨이 깎여있지 않다.
◦ 오랜만에 돌아온 유저에게는 "어디 갔었어!"라는 질책 대신 "다시 와줘서 너무 고마워! 보고 싶었어." 라는 복귀 환영 패키지(Streak Protection 1회권 + Point 선물)를 제공한다.

1. 소셜 강제 배제: 
◦ 친구 초대를 강요하거나 SNS 공유를 해야만 보상을 주는 시스템을 배제하며, 오직 나와 건강이 단 둘만의 깊은 관계 형성에 집중한다.

Runtime
• 미접속 기간이 7일 이상인 유저가 접속하면 EngagementEngine이 EVT_USER_COMEBACK을 발생시켜 복귀 전용 이벤트 팝업과 따뜻한 대사를 출력한다.

Examples
• 30일 동안 접속하지 않은 유저가 앱을 열면, 건강이가 반갑게 뛰어나오며 "그동안 잘 지냈어? 다시 만나서 정말 기뻐!"라고 맞아줌.

Forbidden
• 장기 미접속 시 캐릭터 수치 차감, 아이템 삭제 등 불이익 부여.
• 친구 초대 수에 따라 핵심 보상을 차등 지급하는 소셜 강제성 디자인.

Related Documents
• 03_GAME_SYSTEM/PLAYER_RETENTION.md
• 05_AI/COMPANION_PERSONALITY.md

Change History
• 2026-07-31: PATCH-002 최초 작성 (Gemini)