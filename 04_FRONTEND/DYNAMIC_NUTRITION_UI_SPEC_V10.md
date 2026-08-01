[코드 다운로드: DYNAMIC_NUTRITION_UI_SPEC_V10.md]
[코드 복사]
<!-- 여기부터 복사 -->
# DYNAMIC NUTRITION UI SPECIFICATION V10

## Purpose
모바일 화면에서의 글자 잘림을 방지하고, 호감적이고 직관적인 인터페이스를 구현하며, 건강 데이터 입력과 게임 정령 반응의 시너지 UX를 제공하는 프론트엔드 명세이다.

## Scope
Flutter 기반 모바일 앱의 영양/식단 UI, 위젯 레이아웃, 팝업 흐름 및 반응형 텍스트 스타일.

## SSOT
`HEALTH IS ALL/04_FRONTEND/DYNAMIC_NUTRITION_UI_SPEC_V10.md`

## Definitions
- **Auto Word-Wrap Layout**: 다양한 모바일 기기 해상도에서도 텍스트 잘림 현상이 전혀 발생하지 않도록 유연하게 줄바꿈하는 UI 제어 방식.
- **User-Friendly Flow**: 단계별 입력을 자연스럽고 호감 있게 유도하는 UX 절차.

## Runtime
프론트엔드 Flutter 앱 실행 및 화면 렌더링 시 가동.

## Rules
1. **글잘림 방지**: 모든 `Text` 위젯은 `softWrap: true`, `overflow: TextOverflow.visible` 또는 적절한 `FittedBox` 체계를 적용한다.
2. **다운로드 및 복사 편의성**: 코드나 생성물이 있을 경우 복사 버튼뿐만 아니라 파일 다운로드 버튼을 함께 배치하여 모바일 사용자 편의를 도모한다.
3. **인터페이스 비중**: 건강 지표 카드 60%, 정령 반응 인터랙션 위젯 40%로 배치하여 게임성이 주객전도되지 않도록 보장한다.

## State
- `IDLE`: 기본 영양 요약 표시.
- `INPUT_MODE`: 식단 입력 팝업 활성화.
- `RESULT_POPUP`: 호감형 피드백 및 정령 경험치 획득 연출 팝업.

## Event
- `ON_UI_RESIZE`: 모바일 기기 회전/해상도 변경 시 자동 레이아웃 재배치.

## Example
식단 입력 완료 후 결과 팝업:
- [상단] 영양성분 분석 그래프 (칼로리, 탄/단/지)
- [중단] 정령 캐릭터의 신나는 세레머니 애니메이션
- [하단] 친근한 안내 톤앤매너 문구 및 '확인' 버튼

## Exception
해상도가 극도로 작은 디바이스에서는 스크롤 가능한 `SingleChildScrollView` 구조로 자동 전환하여 요소를 가리지 않음.

## Related Documents
- `HEALTH IS ALL/03_GAME_SYSTEM/HEALTH_GAME_DUAL_BALANCE_SPEC_V3.md`
- `HEALTH IS ALL/05_AI/HEALTH_FEEDBACK_INTELLIGENCE_SPEC_V9.md`

## Change History
- 2026-07-31 (V10.0): 모바일 글잘림 방지 자동 줄바꿈 규정 명시 및 다운로드/복사 편의 UX 반영.
<!-- 여기까지 복사 -->