# NEXT_AI_WORK_INSTRUCTION_PATCH_005

## 목적
PATCH-005 완료 직후 다음 작업자가 가장 먼저 처리해야 할 운영형 후속 액션을 정리한다.

## 이번 패치에서 확정된 것
1. Verification & Traceability Layer 10종 문서 생성 완료
2. `Exp.` → `Exp` active code/user-facing 문자열 정리 완료
3. pytest 수집 실패 원인(`backend` import, `03_BACKEND`/`04_FRONTEND` 경로 문제) 수정 완료
4. `dynamic_health_engine_v13.py` 반올림 로직 보정 후 전체 테스트 통과
5. orphan 후보를 즉시 삭제하지 않고 register 기반 분류로 전환

## 지금 바로 먼저 할 일
1. `00_PROJECT/PATCH_005_EXECUTION_REPORT.md` 검토
2. `00_PROJECT/IMPLEMENTATION_STATUS_MATRIX.md`에서 `Partial/No` 항목 우선순위 확정
3. `03_BACKEND/ORPHAN_MODULE_REGISTER.md` 기준으로 Roadmap / Archive 실제 이동 범위 결정
4. `lib/main_navigation_screen.dart`에 어떤 화면을 연결할지 제품 결정
5. Provider 잔존 화면의 Riverpod migration backlog 작성

## P0 후속 과제
- Event ID를 코드 객체/상수로 승격
- `EVT_USER_LOG_RECORDED` 중심의 producer/consumer 명시화
- Weekly soft cap 2100 런타임 상수 승격 여부 결정
- Point 경제 SSOT와 백엔드 영속화 계약 정의

## P1 후속 과제
- `datetime.utcnow()` 경고를 timezone-aware UTC로 정리
- Flutter 쪽 widget / golden / navigation 테스트 추가
- offline sync / wearable / monthly report의 active 여부 결정
- orphan 후보 중 archive 대상 실제 이동

## 금지사항
- SSOT 문서와 코드 중 한쪽만 수정하는 hotfix
- orphan 후보를 active feature처럼 설명하는 행위
- Provider 신규 확장
- Formula/Event ID 없이 구현만 추가하는 행위

## 완료 기준
- Event/Runtime 영역이 `Partial`에서 `Implemented` 또는 명시적 `Roadmap`으로 수렴
- main navigation 연결 범위 확정
- orphan 후보가 실제 폴더 정책까지 반영
- warning budget 축소 및 Flutter 테스트 추가
