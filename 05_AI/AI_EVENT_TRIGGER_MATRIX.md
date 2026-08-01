AI_EVENT_TRIGGER_MATRIX

Purpose
본 문서는 사용자의 건강 행동 이벤트 발생 시 파이프라인(행동  이벤트  감정  연출  대사  보상  기억) 전체의 매핑 관계를 명시한다.

Scope
• 식단, 운동, 수면, 습관, 출석, 목표 달성 시 발생하는 파이프라인 매핑 표

SSOT
본 문서는 이벤트 트리거 시 일어나는 시스템 간 연동의 단일 진실 출처(SSOT)이다.

Rules
1. 종합 이벤트 파이프라인 매핑 표:


사용자 행동
Trigger Event
감정 전이
애니메이션 연출
대표 대사 톤
보상 (Exp/Point)
기억 저장 (Memory)

영양 식단 등록
EVT_MEAL_QUALIFIED
Joy
박수 치며 미소
식단 영양소 칭찬
Exp +30, Point +10
식단 선호도 업데이트

고강도 운동 완료
EVT_EXERCISE_HEAVY
Energetic
펀치 & 조깅
한계 돌파 응원
Exp +50, Point +15
운동 종류 및 강도 저장

7시간 수면 달성
EVT_SLEEP_GOOD
Calm
개운하게 기지개
상쾌한 아침 인사
Exp +40, Point +10
수면 패턴 기록

습관 7일 연속
EVT_HABIT_STREAK_7
Proud
트로피 들기 연출
끈기 인정 및 감동
Exp +100, Point +50
장기 기억(Streak) 등록

48시간 기록 없음
EVT_NO_RECORD_48H
Concern
고개 갸우뚱 안부
따뜻한 안부 물음
보상 없음
공백 기간 기록



Runtime
• EventDispatcher가 클라이언트 이벤트를 수신하면 위 매핑 표에 정의된 개별 모듈(EmotionEngine, RenderEngine, RewardEngine, MemoryEngine)을 병렬 호출 처리한다.

Examples
• EVT_HABIT_STREAK_7 발생 시: 감정이 Proud로 바뀌고, 트로피 애니메이션이 재생되며, Exp 100 / Point 50이 즉시 지급된다.

Forbidden
• 정의되지 않은 이벤트 타입 사용 또는 파이프라인 중 일부 모듈 호출 누락.

Related Documents
• 05_AI/EMOTION_ENGINE.md
• 03_GAME_SYSTEM/MICRO_REWARD_SYSTEM.md

Change History
• 2026-07-31: PATCH-002 최초 작성 (Gemini)