# DATA_IDEMPOTENCY_SPEC.md

## Purpose
본 문서는 오프라인 동기화 재시도나 네트워크 재요청으로 인해 동일한 건강 기록(식단, 걸음 수, 수분)이 중복 전송되더라도, DB 반영 및 정령 경험치 합산이 단 1회만 정확히 이루어지도록 보장하는 멱등성(Idempotency) 규격을 정의한다.

## Scope
1. 클라이언트 생성 고유 UUID 기반의 Idempotency Key 파이프라인 구축
2. 중복 패킷 수신 시 기존 결과값 즉시 반환(No Double Increment)
3. 정령 스탯 및 퀘스트 달성 수치의 이중 반영 완벽 차단
4. 데이터 중복 제거에 따른 안전한 정령 성장 보장

## SSOT
본 문서는 멱등성 백엔드 엔진(`backend/data_idempotency_engine.py`)의 최상위 **SSOT(Single Source of Truth)**로 기능한다.

## Definitions
- **Idempotency Key**: 클라이언트에서 데이터 생성 시 부여하는 `UUIDv4` 형태의 고유 식별자.
- **Deduplication Window**: 동일 트랜잭션 키의 중복 수신 여부를 검증하는 백엔드 메모리/캐시 유지 기간(7일).

## Runtime
- 백엔드(FastAPI/Python): 수신된 Idempotency Key의 캐시 존재 여부 검사, 신규 처리 또는 기존 처리 결과 반환 분기.

## Rules
1. **단일 반영 원칙**: 동일한 식단/운동 기록에 의해 정령의 경험치나 보상이 두 번 지급되는 오류를 근본적으로 차단한다.
2. **투명한 유저 피드백**: 중복 데이터가 걸러지더라도 유저에게는 "이미 정령이 기쁘게 챙겨둔 기록입니다 ✨"라는 친근한 대답을 전달한다.
3. **세분화 동적 수식**: 트랜잭션 핑거프린트 산출을 위한 SHA-256 해시 및 조합 공식 적용.

## State
- `idempotency_key_store`, `processed_transaction_count`
- `duplicate_blocked_count`

## Event
- `ON_TRANSACTION_RECEIVE`: 트랜잭션 수신 및 키 검증
- `ON_DUPLICATE_DETECTED`: 중복 트랜잭션 감지 및 기존 승인 결과 응답

## Example
$$\text{TransactionHash} = \text{SHA256}(\text{UserID} + \text{Timestamp} + \text{RecordType} + \text{Value})$$

## Exception
- 캐시 서버 장애 시 DB Unique Constraint 단에서 secondary 처리하여 데이터 중복 입력을 최종 차단한다.

## Related Documents
- `01_ARCHITECTURE/OFFLINE_SYNC_SPEC.md`
- `01_ARCHITECTURE/MONTHLY_REPORT_SPEC.md`

## Change History
- 2026-07-31 (PATCH_018): 데이터 멱등성 보장 & 중복 제거 명세서 신규 작성 (SSOT 규격 준수).