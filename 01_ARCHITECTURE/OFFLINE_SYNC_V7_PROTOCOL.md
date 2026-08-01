# OFFLINE_SYNC_V7_PROTOCOL.md

## Purpose
네트워크 미연결 상태에서 기록된 운동, 식단, 퀘스트 수행 데이터를 서버와 데이터 유실 없이 안전하게 연동하는 V7 동기화 프로토콜을 정의합니다.

## Scope
* 클라이언트 로컬 SQLite 저장소 페이로드 구조
* 서버 수신 시 멱등성 검증 및 데이터 충돌 해결

## SSOT
* 오프라인 트랜잭션 동기화 및 멱등성 보장에 관한 단일 진실 공급원.

## Definitions
* **Idempotency Key**: `SHA256(user_id + client_event_id + timestamp)` 형식의 고유 키.
* **Pending Queue**: 온라인 전환 시 전송 대기 중인 오프라인 생성 이벤트 큐.

## Runtime
* 모바일 네트워크 상태 변경 이벤트를 감지하여 Background Worker에서 실행.

## Rules
1. 모든 오프라인 트랜잭션은 생성 시 고유 `Idempotency Key`를 할당받는다.
2. 서버는 동일한 `Idempotency Key`가 이미 처리된 경우 `200 OK`와 기존 처리 결과를 반환하여 중복 처리를 차단한다.
3. 충돌 발생 시 클라이언트 데이터의 기록 시각이 더 최신인 경우 클라이언트 상태를 보존하고 서버 합산 수치를 재계산한다.

## State
* States: OFFLINE_QUEUED, SYNCING, SYNC_COMPLETED, CONFLICT_RESOLVED

## Event
* `EVENT_OFFLINE_QUEUE_FLUSH_STARTED`: 오프라인 대기열 서버 전송 시작.
* `EVENT_OFFLINE_SYNC_SUCCESS`: 오프라인 동기화 완전 성공.

## Example
* 비행기 탑승 중 기록한 산책 및 식단 데이터 5건이 연결 복구 즉시 순차적으로 완벽 반영됨.

## Exception
* 네트워크 연결 타임아웃 발생 시 지수 백오프(Exponential Backoff) 알고리즘을 적용하여 재시도.

## Related Documents
* `HEALTH IS ALL/03_BACKEND/offline_sync_engine_v7.py`
* `HEALTH IS ALL/lib/offline_sync_manager.dart`

## Change History
| 날짜 | 버전 | 작성자 | 변경 내용 |
| :--- | :--- | :--- | :--- |
| 2026-07-31 | V7.0.0 | Infrastructure | V7 SHA-256 멱등성 및 오프라인 대기열 안전 병합 프로토콜 명세화 |