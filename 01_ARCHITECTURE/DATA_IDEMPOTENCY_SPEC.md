# DATA_IDEMPOTENCY_SPEC.md

## Purpose
본 문서는 오프라인 동기화 재시도나 네트워크 재요청으로 인해 동일한 건강 기록(식단, 걸음 수, 수분)이 중복 전송되더라도, DB 반영 및 정령 경험치 합산이 단 1회만 정확히 이루어지도록 보장하는 멱등성(Idempotency) 규격을 정의한다.

## Scope
1. 클라이언트 생성 고유 UUID 기반의 Idempotency Key 파이프라인 구축
2. 중복 패킷 수신 시 DB에 저장된 기존 결과값 즉시 반환(No Double Increment)
3. 정령 스탯 및 퀘스트 달성 수치의 이중 반영 완벽 차단
4. 데이터 중복 제거에 따른 안전한 정령 성장 보장

## SSOT
본 문서는 멱등성 백엔드 엔진(`backend/data_idempotency_engine.py`)의 최상위 **SSOT(Single Source of Truth)**로 기능한다.

## Definitions
- **Idempotency Key**: 클라이언트에서 데이터 생성 시 부여하는 `UUIDv4` 형태의 고유 식별자.
- **Deduplication Window**: MVP 건강 기록은 `activity_logs` 보존 기간 전체. 프로세스 메모리나 7일 캐시에 의존하지 않는다.

## Runtime
- Flutter: 기록 시 UUIDv4를 생성하고 응답 실패 후 같은 입력을 재시도할 때 같은 키를 사용한다.
- 백엔드(FastAPI/Python): UUID를 `activity_logs.activity_id`에 저장하고 기존 PK 조회 후 신규 처리 또는 기존 결과 반환으로 분기한다.

## Rules
1. **단일 반영 원칙**: 동일한 식단/운동 기록에 의해 정령의 경험치나 보상이 두 번 지급되는 오류를 근본적으로 차단한다.
2. **투명한 유저 피드백**: 중복 데이터가 걸러지더라도 유저에게는 "이미 정령이 기쁘게 챙겨둔 기록입니다 ✨"라는 친근한 대답을 전달한다.
3. **키 오용 차단**: 동일 UUID가 다른 사용자·기록 종류·값·세부 데이터에 재사용되면 `409 Conflict`로 거절한다.

## State
- `activity_logs.activity_id` (client UUIDv4, canonical persistent store)
- `HealthRecordResponse.duplicate`

## Event
- `ON_TRANSACTION_RECEIVE`: 트랜잭션 수신 및 키 검증
- `ON_DUPLICATE_DETECTED`: 중복 트랜잭션 감지 및 기존 승인 결과 응답

## Example
$$\text{RecordID} = \text{Client UUIDv4}$$

## Exception
- DB primary key가 최종 동시성 차단 장치다. 별도 캐시 서버 장애 경로는 없다.

## Related Documents
- `01_ARCHITECTURE/OFFLINE_SYNC_SPEC.md`
- `01_ARCHITECTURE/MONTHLY_REPORT_SPEC.md`

## Change History
- 2026-07-31 (PATCH_018): 데이터 멱등성 보장 & 중복 제거 명세서 신규 작성 (SSOT 규격 준수).
- 2026-08-11: 인메모리 후보를 제거하고 `activity_logs` PK 기반 영속 멱등성을 canonical runtime에 연결.
