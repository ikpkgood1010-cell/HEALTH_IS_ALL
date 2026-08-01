# DYNAMIC_NUTRITION_UI_SPEC_V4.md

## Purpose
건강 영양 정보의 직관적 전달을 최우선으로 삼으며, 게임 요소(정령)가 조화롭게 보조하는 V4 UI/UX 레이아웃 명세입니다.

## Scope
* Flutter 영양 대시보드 화면, 정령 위젯 팝업, 다변수 그래픽 가이던스.

## SSOT
* `HEALTH IS ALL/04_FRONTEND/DYNAMIC_NUTRITION_UI_SPEC_V4.md`

## Definitions
* **Primary Health HUD**: 칼로리, 탄/단/지 비율, 수분 섭취량을 최상단에 배치하는 메인 레이아웃.
* **Spirit Companion Overlay**: 영양 달성률에 따라 반응하는 하단 비침습적 정령 상호작용 영역.

## Runtime
* Flutter Mobile Application (Android/iOS)

## Rules
1. 건강 지표(칼로리/영양소)는 어떠한 경우에도 정령 애니메이션에 의해 가려지거나 왜곡되어서는 안 된다.
2. 모든 수치 변경 시 0.3초 애니메이션 트랜지션을 적용하여 자연스러운 시각 효과를 제공한다.
3. 텍스트 자동 줄바꿈(`TextOverflow.fade` 또는 `softWrap: true`)을 적용하여 글자 짤림을 차단한다.

## State
* `LOADING`, `DISPLAY_HEALTH_DATA`, `SHOW_SPIRIT_REACTION`

## Event
* `ON_MEAL_LOGGED`, `ON_UI_REFRESH`

## Example
* 단백질 목표 100% 달성 시 -> 최상단 단백질 바 완료 표시 후, 하단 정령 팝업창에서 "정령이 단백질 파워를 얻었습니다!" 칭찬 문구 노출.

## Exception
* 화면 해상도가 작을 경우 정령 위젯을 축소 아이콘 모드로 자동 전환.

## Related Documents
* `HEALTH IS ALL/04_FRONTEND/UI_SCREEN_SPECIFICATION_V3.md`

## Change History
* **V3.0**: 기본 대시보드 명세.
* **V4.0 (2026-07-31)**: 건강 정보 우위 보장 가이드라인 명시, 모바일 글 잘림 방지 자동 줄바꿈 규칙 추가.