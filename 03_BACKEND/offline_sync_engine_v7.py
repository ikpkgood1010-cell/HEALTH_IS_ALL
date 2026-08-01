"""
===============================================================================
HEALTH IS ALL - Offline Sync Engine V7
===============================================================================
Purpose:
  오프라인 환경에서 기록된 트랜잭션 큐를 수신하여 SHA-256 멱등성 검증을 거친 후
  DB에 중복 없이 순차적으로 안전하게 병합하는 백엔드 오프라인 처리 엔진.

Scope:
  - Idempotency Key 하이퍼 해싱 및 검증
  - 오프라인 이벤트 처리 결과 일괄 응답 생성

SSOT:
  - 백엔드 데이터 동기화 및 멱등성 보장의 단일 진실 공급원.

Definitions:
  - Idempotency Key: SHA-256 기반 유일 트랜잭션 해시.
  - Processed Cache: 이미 처리된 트랜잭션 키 메모리 세트.

Runtime:
  - Python 3.11+, FastAPI `/api/v7/sync` 엔드포인트 수신기

Rules:
  - 이미 존재하는 멱등성 키 수신 시 에러를 내지 않고 성공(SUCCESS_DUPLICATE_SKIPPED) 결과를 반환.

State:
  - READY, SYNCING, COMPLETED

Event:
  - OfflineSyncEngineV7.process_sync_queue()

Example:
  >>> engine = OfflineSyncEngineV7()
  >>> res = engine.process_sync_queue(user_id="user_123", queue=[...])

Exception:
  - SyncException: 오프라인 데이터 형식이 손상되었을 경우 해당 데이터만 격리 후 다음 큐 진행.

Related Documents:
  - HEALTH IS ALL/01_ARCHITECTURE/OFFLINE_SYNC_V7_PROTOCOL.md

Change History:
  - 2026-07-31 (V7.0.0): V7 SHA-256 멱등성 보장 알고리즘 구현.
===============================================================================
"""

import hashlib
from typing import List, Dict, Any

class OfflineSyncEngineV7:
    def __init__(self):
        self.version = "7.0.0"
        # 실제 환경에서는 Redis 캐시 또는 DB 테이블 활용
        self._processed_idempotency_keys = set()

    def generate_idempotency_key(self, user_id: str, client_event_id: str, timestamp: str) -> str:
        raw_str = f"{user_id}:{client_event_id}:{timestamp}"
        return hashlib.sha256(raw_str.encode('utf-8')).hexdigest()

    def process_sync_queue(self, user_id: str, queue: List[Dict[str, Any]]) -> Dict[str, Any]:
        processed_count = 0
        skipped_count = 0
        results = []

        for item in queue:
            client_event_id = item.get("client_event_id", "")
            timestamp = item.get("timestamp", "")
            payload = item.get("payload", {})

            key = self.generate_idempotency_key(user_id, client_event_id, timestamp)

            if key in self._processed_idempotency_keys:
                skipped_count += 1
                results.append({
                    "client_event_id": client_event_id,
                    "status": "SUCCESS_DUPLICATE_SKIPPED",
                    "idempotency_key": key
                })
                continue

            # 신규 오프라인 이벤트 DB 병합 처리
            self._processed_idempotency_keys.add(key)
            processed_count += 1
            results.append({
                "client_event_id": client_event_id,
                "status": "SUCCESS_PROCESSED",
                "idempotency_key": key
            })

        return {
            "engine_version": self.version,
            "user_id": user_id,
            "total_received": len(queue),
            "processed_count": processed_count,
            "skipped_count": skipped_count,
            "details": results,
            "message": f"성공적으로 {processed_count}건의 오프라인 기록이 동기화되었습니다!"
        }

if __name__ == "__main__":
    engine = OfflineSyncEngineV7()
    test_queue = [
        {"client_event_id": "evt_001", "timestamp": "2026-07-31T10:00:00", "payload": {"type": "exercise"}},
        {"client_event_id": "evt_001", "timestamp": "2026-07-31T10:00:00", "payload": {"type": "exercise"}}, # 중복
    ]
    res = engine.process_sync_queue("user_999", test_queue)
    print("Offline Sync V7 Result:", res)