DISCOVERY_SYSTEM

Purpose
본 문서는 반복적인 앱 사용 속에서 플레이어가 예기치 못한 재미를 느끼도록 만드는 발견(Discovery) 및 숨겨진 요소 시스템을 정의한다.

Scope
• Hidden Dialogue, Rare Reaction, Secret Touch Interaction, Health Lore 발굴 규칙

SSOT
본 문서는 숨겨진 상호작용 및 발견 시스템에 대한 단일 진실 출처(SSOT)이다.

Rules
1. Discovery 콘텐츠 분류: 
◦ Secret Touch: 건강이의 특정 부위(예: 발바닥, 머리 뿔)를 연속 3회 터치 시 나오는 전용 희귀 동작.
◦ Time-based Hidden Dialogue: 새벽 5시 접속 시, 혹은 비 오는 날 접속 시에만 출력되는 특별 대사.
◦ Health Lore Card: 특정 건강 습관(예: 20일간 상추 섭취) 달성 시 해금되는 건강이의 비하인드 스토리 카드.

1. 희귀 반응 출현 수식 (Rare Reaction Chance):

◦  (

◦  기본 확률)

◦ : 당일 건강 점수에 따라 

◦  보정.

Runtime
• 사용자 입력 발생 시 DiscoveryEngine.checkTrigger()가 계산하여 조건을 만족할 경우 특별 인터랙션을 우선 반환한다.

Examples
• 비 오는 날 아침 유저가 앱을 열면 건강이가 우산을 쓰고 나타나 "오늘 비 오는데 창밖 구경해 봤어?"라는 특별 대사를 출력함.

Forbidden
• 발견 요소의 해금 조건을 유료 결제나 외부 공유로만 제한하는 행위.

Related Documents
• 03_GAME_SYSTEM/COLLECTION_SYSTEM.md
• 05_AI/COMPANION_PERSONALITY.md

Change History
• 2026-07-31: PATCH-002 최초 작성 (Gemini)