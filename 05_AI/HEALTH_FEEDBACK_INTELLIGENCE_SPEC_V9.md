[코드 다운로드: HEALTH_FEEDBACK_INTELLIGENCE_SPEC_V9.md]
[코드 복사]
<!-- 여기부터 복사 -->
# HEALTH FEEDBACK INTELLIGENCE SPECIFICATION V9

## Purpose
사용자에게 친근하고 호감도를 주는 대화 톤앤매너로 건강 피드백 및 안내 팝업을 제공하여, 앱에 대한 긍정적 애착과 건강 관리 동기를 지속적으로 유발한다.

## Scope
AI 가이던스, 정령 메시지, 건강 대화 인터페이스, 다이얼로그 팝업 및 사용자 맞춤 팁 발송 시스템.

## SSOT
`HEALTH IS ALL/05_AI/HEALTH_FEEDBACK_INTELLIGENCE_SPEC_V9.md`

## Definitions
- **Empathetic Dialogue Engine**: 단조롭거나 지시적인 말투를 지양하고 호감적이고 공감적인 표현을 생성하는 AI 모듈.
- **Micro-Feedback**: 사용자의 조그만 수치 개선에도 즉각적으로 호응하는 미세 피드백.

## Runtime
사용자 인터랙션 발생 시 프론트엔드 다이얼로그 매니저 및 백엔드 AI 피드백 엔진에서 실시간 가동.

## Rules
1. **톤앤매너**: 따뜻함, 응원, 전문성의 조화 (예: "오늘 단백질 섭취량이 목표에 아주 가까워졌어요! 정말 잘하고 계십니다 😊").
2. **비난 및 강요 금지**: 목표 미달 시 자책감을 주지 않고 대안을 친절히 제안함.
3. **인터페이스 호환성**: 모바일 화면에서 문구가 잘리지 않도록 3줄 이내의 간결하고 효과적인 문장 구조 유지 (Auto Word-Wrap 적용).

## State
- `GREETING`: 사용자 진입 시 반가운 인사.
- `PRAISE`: 건강 목표 달성 시 축하 피드백.
- `ENCOURAGE`: 미달 시 친절한 격려 및 대안 제시.

## Event
- `ON_MEAL_LOGGED`: 식단 기록 시 호감형 피드백 생성.
- `ON_ACHIEVEMENT_UNLOCKED`: 업적 달성 팝업 트리거.

## Example
사용자가 찜 요리로 건강한 식단을 입력했을 때:
> "와, 기름기를 쏙 뺀 담백한 찜 요리라니! 몸도 마음도 가벼워지는 최고의 선택이에요. 정령도 기분이 좋아 보여요 🌿"

## Exception
네트워크 지연 시 로컬 프롬프트 라이브러리에서 호감형 기본 템플릿 문구를 즉시 렌더링.

## Related Documents
- `HEALTH IS ALL/05_AI/HEALTH_TIPS_TRICKS_FEEDER_V2.md`
- `HEALTH IS ALL/03_GAME_SYSTEM/HEALTH_GAME_DUAL_BALANCE_SPEC_V3.md`

## Change History
- 2026-07-31 (V9.0): 호감형 문구 가이드라인 강화 및 모바일 자동 줄바꿈 대응 규정 수립.
<!-- 여기까지 복사 -->