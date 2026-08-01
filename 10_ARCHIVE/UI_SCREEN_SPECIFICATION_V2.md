# UI_SCREEN_SPECIFICATION_V2

## Purpose
모바일 화면에서 텍스트 잘림 현상을 방지하고, 자동 줄바꿈과 복사 버튼 최적화를 통해 사용자 경험을 극대화하기 위한 프론트엔드 UI 화면 마스터 사양을 정의합니다.

## Scope
- Flutter 전체 UI 화면 및 위젯 (`lib/widgets/`, `lib/*_screen.dart`)

## SSOT
- UI 레이아웃, 줄바꿈 규칙 및 컴포넌트 디자인의 단일 진실 공급원(SSOT)

## Definitions
- **Flexible Wrap**: 화면 크기 변화에 대응하여 텍스트가 자연스럽게 줄바꿈되도록 하는 UI 규칙
- **Mobile Action Bar**: 모바일 환경에서 복사 및 다운로드 기능을 터치 한 번에 수행할 수 있는 하단 고정 바

## Runtime
- 앱 빌드 및 화면 렌더링 시 실시간 적용

## Rules
1. 모든 텍스트 컴포넌트는 `softWrap: true` 및 적절한 `TextOverflow`를 적용하여 글자가 잘리지 않도록 합니다.
2. 모바일 사용자의 편의를 위해 복사 버튼을 명확하게 배치하고 성공 시 토스트 팝업을 띄웁니다.
3. 건강과 게임 요소가 시각적으로 조화롭게 배치되도록 대시보드 인터페이스를 정돈합니다.

## State
- `ui_layout_mode`: responsive
- `autowrap_enabled`: true

## Event
- `EVENT_UI_RESIZED`: 화면 회전 또는 기기 변경 시 레이아웃 재조정

## Example
- 긴 식단 가이드 문구가 화면 너비를 넘어갈 경우 자동으로 2줄로 분할되어 표시됨

## Exception
- 고정 픽셀 오버플로 발생 시 SingleChildScrollView로 자동 감싸서 에러 방지

## Related Documents
- `04_FRONTEND/CODING_STANDARDS.mdux`
- `lib/app_theme.dart`

## Change History
- **v2.0 (2026-07-31)**: 자동 줄바꿈 강제 규칙 및 모바일 최적화 복사 인터페이스 도입