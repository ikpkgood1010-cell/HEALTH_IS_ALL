# PERFORMANCE_BUDGET_SPEC.md

## Purpose
Flutter 앱 및 백엔드 서비스의 성능 목표 수치, 프레임 레이트, 메모리 점유율 상한선을 규정한다.

## Rules
1. **UI 프레임 예산**: 프레임 드랍률(Jank) 1% 미만 유지.
2. **클라이언트 메모리 상한**: Peak Game Screen 기준 250MB 이하.
3. **API Latency**: Read p95 < 100ms, Write p99 < 300ms.

## Change History
* **v1.0.0 (2026-07-31)**: PATCH-005 최초 작성.