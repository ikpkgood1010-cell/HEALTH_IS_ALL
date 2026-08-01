# DYNAMIC_NUTRITION_UI_SPEC_V9.md

## Purpose
본 문서는 프론트엔드 모바일 UI/UX 상의 식단 및 건강 영양 디스플레이 스펙을 정의합니다. 글자 잘림 없는 자동 줄바꿈, 호감적인 대화 팝업, 모바일에서의 편리한 복사 및 다운로드 UI 구성을 제공합니다.

## Scope
* 식단 및 영양소 다이얼로그 레이아웃
* 모바일 화면 자동 줄바꿈 (Auto Line-Wrapping) 및 반응형 폰트
* 정령 감정 반응 위젯 및 1~3줄 꿀팁 카드 UI

## SSOT
* **경로**: `HEALTH IS ALL/04_FRONTEND/DYNAMIC_NUTRITION_UI_SPEC_V9.md`
* **소유팀**: Frontend Mobile UX/UI Team

## Definitions
* **Auto-Wrap Container**: 모바일 디바이스 해상도에 맞춰 텍스트가 잘리지 않고 부드럽게 개행되는 가변 박스.
* **Micro-Tip Card**: 홈 화면 및 다이얼로그 하단에 1~3줄로 가볍게 노출되는 카드 형태의 위젯.

## Runtime
* **실행 환경**: Flutter 3.x Mobile Client (Android / iOS)

## Rules
1. 모든 텍스트 카드 및 팝업창은 `SoftWrap: true` 및 `TextOverflow.visible` 속성을 기본 적용한다.
2. 건강 지표는 직관적인 그래프로 표현하고, 정령 캐릭터 위젯은 터치 시 호감 문구를 출력한다.
3. 복사 및 다운로드가 필요한 정보는 명확한 버튼 형태의 UI로 제공한다.

## State
* `DISPLAY_SUMMARY`: 요약 정보 보기 상태
* `DISPLAY_DETAIL`: 세부 영양소 연산 결과 보기 상태
* `POPUP_ACTIVE`: AI 정령 꿀팁 팝업 활성화 상태

## Event
* `ON_TIP_CARD_TAP`: 팁 카드 클릭 시 세부 설명 및 추가 팁 롤링
* `ON_COPY_BTN_CLICK`: 정보 텍스트 클립보드 복사 실행

## Example
* 사용자가 식단 기록 완료 팝업을 열면, 스팀 요리 및 대체당 사용 보너스가 계산되어 정령의 모션과 함께 부드럽게 개행된 3줄 꿀팁 카드가 깔끔하게 표시됨.

## Exception
* 화면 해상도가 360dp 이하인 소형 디바이스: 폰트 크기를 단계별로 자동 축소(Auto-Sizing)하여 가독성 유지.

## Related Documents
* `HEALTH IS ALL/05_AI/HEALTH_FEEDBACK_INTELLIGENCE_SPEC_V8.md`
* `HEALTH IS ALL/04_FRONTEND/UI_SCREEN_SPECIFICATION_V3.mdux`

## Change History
* **v9.0.0 (2026-07-31)**: V8 대비 자동 줄바꿈 표준 적용, 모바일 원클릭 복사/다운로드 UI 스펙 반영.