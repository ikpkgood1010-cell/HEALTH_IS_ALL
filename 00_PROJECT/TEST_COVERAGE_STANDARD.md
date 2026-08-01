# TEST_COVERAGE_STANDARD

- Document Name: TEST_COVERAGE_STANDARD.md
- Version: 1.0
- Status: Active
- Owner: PATCH-004 Implementation Governance
- Last Updated: 2026-08-01
- Purpose: 문서 검증보다 실행 검증을 우선하는 테스트 기준을 정의한다.
- Implementation Status: Implemented
- Source of Truth: Documentation + Test Code
- Verification:
  - Last Verified Date: 2026-08-01
  - Verified By: PATCH-004 governance pass
  - Test Reference: `test/`, `tests/`, future CI gate

## Principle
정적 검토는 참고자료이고, 최종 신뢰는 실행 검증이 만든다.

## Required Coverage Areas
### Unit
- Progression, Health Calculator, Quest, AI feedback, sync utility의 순수 로직

### Integration
- FastAPI route -> service/engine -> DB 기본 흐름
- Flutter state -> repository/service -> UI 반영 흐름

### Engine
- `progression_engine.py`
- `health_calculator.py`
- `quest_engine.py`
- reward/analytics/recommendation 계열 주요 엔진

### Formula
- cap, bonus, soft cap, fallback 계산식
- 동일 입력 대비 기대값 검증

### API
- request validation
- response contract
- error code / nullable rule
- Swagger와 실제 코드 일치 여부

### AI
- 피드백 메시지 fallback
- 금지 용어 유입 여부
- 건강 점수 범위(0~100)

### Offline
- 로컬 저장 성공 시 UI 즉시 반영
- 재시도/backoff 정책
- 중복 전송 방지

### Sync
- 동일 이벤트 재처리 방지
- conflict resolution
- wearable/offline 데이터 병합

### Regression
- Daily Cap
- anti-farming 10분 규칙
- default name / role label / API 기본값
- route 연결 여부

## Coverage Goals
- Backend core engine: 80%+
- API contract critical path: 90%+
- Formula branch coverage: 85%+
- Frontend state/reducer/controller critical path: 70%+
- Regression scenarios for canonical constants: 100% of listed constants

## Reporting Rule
테스트 결과는 반드시 아래처럼 구분한다.
- Static Check
- Compile Check
- Unit Test
- Integration Test
- Manual Runtime Verification

## Minimum Merge Gate
- 핵심 엔진 변경 시 unit test 필수
- API 계약 변경 시 integration/API test 필수
- 상수 변경 시 canonical constant check 필수
- orphan 복귀 시 route/import/runtime 검증 필수

## Related Source Files
- `test/progression_engine_test.py`
- `test/system_integration_test.py`
- `tests/test_backend.py`
- `backend/progression_engine.py`
- `backend/main.py`

## Validation Method
- Unit Test
- Integration Test
- Runtime Verification
- Regression Test
