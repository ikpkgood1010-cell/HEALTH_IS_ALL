MICRO_REWARD_SYSTEM

Purpose
본 문서는 정성적 보상 외에 시각, 음향, 미세한 상호작용을 통해 플레이어에게 즉각적인 즐거움을 제공하는 미세 보상(Micro-Reward) 시스템을 정의한다.

Scope
• Animation, Confetti, Sound Effect, Tiny Gift, Sticker, Combo Spark 연출 체계

SSOT
본 문서는 인게임 피드백 연출 및 미세 보상 규칙의 단일 진실 출처(SSOT)이다.

Rules
1. 미세 보상 연출 구성 요소를 정 정밀하게 매핑: 
◦ Confetti Effect: 퀘스트 완료 시 화면 상단에서 터지는 다채로운 종이 가루 연출.
◦ Combo Spark: 연속 3일 이상 습관 달성 시 화면 중앙 터치 위치에 일어나는 불꽃 파티클.
◦ Sound Feedback: 햅틱 진동(Haptic Vibration)과 연동된 경쾌한 3음계 획득 음향.
◦ Tiny Gift Box: 5회 행동 시 마다 등장하는 무작위 가구 스티커 / 프로필 배경 조각.

1. 스파크 발생 확률 수식 (Dynamic Spark Probability):

◦ 연속 달성일수가 늘어날수록 화려한 스파크 이펙트가 출현할 확률이 상승한다.

1. 연출 속도 및 템포: 
◦ 미세 보상 연출은 

◦ 초 이내에 완료되어 사용자의 다음 인터랙션을 방해하지 않아야 한다 (Skip 터치 지원).

Runtime
• MicroRewardEngine.trigger(effect_type) 호출 시 시각 이펙트와 로컬 Audio/Haptic API가 동기화되어 가동된다.

Examples
• 사용자가 물 마시기를 터치하면 0.3초간 경쾌한 물방울 소리와 함께 건강이 머리 위에 작은 하트 스파크가 튀어 오름.

Forbidden
• 미세 보상 연출이 3초 이상 지속되어 사용자의 화면 이동을 강제로 막는 현상.

Related Documents
• 03_GAME_SYSTEM/GAMEPLAY_LOOP_MASTER.md
• 05_AI/AI_EVENT_TRIGGER_MATRIX.md

Change History
• 2026-07-31: PATCH-002 최초 작성 (Gemini)