# DYNAMIC NUTRITION UI SPEC

## Purpose
모바일 환경에서 사용자가 식단(클린 식단, 찜 요리 등)과 영양 상태를 직관적이고 아름답게 확인할 수 있도록 자동 줄바꿈, 명확한 복사 버튼, 깔끔한 레이아웃을 제공하는 UI 스펙입니다.

## Scope
- Flutter 기반 영양/식단 트래커 화면 컴포넌트
- 반응형 레이아웃 및 폰트 자동 줄바꿈 규칙

## SSOT
- `HEALTH IS ALL/04_FRONTEND/DYNAMIC_NUTRITION_UI_SPEC.md`

## Definitions
- **반응형 줄바꿈 (Auto-Wrap):** 화면 크기에 관계없이 텍스트와 수치가 잘리지 않도록 처리하는 스타일 규칙.

## Runtime
- 식단 화면 진입 및 데이터 갱신 시 실시간 렌더링.

## Rules
1. 모바일 환경에서 불편함이 없도록 모든 주요 수치 카드에 원터치 복사 기능과 명확한 시각적 버튼을 제공합니다.
2. 글자가 잘리지 않도록 `Expanded` 및 `Wrap` 위젯을 적극 활용합니다.

## State
- `ui_theme`: Clean & Modern
- `text_scaling`: Enabled

## Event
- `NUTRITION_UI_RENDERED`
- `COPY_BUTTON_CLICKED`

## Example
- 식단 기록 카드 내 탄단지 비율 및 클린 지수 프로그레스 바 표시.

## Exception
- 화면 해상도 초과 시 스크롤뷰로 자동 전환.

## Related Documents
- `HEALTH IS ALL/04_FRONTEND/UI_SCREEN_SPECIFICATION.md`
- `HEALTH IS ALL/04_FRONTEND/CODING_STANDARDS.md`

## Change History
- v1.0 (2026-01-10): 기본 UI 스펙 작성
- v2.0 (2026-07-31): 모바일 사용성 개선 및 자동 줄바꿈 규격 강화