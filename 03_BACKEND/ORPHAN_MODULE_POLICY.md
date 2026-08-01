# ORPHAN_MODULE_POLICY

- Document Name: ORPHAN_MODULE_POLICY.md
- Version: 1.0
- Status: Active
- Owner: PATCH-004 Implementation Governance
- Last Updated: 2026-08-01
- Purpose: 미사용 코드와 향후 사용 예정 코드를 구분하고, 방치된 모듈을 통제한다.
- Implementation Status: Implemented
- Source of Truth: Documentation
- Verification:
  - Last Verified Date: 2026-08-01
  - Verified By: PATCH-004 governance pass
  - Test Reference: import/route scan baseline

## Orphan 정의
다음 조건 중 하나를 만족하면 orphan 후보다.
1. 실행 진입점(route/navigation/main)에서 참조되지 않음
2. 테스트도 없고 문서상 활성 표시도 없음
3. 유사 책임의 활성 모듈이 별도로 존재함
4. 이름/용어/계약이 현재 SSOT와 크게 어긋남

## 탐지 기준
- import graph에 없음
- navigation route에 없음
- API router/app에 연결 없음
- 최근 패치에서 활성 범위로 언급되지 않음
- legacy 용어가 강하게 남아 있음

## 허용 기준
다음 모두를 만족하면 orphan 상태로 임시 보유 가능하다.
1. 제품 로드맵상 복귀 예정
2. owner가 명시됨
3. 예상 복귀 시점이 있음
4. 활성 코드와의 충돌이 통제됨

## 삭제 기준
1. 2회 이상 review 주기 동안 owner 없음
2. 동일 책임의 활성 모듈이 대체 완료
3. 보안/품질/혼란 비용이 유지 가치보다 큼

## Archive 기준
1. 즉시 삭제 대신 `10_ARCHIVE/` 이동을 우선한다.
2. archive 이동 시 원래 경로, 이동 일자, 사유를 기록한다.
3. archive 파일은 실행 기준으로 참조하지 않는다.

## Review 주기
- 릴리스 전 1회
- 대형 리팩터링 전 1회
- 분기별 정리 1회

## Current Candidate List
- `backend/spirit_album_engine.py`
- `backend/spirit_evolution_engine.py`
- `backend/guild_challenge_engine.py`
- `backend/guild_synergy_engine.py`
- `lib/heartrate_spirit_widget.dart`
- `lib/guild_challenge_widget.dart`
- 기타 route 미연결/미호출 모듈

## Decision Outcomes
- Keep Active
- Keep Roadmap Orphan
- Archive
- Delete

## Related Source Files
- `backend/spirit_album_engine.py`
- `backend/spirit_evolution_engine.py`
- `backend/guild_challenge_engine.py`
- `lib/main_navigation_screen.dart`
- `lib/heartrate_spirit_widget.dart`

## Validation Method
- Import Scan
- Route Scan
- Manual Review
- Runtime Verification
