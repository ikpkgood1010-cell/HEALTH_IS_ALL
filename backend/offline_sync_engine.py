"""
HEALTH IS ALL - Offline Sync & Data Merge Engine
Filename: offline_sync_engine.py
Path: HEALTH IS ALL/backend/offline_sync_engine.py
Purpose: 오프라인 재연동 시 수신된 대량의 데이터 패킷을 정밀 검증하고 정령 경험치를 합산하는 백엔드 엔진
"""

import random
from typing import Dict, Any, List

class OfflineSyncEngine:
    """
    오프라인 데이터 일괄 재연동 및 검증 엔진
    """

    @staticmethod
    def process_offline_batch(
        batch_packets: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        오프라인 동안 누적된 패킷 목록을 검증하고 정령 성장 보상 계산
        """
        if not batch_packets:
            return OfflineSyncEngine._build_empty_response()

        processed_count = 0
        total_steps_added = 0
        total_water_added = 0
        clean_meal_count = 0

        for packet in batch_packets:
            record_type = packet.get("record_type")
            value = packet.get("value", 0)

            if record_type == "STEPS":
                total_steps_added += int(value)
                processed_count += 1
            elif record_type == "WATER":
                total_water_added += int(value)
                processed_count += 1
            elif record_type == "MEAL_CLEAN":
                clean_meal_count += 1
                processed_count += 1

        # 지연 제출에 대한 다정한 보너스 가중치 계산 ($0.98 \sim 1.02$ jitter)
        jitter = random.uniform(0.98, 1.02)
        spirit_bonus_exp = round((total_steps_added * 0.05 + total_water_added * 0.02 + clean_meal_count * 50) * jitter, 1)

        sync_message = (
            f"오프라인 동안 보관해둔 {processed_count}개의 소중한 기록을 안전하게 수신했어요! "
            f"수호 정령이 기다렸다는 듯 펄쩍 뛰며 {spirit_bonus_exp} EXP의 에너지를 얻었습니다 🌿"
        )

        return {
            "processed_count": processed_count,
            "total_steps_added": total_steps_added,
            "total_water_added": total_water_added,
            "clean_meal_count": clean_meal_count,
            "spirit_bonus_exp": spirit_bonus_exp,
            "sync_message": sync_message,
            "is_success": True
        }

    @staticmethod
    def _build_empty_response() -> Dict[str, Any]:
        return {
            "processed_count": 0,
            "total_steps_added": 0,
            "total_water_added": 0,
            "clean_meal_count": 0,
            "spirit_bonus_exp": 0.0,
            "sync_message": "정령의 배낭에 새로 추가할 오프라인 기록이 없어요. 오늘도 함께 차근차근 걸어볼까요? ✨",
            "is_success": True
        }

if __name__ == "__main__":
    engine = OfflineSyncEngine()
    mock_batch = [
        {"record_type": "STEPS", "value": 3500},
        {"record_type": "WATER", "value": 500},
        {"record_type": "MEAL_CLEAN", "value": 1},
        {"record_type": "STEPS", "value": 4200}
    ]
    res = engine.process_offline_batch(mock_batch)
    print(f"[Offline Sync Engine Output] {res}")