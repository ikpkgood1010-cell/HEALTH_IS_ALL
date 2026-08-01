# [중복문서-덮어쓰기, 교체] Dynamic Nutrition UI Experience Specification

## Purpose
엄격한 식단 관리(무설탕, 무밀가루, 무튀김, 찜 요리 선호 등)를 수행하는 사용자가 번거로움 없이 직관적이고 즐겁게 기록할 수 있는 UI/UX를 제공합니다.

## Scope
- 영양/식단 트래킹 화면, 인터랙티브 위젯, 칭찬 및 피드백 팝업 디자인

## SSOT
- 프론트엔드 영양 및 식단 UI 인터페이스 규격의 SSOT.

## Definitions
- **Quick Toggle Chip**: 설탕, 밀가루, 튀김 제외 여부를 원터치로 기록할 수 있는 인터페이스 구성 요소.
- **Interactive Feedback Pop-up**: 기록 완료 시 정령이 반응하는 감성적 피드백 화면.

## Runtime
- Flutter 모바일 앱 환경에서 구동되며, 60fps 이상의 부드러운 애니메이션 보장.

## Rules
1. 모바일 환경에서 복사 및 입력이 편리하도록 UI 요소 배치를 최적화합니다.
2. 이용자 친화적이고 따뜻한 문구를 사용하여 건강 관리의 부담감을 낮춥니다.

## State
- 로컬 상태 관리를 통해 네트워크 지연 없이 즉각적인 UI 피드백 제공.

## Event
- `UI_EVENT_DIET_LOGGED`: 식단 기록 저장 시 발생.

## Example
- 사용자가 '찜 포크 넥 + 양파' 식단 입력 및 무설탕/무밀가루 체크 시 정령의 환호 애니메이션 출력.

## Exception
- 입력 누락 항목 발생 시 부드러운 안내 메시지 노출 (강제성 배제).

## Related Documents
- `HEALTH IS ALL/04_FRONTEND/DYNAMIC_NUTRITION_UI_SPEC.md`

## Change History
- v3.0 (2026-07-31): 모바일 친화적 원터치 토글 및 감성 피드백 스펙 추가