ECONOMY_MASTER

Purpose
본 문서는 HEALTH IS ALL 프로젝트의 인게임 경제 시스템, 자원 흐름, 인플레이션 방지 및 밸런스 정책을 정의하는 단일 진실 출처(SSOT)이다.

Scope
• Exp(성장치)와 Point(꾸미기 재화)의 철저한 역할 분리 및 수급/소진 구조
• 일간, 주간, 월간, 시즌 단위 경제 흐름 및 프리미엄(유료) 요소의 영향 범위
• 상점(Shop), 퀘스트(Quest), 업적(Achievement) 시스템과의 연계 규칙

SSOT
본 문서는 게임 경제 규칙 및 자원 구조에 대해 프로젝트 내 최상위 권한을 가진다.

Definitions
• Exp: 건강이와 플레이어의 레벨을 올려주는 성장 지수. 절대 거래나 구매에 사용할 수 없는 '비화폐성 성취 지수'.
• Point: 상점 이용, 코스튬 구매, 메인 화면 꾸미기 등에 사용되는 인게임 화폐. 절대 스탯 성장이나 레벨업에 직접 관여할 수 없음.

Rules
1. 자원 분리의 원칙: 
◦ Exp = 성장 및 스토리 해금 전용 (수급 경로: 순수 건강 행동)
◦ Point = 외형 꾸미기 및 수집 전용 (수급 경로: 건강 행동, 퀘스트, 시즌 패스)
2. Exp Source & Sink: 
◦ Source: 식단 기록, 운동 완료, 정시 수면, 습관 달성, 주간 퀘스트.
◦ Sink: 레벨업 요구량 상승 (누적 구조), 신규 스토리/배지 해금.
3. Point Source & Sink: 
◦ Source: 일일 미션 달성, 연속 출석, 업적 달성, 이벤트.
◦ Sink: 건강이 코스튬, 방 꾸미기 가구, 프로필 테마, 칭호 구매.
4. 인플레이션 방지 정책: 
◦ Daily Cap / Soft Cap을 도입하여 무제한 획득을 차단한다.
◦ 리워드 감쇄(Diminishing Returns): 하루 일정 횟수 이상의 기록부터는 획득량이 단계적으로 감소한다.
5. 프리미엄(Pay-to-Win) 방지: 
◦ 유료 결제는 오직 편의성 기능(데이터 분석 리포트) 및 한정판 코스튬 구매에만 적용하며, Exp 획득 속도를 직접적으로 상승시킬 수 없다.

Runtime
• 자원 변경 요청 발생 시 EconomyManager가 호출되며, DailyCapCheck() 및 AntiAbuseCheck()를 거쳐 DB 트랜잭션으로 안전하게 단일 처리된다.

Examples
• 플레이어가 Point가 모자란다고 해서 Exp를 Point로 환전할 수 없으며, 돈을 내고 Exp를 직접 구매할 수 없다.

Forbidden
• Exp를 상점 재화로 사용하는 시스템 구현.
• Point로 건강이 레벨을 직접 상승시키는 기능.
• 결제를 통한 직접적 건강 레벨 구매 (Pay-to-Win).

Related Documents
• 03_GAME_SYSTEM/GAMEPLAY_LOOP_MASTER.md
• 03_GAME_SYSTEM/EXP_RULE.md
• 03_GAME_SYSTEM/POINT_RULE.md

Change History
• 2026-07-31: PATCH-001 최초 작성 (Gemini)