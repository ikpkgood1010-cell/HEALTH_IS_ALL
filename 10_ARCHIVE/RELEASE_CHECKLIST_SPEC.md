# RELEASE_CHECKLIST_SPEC.md

## Purpose
프로덕션 배포 전 필수 조건의 이행 여부를 검증하는 최종 게이트키핑 절차를 정의한다.

## Rules
1. **DB 마이그레이션 호환성**: 다운타임 없는 롤백이 가능하도록 모든 DB Schema 변경은 Backwards Compatible 해야 함.
2. **보안 검증**: `.env` 파일 내 개발용 MOCK 키 유출 여부 점검.

## Change History
* **v1.0.0 (2026-07-31)**: PATCH-005 최초 작성.