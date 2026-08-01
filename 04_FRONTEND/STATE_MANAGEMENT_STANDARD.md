# STATE_MANAGEMENT_STANDARD

- Document Name: STATE_MANAGEMENT_STANDARD.md
- Version: 1.0
- Status: Active
- Owner: PATCH-004 Implementation Governance
- Last Updated: 2026-08-01
- Purpose: Flutter 상태관리를 한 기준으로 묶고 Provider/Riverpod 혼재를 통제한다.
- Implementation Status: Implemented
- Source of Truth: Documentation + Code
- Verification:
  - Last Verified Date: 2026-08-01
  - Verified By: PATCH-004 governance pass
  - Test Reference: `lib/main.dart`, `lib/meal_exercise_logger_screen.dart`, `lib/settings_profile_screen.dart`

## Current State Summary
- 현재 런타임에는 `provider`와 `flutter_riverpod`가 혼재한다.
- 신규 표준은 Riverpod로 통일한다.
- 기존 Provider 코드는 즉시 전면 삭제하지 않고 migration 대상으로 관리한다.

## Standard Rule
1. 신규 화면/기능은 Riverpod를 사용한다.
2. 기존 Provider 기반 코드는 유지 가능하나 확장 개발 시 Riverpod로 옮긴다.
3. 하나의 화면에서 Provider와 Riverpod를 혼합하지 않는다.

## ReadModel
1. 서버/로컬 저장소에서 읽는 데이터는 ReadModel로 분리한다.
2. ReadModel은 UI 포맷팅 책임을 가지지 않는다.
3. 목록/상세/대시보드 ReadModel을 분리한다.

## ViewModel
1. 화면 상태 조합, 사용자 액션, validation, refresh orchestration을 담당한다.
2. ViewModel은 repository/service를 호출하지만 위젯 트리를 직접 알지 않는다.
3. Riverpod의 `Notifier`/`AsyncNotifier`를 표준으로 사용한다.

## State
1. 상태는 `idle`, `loading`, `data`, `error`, `refreshing`, `offline_pending`를 구분한다.
2. state는 immutable을 기본으로 한다.
3. 사용자 입력 임시 상태와 서버 동기 상태를 분리한다.

## Cache
1. 읽기 캐시는 화면별이 아니라 도메인별로 관리한다.
2. 캐시 TTL 또는 무효화 조건을 명시한다.
3. stale data 허용 시 UI에 refresh 상태를 표시한다.

## Refresh
1. refresh는 수동/자동을 구분한다.
2. mutation 후 관련 provider를 invalidate한다.
3. 연쇄 invalidation 범위를 문서화한다.

## Offline
1. 오프라인 입력은 로컬에 먼저 저장하고 즉시 UI에 반영한다.
2. 동기화 대기 상태를 숨기지 않는다.
3. 충돌 시 최신값/서버값/병합값 정책을 도메인별로 정한다.

## Retry
1. 네트워크/동기화 실패는 재시도 전략을 가진다.
2. 자동 재시도 횟수와 사용자 수동 재시도를 분리한다.
3. 재시도 중복으로 보상 중복 지급이 생기지 않아야 한다.

## Loading
1. 첫 로딩과 백그라운드 리프레시는 다른 UX를 사용한다.
2. skeleton/shimmer 사용 여부를 화면별로 정한다.
3. loading 중 이전 데이터를 유지할 수 있으면 유지한다.

## Error
1. 사용자 메시지와 디버깅 메시지를 구분한다.
2. provider 내부 stack trace를 그대로 노출하지 않는다.
3. 재시도 가능 여부를 state에 포함한다.

## Provider/Riverpod Migration Rule
1. `lib/main.dart`의 전역 `provider` 사용은 레거시로 표기한다.
2. `mock_data_provider.dart`, `offline_sync_manager.dart`는 migration 후보로 관리한다.
3. `meal_exercise_logger_screen.dart`, `habit_routine_screen.dart`, `settings_profile_screen.dart` 패턴을 신규 표준 참고점으로 삼되, 장기적으로는 codegen 기반 Riverpod 표준으로 정리한다.

## Naming Rule
- provider/controller 파일: `snake_case`
- state class: `PascalCase + State`
- view model/controller: `PascalCase + Controller/Notifier`

## Related Source Files
- `lib/main.dart`
- `lib/mock_data_provider.dart`
- `lib/meal_exercise_logger_screen.dart`
- `lib/habit_routine_screen.dart`
- `lib/settings_profile_screen.dart`
- `04_FRONTEND/STATE_MANAGEMENT_GUIDE.md`

## Validation Method
- Widget Test
- State Unit Test
- Manual Runtime Verification
- Migration Review
