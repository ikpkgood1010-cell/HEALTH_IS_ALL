"""
HEALTH IS ALL - Offline Outbox Sync & Validation Engine
Filename: offline_sync_engine.py
Path: HEALTH IS ALL/backend/offline_sync_engine.py
Purpose: 오프라인 아웃박스 페이로드의 멱등성 검증, 타임스탬프 충돌 보정 및 동기화 처리 백엔드 엔진
"""

import hashlib
import time
import math
from typing import Dict, Any, List, Tuple

class OfflineSyncEngine:
    """
    오프라인 동기화 페이로드 검증 및 중복 방지 처리 클래스
    """

    def __init__(self):
        # 처리 완료된 Idempotency Key 인메모리 캐시 (실제 운영 시 Redis/DB 적용)
        self.processed_keys: set = set()

    def generate_idempotency_key(self, user_id: str, payload_type: str, timestamp: float, raw_data: str) -> str:
        """
        고유 멱등성 키 생성 (사용자 ID + 데이터 유형 + 시간 + 원본 데이터 해시)
        """
        base_str = f"{user_id}:{payload_type}:{int(timestamp)}:{raw_data}"
        return hashlib.sha256(base_str.encode('utf-8')).hexdigest()

    def calculate_backoff_sec(self, retry_count: int, base_sec: float = 2.0, max_sec: float = 300.0) -> float:
        """
        지수 백오프 및 변동성(Jitter) 계산 수식
        """
        jitter = (time.time() * 1000) % 1.5  # 미세 난수 대체
        calculated_backoff = (base_sec * math.pow(2, min(retry_count, 10))) + jitter
        return min(max_sec, calculated_backoff)

    def process_sync_batch(self, user_id: str, server_time: float, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        동기화 큐 일괄 검증 및 동적 가중치 순 정렬 처리
        """
        success_list = []
        failed_list = []
        audit_list = []

        # 1. 우선순위 가중치(Sync Weight) 기준 내림차순 정렬
        sorted_items = sorted(items, key=lambda x: x.get('sync_weight', 0), reverse=True)

        for item in sorted_items:
            payload_id = item.get('queue_id')
            payload_type = item.get('type')  # 'HEALTH_LOG' or 'SPIRIT_REWARD'
            client_time = item.get('created_at_utc', server_time)
            raw_data = str(item.get('payload', {}))
            key = self.generate_idempotency_key(user_id, payload_type, client_time, raw_data)

            # 2. 중복 처리 검증 (Idempotency Check)
            if key in self.processed_keys:
                success_list.append({"queue_id": payload_id, "status": "ALREADY_PROCESSED"})
                continue

            # 3. 타임스탬프 조작 검증 (24시간 이상 오차 시 Exception)
            time_diff = abs(server_time - client_time)
            if time_diff > 86400:  # 24시간
                audit_list.append({
                    "queue_id": payload_id,
                    "reason": "TIMESTAMP_SKEW_EXCEEDED",
                    "action": "HEALTH_ONLY_ACCEPTED"
                })
                self.processed_keys.add(key)
                continue

            # 4. 데이터 정상 반영 처리
            self.processed_keys.add(key)
            success_list.append({
                "queue_id": payload_id,
                "status": "SYNCED",
                "processed_at": server_time
            })

        return {
            "total_received": len(items),
            "synced_count": len(success_list),
            "synced_items": success_list,
            "failed_items": failed_list,
            "manual_audit_items": audit_list
        }

if __name__ == "__main__":
    engine = OfflineSyncEngine()
    now = time.time()
    sample_batch = [
        {
            "queue_id": "Q001",
            "type": "HEALTH_LOG",
            "created_at_utc": now - 300,
            "sync_weight": 110,
            "payload": {"workout_min": 45, "calories_burned": 320}
        },
        {
            "queue_id": "Q002",
            "type": "SPIRIT_REWARD",
            "created_at_utc": now - 300,
            "sync_weight": 10,
            "payload": {"catalyst_gained": 15}
        }
    ]
    res = engine.process_sync_batch("USER_101", now, sample_batch)
    print(f"[Sync Processing Result] {res}")