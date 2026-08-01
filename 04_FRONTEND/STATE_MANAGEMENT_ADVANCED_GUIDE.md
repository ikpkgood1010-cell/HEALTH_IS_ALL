# [중복문서-덮어쓰기, 교체] State Management Advanced Guide

## Purpose
Flutter 프레임워크 기반에서 RPG 게임 요소(정령 애니메이션, 실시간 효과)와 건강 트래킹 데이터(칼로리, 식단)가 충돌 없이 매끄럽게 연동되도록 상태 관리 아키텍처를 안내합니다.

## Scope
- Provider / Bloc 패턴 활용 규칙, 메모리 최적화, 렌더링 성능 유지

## SSOT
- 프론트엔드 상태 관리 및 데이터 흐름의 SSOT.

## Definitions
- **Reactive Health Provider**: 건강 상태 변화에 따라 UI 위젯이 즉각 반응하도록 설계된 상태 관리 모듈.

## Runtime
- 클라이언트 앱 실행 중 상시 가동.

## Rules
1. 불필요한 위젯 리빌드를 방지하여 모바일 배터리 소모를 최소화합니다.
2. 게임 애니메이션 성능이 건강 데이터 로깅 기능에 지장을 주지 않도록 스레드를 분리합니다.

## State
- 글로벌 상태와 로컬 위젯 상태의 명확한 분리.

## Event
- `STATE_EVENT_REFRESH`: 화면 포커스 시 데이터 갱신.

## Example
- 식단 기록 완료 즉시 정령 위젯의 경험치바가 부드럽게 차오르는 애니메이션 실행.

## Exception
- 상태 동기화 실패 시 로컬 캐시 데이터를 바인딩하고 콘솔에 무소음 로깅.

## Related Documents
- `HEALTH IS ALL/04_FRONTEND/FLUTTER_PROJECT_STRUCTURE.md`

## Change History
- v3.0 (2026-07-31): 게임성과 건강 UI 분리 및 성능 최적화 가이드 작성