# DYNAMIC NUTRITION UI SPECIFICATION V3

## Purpose
본 문서는 사용자가 복잡한 영양 성분 수치를 한눈에 직관적으로 이해하면서, 스피릿과의 상호작용을 통해 식단 기록의 재미를 느낄 수 있도록 프론트엔드 UI/UX 인터페이스를 명시한다.

## Scope
- 마크로 영양소(탄/단/지) 및 클린 성분(식이섬유, 당 제한) Visual Gauge 컴포넌트
- 스피릿 인터랙티브 상호작용 애니메이션 영역 배치
- 모바일 가독성을 위한 자동 줄바꿈 및 터치 친화적 버튼 레이아웃

## SSOT (Single Source of Truth)
- 본 문서는 dynamic nutrition 화면 레이아웃 및 UX 디자인 표준의 유일한 SSOT이다.

## Definitions
- **Macro Gauge Bar**: 탄수화물, 단백질, 지방 비율을 색상별로 직관적으로 보여주는 커스텀 게이지.
- **Spirit Food Reaction View**: 식단 입력 시 스피릿이 음식을 먹는 반응 애니메이션 레이어.

## Runtime
- Flutter 프론트엔드 `dynamic_nutrition_tracker_widget.dart` 제어.

## Rules
1. **화면 분할 밸런스**: 상단 40%는 스피릿 반응 및 게임 요소, 하단 60%는 직관적 건강/영양 수치를 배치하여 주객전도를 방지한다.
2. **모바일 최적화**: 모든 텍스트 및 버튼 요소는 자동 줄바꿈(`softWrap: true`)을 적용하여 글자가 잘리지 않도록 구현한다.

## State
- `NutritionUIState`: `LOADING` | `DISPLAY_MACROS` | `SPIRIT_ANIMATING` | `ERROR_SNACKBAR`

## Event
- `ON_MEAL_SUBMITTED`: 식단 입력 후 스피릿 반응 효과음 및 리워드 애니메이션 재생.

## Example
- **영양 상태 가이드**:
  - 단백질 충족 시: 녹색 게이지 활성화 + 스피릿 머리 위에 '근력 UP' 아이콘 표시.

## Exception
- 통신 지연 시 영양 수치를 로컬 캐시에서 먼저 읽어와 UI cut-off 없이 즉시 표시.

## Related Documents
- `HEALTH IS ALL/04_FRONTEND/UI_SCREEN_SPECIFICATION_V3.mdux`
- `HEALTH IS ALL/lib/dynamic_nutrition_tracker_widget.dart`

## Change History
- v3.0.0 (2026-07-31): 스피릿 반응 영역 및 모바일 가독성 향상 최적화 UI 명세 추가.