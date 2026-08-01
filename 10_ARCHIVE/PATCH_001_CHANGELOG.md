PATCH_001_CHANGELOG

Purpose
본 문서는 PATCH-001 (Gameplay Core & Economy Foundation)의 수행 결과, 신규 생성 문서, 기존 문서 수정 내역 및 파급 효과를 기록한다.

Scope
• PATCH-001 실행 범위 내 모든 문서 변경 및 참조 전환 내역

SSOT
본 문서는 PATCH-001 변경 역사에 대한 단일 진실 출처(SSOT)이다.

Created Documents (신규 생성 문서 10종)
1. 03_GAME_SYSTEM/GAMEPLAY_LOOP_MASTER.md
2. 03_GAME_SYSTEM/ECONOMY_MASTER.md
3. 03_GAME_SYSTEM/EXP_RULE.md
4. 03_GAME_SYSTEM/POINT_RULE.md
5. 03_GAME_SYSTEM/ANTI_GRIND_POLICY.md
6. 03_GAME_SYSTEM/PLAYER_RETENTION.md
7. 00_PROJECT/CANONICAL_NAMING.md
8. 00_PROJECT/DOCUMENT_DEPENDENCY_MATRIX.md
9. START_HERE.md
10. 00_PROJECT/PATCH_HISTORY/PATCH_001_CHANGELOG.md

Deprecation & Reference Transition (기존 문서 수정 방침)
• 기존 문서 (GAME_SYSTEM.md, QUEST_SYSTEM.md, REWARD_SYSTEM.md, SHOP_SYSTEM.md, HEALTH_AI.md, GOAL_SYSTEM.md, HABIT_SYSTEM.md) 내의 중복 게임 루프 및 경제 정의는 삭제 대상이며, 각 상단에 아래 참조 링크를 명시하도록 전환한다: 
◦ See 03_GAME_SYSTEM/GAMEPLAY_LOOP_MASTER.md
◦ See 03_GAME_SYSTEM/ECONOMY_MASTER.md

Breaking Changes & Terminology Clean
• XP 단어를 전면 제거하고 Exp로 일원화함.
• Spirit, Pet 단어를 전면 제거하고 건강이로 일원화함.
• Gold, Coin 단어를 전면 제거하고 Point로 일원화함.

Related Documents
• START_HERE.md
• 00_PROJECT/DOCUMENT_DEPENDENCY_MATRIX.md

Change History
• 2026-07-31: PATCH-001 완료 기록 작성 (Gemini)