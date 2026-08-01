# API_CONTRACT_STANDARD

- Document Name: API_CONTRACT_STANDARD.md
- Version: 1.0
- Status: Active
- Owner: PATCH-004 Implementation Governance
- Last Updated: 2026-08-01
- Purpose: Frontend와 Backend가 같은 계약을 보도록 요청·응답·오류·버전·검증 규칙을 표준화한다.
- Implementation Status: Implemented
- Source of Truth: Documentation + Code
- Verification:
  - Last Verified Date: 2026-08-01
  - Verified By: PATCH-004 governance pass
  - Test Reference: `backend/main.py`, `backend/models.py`, `tests/test_backend.py`

## Scope
- FastAPI 기반 HTTP API
- request/response schema
- validation, error, versioning, Swagger sync 규칙

## Request Rule
1. 모든 request schema는 Pydantic 모델 또는 동등한 typed schema를 사용한다.
2. 필수 필드는 명시적으로 required로 선언한다.
3. request 예시는 schema에 포함한다.
4. 서버가 계산하는 값(`exp_gained`, `daily_exp_cap`, `level`)은 request에서 받지 않는다.

## Response Rule
1. response는 코드와 문서가 동일한 필드명을 사용한다.
2. 필드명은 `snake_case`로 통일한다.
3. 날짜/시간은 ISO-8601 UTC를 기본으로 반환한다.
4. 사용자 표기용 문자열과 내부 계산 필드를 혼동하지 않는다.

## Current Core Contracts
### POST `/api/v1/health/record`
Request:
- `user_id: str`
- `record_type: str`
- `value: float`
- `detail_data: object | null`

Response:
- `success: bool`
- `record_id: str`
- `exp_gained: int`
- `current_daily_exp: int`
- `message: str`

### GET `/api/v1/health-i/status/{user_id}`
Response:
- `name: str`
- `level: int`
- `current_exp: int`
- `daily_exp_cap: int`
- `emotion_state: str`
- `dialogue: str`
- `equipped_skin: str`
- `last_updated: datetime`

## Pagination Rule
1. 목록 API가 추가되면 query parameter는 `page`, `page_size`, `cursor` 중 하나의 방식으로 통일한다.
2. 동일 도메인에서 page/cursor를 혼용하지 않는다.
3. response에는 `items`, `total_count` 또는 `next_cursor`를 포함한다.
4. 현재 핵심 API 두 개는 pagination 대상이 아니다.

## Error Rule
1. validation error와 business error를 구분한다.
2. 오류 응답 최소 필드:
   - `error_code`
   - `message`
   - `details` (optional)
   - `trace_id` (optional in non-debug)
3. 사용자 메시지에는 내부 예외나 SQL/stack trace를 노출하지 않는다.
4. anti-farming, daily cap 도달은 200 응답 + business message로 처리할 수 있으나, 향후 일관 정책으로 문서화해야 한다.

## Validation Rule
1. 숫자 범위, enum 후보, nullable 허용 범위를 schema에서 우선 표현한다.
2. `record_type` 같은 분기 키는 허용 목록을 문서화한다.
3. 서버는 클라이언트 계산 결과를 신뢰하지 않는다.
4. response 기본값도 canonical constants와 정합해야 한다.

## Version Rule
1. 공개 API는 `/api/v1/...`처럼 명시 버전을 사용한다.
2. breaking change는 `v2`로 올리고, 기존 `v1`은 deprecation 기간을 둔다.
3. 비파괴적 필드 추가는 minor 문서 변경으로 허용하되 nullable 규칙을 명확히 한다.

## Deprecation Rule
1. deprecated endpoint는 문서에 제거 예정일과 대체 endpoint를 함께 적는다.
2. 제거 전 테스트와 클라이언트 호출처를 전수 확인한다.
3. Swagger에서 deprecated 표시를 함께 유지한다.

## Date Format Rule
1. datetime은 ISO-8601 문자열을 사용한다.
2. 서버 저장/전송 기본 timezone은 UTC다.
3. 날짜 기준 정책(일일 캡 계산 등)은 사용자 Local Time 해석 여부를 별도 문서에서 정의한다.

## Timezone Rule
1. transport는 UTC 기준이다.
2. business rule에서 로컬 날짜를 쓸 경우 변환 지점을 명시한다.
3. 리셋/일일 집계 로직은 timezone 기준이 문서화되어야 한다.

## Locale Rule
1. 구조 필드명은 영문 `snake_case`를 유지한다.
2. 사용자 메시지(`message`, `dialogue`)는 locale-aware가 가능해야 한다.
3. 기본 locale은 ko-KR, fallback은 en-US로 정의한다.

## Nullable Rule
1. null 허용은 schema에서 명시한다.
2. optional 필드는 누락과 null을 구분해야 한다.
3. nullable 필드를 mandatory처럼 사용하는 구현은 금지한다.

## Swagger Sync Rule
1. Swagger/OpenAPI는 실제 코드와 동시에 갱신한다.
2. route, schema, field example, default value 변경 시 문서를 같이 고친다.
3. PR 리뷰에서 Swagger와 코드가 다르면 병합하지 않는다.
4. 테스트는 최소 1개 이상 실제 endpoint 응답 필드 구조를 검증한다.

## Related Source Files
- `backend/main.py`
- `backend/models.py`
- `backend/config.py`
- `tests/test_backend.py`

## Validation Method
- API Test
- Schema Review
- Swagger Review
- Runtime Verification
