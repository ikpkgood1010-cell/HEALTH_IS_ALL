# NEXT_AI_EXECUTION_PLAN_PATCH_004

## Phase 1 — Drift 정리
1. canonical constants 검증 스크립트 실행
2. 상수 mismatch 발견 시 문서/코드/테스트 동시 수정 범위 확정
3. `Exp.` / `Exp` 표기 drift 목록화

## Phase 2 — Naming 정렬
1. `CANONICAL_NAMING.md`를 역할명 `정령`, 기본 이름 `건강이` 구조로 정리
2. 사용자 노출 문자열에서 `XP`, `EXP`, `Spirit` 신규 사용 금지
3. 레거시 파일은 기술 부채와 orphan 정책으로 분리

## Phase 3 — Frontend 운영화
1. `main_navigation_screen.dart` 미연결 화면 결정
2. Provider -> Riverpod migration backlog 작성
3. 손상 템플릿 문자열이 있는 화면 정리

## Phase 4 — Backend 계약 고정
1. request/response contract test 보강
2. anti-farming / cap / fallback regression test 추가
3. 레벨업 기준 상수 분리 여부 결정

## Phase 5 — Orphan 정책 집행
1. orphan 후보 import/route scan
2. archive 이동 또는 roadmap 복귀 결정
3. 복귀 시 리네이밍 + 테스트 + 연결 작업을 한 세트로 수행

## 완료 기준
- 상수 drift 0
- API contract 문서와 코드 일치
- 상태관리 표준이 신규 코드에 일관 적용
- orphan 후보가 active/roadmap/archive로 분류 완료
