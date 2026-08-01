# [중복문서-덮어쓰기, 교체] Release Readiness Checklist V2

## Purpose
'HEALTH IS ALL' 앱이 건강 관리 목적(식단, 운동, 찜 요리 등 건강 루틴)과 뛰어난 RPG 게임성(정령 진화, 길드 챌린지)을 모두 최고 수준으로 만족하는지 최종 검증합니다.

## Scope
- 백엔드 계산식 정밀도, 프론트엔드 UI 렌더링 속도, 데이터 무결성 검증 항목

## SSOT
- 배출 및 릴리즈 승인의 최종 기준 문서.

## Definitions
- **Quality Equilibrium**: 건강 유틸리티와 게임적 재미가 상호 방해하지 않고 균형을 이루는 상태.

## Runtime
- 배포 파이프라인 구동 전 로컬 및 CI 환경에서 검증.

## Rules
1. 두 가지 요소 중 어느 한쪽이 부실할 경우 배포를 보류합니다.
2. 모든 계산식은 무작위 변수와 예외 상황 테스트를 통과해야 합니다.

## State
- 릴리즈 승인 상태 (`ReleaseApproved: True/False`).

## Event
- `CHECKLIST_VERIFIED`: 모든 항목 통과 시 발생.

## Example
- [x] 다변수 동적 계산식 오차율 검증 완료
- [x] 식단-정령 연동 촉매 시스템 테스트 통과
- [x] 오프라인 우선 동기화 안정성 확인

## Exception
- 테스트 실패 항목 발생 시 해당 버전 스펙으로 롤백 후 수정.

## Related Documents
- `HEALTH IS ALL/00_PROJECT/RELEASE_CHECKLIST_SPEC.md`

## Change History
- v2.0 (2026-07-31): 건강-게임 밸런스 검증 항목 추가