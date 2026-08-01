# RELEASE_READINESS_CHECKLIST_V5.md

## Purpose
본 문서는 'HEALTH IS ALL' 서비스 배포 전 최신 시스템 품질, SSOT 규칙 준수, 동적 계산 수식 안정성, UX/UI 모바일 가독성을 최종 점검하는 배포 준비 체크리스트 v5입니다.

## Scope
* 백엔드 및 모바일 앱 엔드투엔드(E2E) 시스템 통합 검수
* 동적 수식 연산 및 에러 발생 시 폴백 로직 검증
* SSOT 문서 표준 규격 준수 여부 점검

## SSOT
* **경로**: `HEALTH IS ALL/00_PROJECT/RELEASE_READINESS_CHECKLIST_V5.md`
* **소유팀**: Release & Quality Assurance Team

## Definitions
* **Zero-Critical Policy**: 크리티컬한 버그나 수식 연산 에러가 0건이어야 배포 승인되는 원칙.

## Runtime
* **실행 환경**: CI/CD Pipeline (GitHub Actions) 및 QA Staging Environment

## Rules
1. 모든 필수 문서는 SSOT, Related Documents, Change History 항목을 반드시 포함해야 한다.
2. 모바일 디바이스에서 글자 잘림 현상이 없어야 하며 자동 줄바꿈이 정상 작동해야 한다.
3. 수식 복잡도로 인한 런타임 에러 발생 시 100% 확률로 폴백 수식으로 전환되어야 한다.

## State
* `DRAFT`: 체크리스트 작성 중
* `IN_CHECK`: 검수 진행 상태
* `PASSED`: 모든 항목 통과 및 배포 가능 상태

## Event
* `ON_QA_APPROVED`: 최종 QA 검수 승인
* `ON_RELEASE_DEPLOYED`: 프로덕션 배포 완료

## Example
* 백엔드 dynamic_health_engine_v9 실행 중 에러를 강제로 주입했을 때, 시스템이 중단되지 않고 1단계 폴백 수식을 실행하여 유저 화면에 정상 출력이 확인되면 검수 통과 처리됨.

## Exception
* 테스트 커버리지 85% 미달 시: 배포 프로세스 자동 차단(Block).

## Related Documents
* `HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V9_SPEC.md`
* `HEALTH IS ALL/06_QA/QA_TEST_STRATEGY_V7.mdux`

## Change History
* **v5.0.0 (2026-07-31)**: V4 대비 다변수 수식 검증 항목 추가, 모바일 UX 줄바꿈 및 복사 UI 검수 표준 도입.