COLLECTION_SYSTEM

Purpose
본 문서는 건강이 코스튬, 방 꾸미기 요소, 칭호, 배지 등 수집 콘텐츠의 획득 및 도감 관리를 정의하는 단일 진실 출처(SSOT)이다.

Scope
• 의상, 배경, 액세서리, 포즈, 칭호의 희귀도(Rarity) 및 순수 건강 행동 기반 수급 경로
• 절대 Pay-to-Win 배제 원칙

SSOT
본 문서는 프로젝트 내 모든 수집 아이템 도감 및 획득 로직의 단일 진실 출처(SSOT)이다.

Rules
1. 아이템 희귀도 구조: 
◦ Common (일반) : 일일 Quest 및 Point 상점 기본 구매.
◦ Rare (희귀) : 주간 Goal 달성 및 특정 연속 습관 달성 보상.
◦ Epic (영웅) : 월간 시즌 패스 순수 완주 및 업적(Achievement) 해금.
◦ Legendary (전설) : 1년 연속 건강 관리 등 장기 헌신 보상.

1. 절대 과금 금지 원칙 (No Pay-to-Win / No Gacha): 
◦ 모든 희귀도(Legendary 포함) 아이템은 오직 사용자의 실질적 건강 행동 및 성취로만 해금할 수 있다.
◦ 유료 결제로 도감 수집률을 직접 올리는 시스템은 엄격히 금지한다.

1. 도감(Archive) 혜택: 
◦ 도감 수집률은 과시용 칭호 및 외형 변경 혜택만 제공하며, Exp 획득량을 늘려주는 등의 스탯적 이득을 주지 않는다.

Runtime
• 업적 달성 시 CollectionManager.unlockItem(itemId)가 호출되어 유저 인벤토리에 아이템이 영구 추가된다.

Examples
• 100일간 매일 수면 목표를 달성한 유저는 '수면의 마법사' 전설 코스튬과 칭호를 획득함.

Forbidden
• 확률형 뽑기(Gacha)를 통해서만 획득 가능한 수집 아이템 배치.
• 유료 재화로 수집 아이템을 직접 즉시 구매하게 만드는 구조.

Related Documents
• 03_GAME_SYSTEM/ECONOMY_MASTER.md
• 03_GAME_SYSTEM/POINT_RULE.md

Change History
• 2026-07-31: PATCH-002 최초 작성 (Gemini)