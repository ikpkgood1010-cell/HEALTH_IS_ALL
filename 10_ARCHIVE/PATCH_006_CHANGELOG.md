# PATCH_006_CHANGELOG.md

## Purpose
본 문서는 HEALTH IS ALL 프로젝트의 Patch 006(V6 시스템 확장) 변경 사항을 명확히 기록하고 관리하기 위해 작성되었습니다.

## Scope
* V6 다변수 동적 건강 및 게임 연산 엔진 명세 적용
* 백엔드(Python), 프론트엔드(Dart), 데이터베이스(SQL) 데이터 모델 개편
* dynamic 연산에 대한 자동 폴백(Fallback) 방어 로직 추가

## SSOT
* `HEALTH IS ALL/00_PROJECT/PATCH_HISTORY/PATCH_006_CHANGELOG.md`

## Definitions
* **V6 Dynamic Engine**: 사용자 환경 수치(심박수 변동성, 수면 부채, 일주기 리듬 등)를 반영하여 매회 다른 보상/건강 수치를 계산하는 고도화 엔진.
* **Fallback Safety**: 연산 변수 누락 시 시스템 오류를 방지하기 위해 단일 기본 공식으로 자동 전환하는 메커니즘.

## Runtime
* 적용 시점: Patch 006 배포 즉시 활성화
* 영향 범위: 백엔드 계산 엔진, Flutter 클라이언트 계산기, DB 스키마 v6

## Rules
1. 모든 동적 공식은 1단계 연산 실패 시 0.05초 이내에 기본(Fallback) 연산으로 전환되어야 한다.
2. 건강 수치 표시 UI는 게임 요소보다 항상 상위에 배치되며 직관성을 유지한다.

## State
* 상태: Proposed -> Active (Patch 006)

## Event
* `EVENT_PATCH_006_APPLIED`: 패치 적용 완료 이벤트 발생

## Example
* 심박수 변동성 데이터 미수집 시 -> 기본 BMR 공식(Mifflin-St Jeor) 자동 적용.

## Exception
* DB 마이그레이션 실패 시 PATCH_005 상태로 자동 롤백.

## Related Documents
* `HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V6_SPEC.md`
* `HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V6.md`

## Change History
* **2026-07-31 (V6.0.0)**: Patch 006 변경 내역 문서 최초 작성 (V6 체계 구축).