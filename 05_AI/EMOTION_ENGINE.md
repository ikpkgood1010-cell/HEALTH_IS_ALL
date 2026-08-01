EMOTION_ENGINE

Purpose
본 문서는 건강이의 감정 상태(Emotion State), 감정 전이(Transition), 감정 감쇄 및 시각/음성 표현 매핑 규칙을 정의하는 단일 진실 출처(SSOT)이다.

Scope
• 5대 기본 감정 축 및 정밀 감정 지수 계산식
• 사용자 건강 행동에 따른 감정 전이 우선순위 및 감쇄(Decay) 수식
• 감정에 따른 3D/2D 애니메이션, 표정(Face Expression), 보이스 톤(Voice Tone) 매핑

SSOT
본 문서는 AI 건강이의 감정 연산 및 표현 제어에 대해 프로젝트 내 최상위 권한을 가진다.

Definitions
• Emotion Vector: 건강이의 감정을 결정하는 5개 축 .
• Primary Emotion: Emotion Vector 중 가장 높은 값을 가지며 현재 UI에 표현되는 대표 감정.

Rules
1. 감정 결정의 원칙: 
◦ 감정은 무작위(Random)로 바뀌지 않으며, 반드시 사용자의 검증된 건강 행동(식단/운동/수면/습관) 및 미입력 기간에 비례하여 변화한다.

1. 감정 상태 지수 산출 공식:
◦ : 시각 에서의 감정 의 수치 ()
◦ : 건강 행동 완료에 따른 감정 증가 수치
◦ : 연속 달성 보정 계수 ()
◦ : 감정별 자연 감쇄율 (Joy: , Concern: )
◦ : 마지막 건강 행동 수행 후 경과 시간 (단위: 시간)

1. 감정 전이 및 우선순위 (Emotion Priority): 
◦ Priority 1: Concern (건강 위험/48시간 미기록 시 - 단, 비난 없이 걱정으로 표현)
◦ Priority 2: Proud (주간 Goal 달성 또는 어려운 운동 완료)
◦ Priority 3: Energetic (운동 직후)
◦ Priority 4: Joy (정상 식단/수면 기록 완료)
◦ Priority 5: Calm (기본 상태 및 수면 전 시간대)

1. 시각/음성 매핑 표:


대표 감정
애니메이션 매핑
표정(BlendShape)
보이스 톤
대사 어조

Joy
점프 및 손흔들기
눈웃음, 입꼬리 상승
밝고 경쾌함
반가움, 칭찬

Proud
가슴 펴고 자부심 포즈
눈 반짝임, 미소
당당하고 힘참
함께 이룬 성과 강조

Concern
손을 턱에 대고 고개 갸우뚱
걱정스러운 눈썹
부드럽고 차분함
안부 확인, 가벼운 제안

Energetic
펀치 시늉 및 가벼운 조깅
활기찬 눈빛
템포가 빠르고 밝음
에너지 넘치는 격려

Calm
호흡하며 편안히 서기
평온한 표정
나긋나긋함
편안한 일상 대화



Runtime
• 건강 행동 등록 이벤트 수신 시 EmotionEngine.update()가 호출되어 Vector 수치를 계산한 후, 가장 높은 우선순위의 대표 감정을 StateEngine으로 전달하여 UI를 갱신한다.

Examples
• 사용자가 3일 연속 운동을 완료하고  상태일 때 운동을 등록하면:
• 
건강이는 Energetic 상태로 전이되어 조깅 애니메이션과 활기찬 보이스를 출력한다.

Forbidden
• 사용자가 기록을 하지 않았다고 해서 짜증(Angry)이나 혐오(Disgust) 상태로 전이되는 규칙 지정 금지.
• 외부 입력 없이 감정 수치가 완전히 임의로 변동하는 로직 구현 금지.

Related Documents
• 03_GAME_SYSTEM/GAMEPLAY_LOOP_MASTER.md
• 05_AI/COMPANION_PERSONALITY.md
• 05_AI/AI_EVENT_TRIGGER_MATRIX.md

Change History
• 2026-07-31: PATCH-002 최초 작성 및 동적 감정 수식 반영 (Gemini)