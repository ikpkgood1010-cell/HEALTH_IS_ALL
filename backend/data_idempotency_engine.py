"""
HEALTH IS ALL - Data Idempotency Engine
Filename: data_idempotency_engine.py
Path: HEALTH IS ALL/backend/data_idempotency_engine.py
Purpose: Idempotency Key 기반 중복 트랜잭션 차단 및 데이터 무결성 보장 엔진
"""

import hashlib
from typing import Dict, Any, Set

class DataIdempotencyEngine:
    """
    트랜잭션 멱등성 보장 및 중복 검증 엔진
    """

    _processed_keys: Set[str] = set()

    @classmethod
    def execute_idempotent_transaction(
        cls,
        idempotency_key: str,
        user_id: str,
        action_type: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        중복 트랜잭션 여부를 판별하여 단 1회만 처리
        """
        # 1. 트랜잭션 고유 핑거프린트 해시 생성
        raw_sig = f"{user_id}:{action_type}:{idempotency_key}"
        tx_hash = hashlib.sha256(raw_sig.encode('utf-8')).hexdigest()

        # 2. 이미 처리된 키인지 검증
        if tx_hash in cls._processed_keys:
            return {
                "status": "DUPLICATE_SKIPPED",
                "idempotency_key": idempotency_key,
                "message": "이미 수호 정령이 소중하게 챙겨둔 기록입니다 🌿 (중복 반영 차단됨)",
                "applied": False
            }

        # 3. 신규 트랜잭션 등록 및 처리
        cls._processed_keys.add(tx_hash)

        return {
            "status": "SUCCESS",
            "idempotency_key": idempotency_key,
            "message": "새로운 건강 기록이 정령의 정원에 정상적으로 반영되었습니다 ✨",
            "applied": True
        }

if __name__ == "__main__":
    engine = DataIdempotencyEngine()
    key = "UUID-9876-4321-ABCDE"
    res1 = engine.execute_idempotent_transaction(key, "USER_001", "ADD_WATER", {"amount_ml": 250})
    res2 = engine.execute_idempotent_transaction(key, "USER_001", "ADD_WATER", {"amount_ml": 250})
    print(f"[First Exec]: {res1}")
    print(f"[Second Exec]: {res2}")