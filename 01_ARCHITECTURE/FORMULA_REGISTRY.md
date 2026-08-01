FORMULA_REGISTRY

Purpose
본 문서는 프로젝트 내 모든 건강, 게임, 보상, 시스템 연산 공식의 중앙 등록소(SSOT)이다. 본 문서는 공식의 등록 및 메타데이터 관리만 수행하며, 세부 수식은 각 Owner 문서에서 관리한다.

Formula Registry Table


Formula ID
Formula Name
Ver
Input Variables
Output Value
Owner Document
Used By System
Related Event ID

F-001
Overall Health Score
1.0.0
Diet, Exercise, Sleep, GrowthRate
 ()
05_AI/HEALTH_SCORE_ENGINE.md
AI, Dashboard, Report
EVT_HEALTH_SCORE_UPDATED

F-002
Dynamic Emotion Value
1.0.0
BaseVal, ActionDelta, Streak, TimeDelta
 ()
05_AI/EMOTION_ENGINE.md
AI EmotionEngine
EVT_AI_EMOTION_CHANGED

F-003
EXP Reward Calculation
1.1.0
ActionType, Difficulty, StreakMult

03_GAME_SYSTEM/EXP_RULE.md
QuestEngine, Reward
EVT_USER_LOG_RECORDED

F-004
Memory Recall Score
1.0.0
EmotionalWeight, TimeDelta, RecallCount

05_AI/MEMORY_ENGINE.md
AI MemoryEngine
EVT_AI_PROMPT_GENERATED

F-005
Micro Spark Probability
1.0.0
StreakDays, UserLuckFactor
 ()
03_GAME_SYSTEM/MICRO_REWARD_SYSTEM.md
RenderEngine
EVT_MICRO_REWARD_TRIGGERED



Rules
1. 새로운 수식을 코드에 구현하기 전에 반드시 FORMULA_REGISTRY에 ID를 선할당받아야 한다.
2. Formula ID는 중복될 수 없으며, 단종 시 Deprecated 처리 후 신규 ID를 발행한다.

Related Documents
• 01_ARCHITECTURE/FORMULA_VERSION_POLICY.md