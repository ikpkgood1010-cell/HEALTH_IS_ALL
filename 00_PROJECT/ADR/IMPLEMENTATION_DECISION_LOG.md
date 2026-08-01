# IMPLEMENTATION_DECISION_LOG

- Version: 1.0
- Status: Active
- Last Updated: 2026-08-01
- Purpose: PATCH-005 기준 구현 의사결정과 근거를 기록한다.

## ADR-014 — Daily Exp Soft Cap = 300
- Status: Accepted
- Decision: 일일 성장 반영 상한은 300 Exp로 고정한다.
- Rationale: 문서/코드/테스트 일치 확보와 성장 경제 안정성 확보.
- Evidence: `backend/config.py`, `backend/models.py`, `lib/mock_data_provider.dart`, `03_GAME_SYSTEM/EXP_RULE.md`.

## ADR-015 — 역할명은 `정령`, 기본 이름은 `건강이`
- Status: Accepted
- Decision: 역할명(role)과 기본 이름(default name)을 분리한다.
- Rationale: UX 표기 일관성과 캐릭터 개인화 지원.
- Evidence: `00_PROJECT/CANONICAL_NAMING.md`, `backend/config.py`, `backend/models.py`.

## ADR-016 — 사용자 노출 표기는 `Exp`
- Status: Accepted
- Decision: active code/user-facing string에서 `Exp.`를 `Exp`로 통일한다.
- Rationale: PATCH-004 handoff에서 지정한 표준 반영.
- PATCH-005 Action: backend/UI active code의 `Exp.` 문자열 정리 완료.

## ADR-017 — pytest 경로 부트스트랩 추가
- Status: Accepted
- Decision: 루트 `conftest.py`, `backend/__init__.py`, `pytest.ini`를 추가해 테스트 수집 안정성을 확보한다.
- Rationale: `backend`, `03_BACKEND`, `04_FRONTEND` 모듈 import 실패로 검증이 막히는 문제 해소.

## ADR-018 — Dynamic Health Engine 정밀 반올림 적용
- Status: Accepted
- Decision: `03_BACKEND/dynamic_health_engine_v13.py`의 다변수 보상 계산은 floor가 아닌 round를 사용한다.
- Rationale: 기존 테스트 및 문서 기대값 966과 일치시키고 계산 오차를 줄이기 위함.

## ADR-019 — Orphan는 즉시 삭제하지 않고 분류한다
- Status: Accepted
- Decision: orphan 후보는 `Active / Roadmap / Archive Candidate`로 문서화 후 이동한다.
- Rationale: 기능 재사용 가능성을 보존하면서 오동작 설명을 방지한다.

## Open Decisions
1. `main_navigation_screen.dart`에 diet/workout/settings를 연결할지 여부
2. Weekly soft cap 2100을 런타임 상수로 승격할지 여부
3. Event bus / outbox / scheduler를 어느 계층에서 구현할지 여부
4. Provider 잔존 화면을 Riverpod로 언제 마이그레이션할지 여부
