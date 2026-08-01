"""
HEALTH IS ALL - Spirit Album & Memory Engine
Filename: spirit_album_engine.py
Path: HEALTH IS ALL/backend/spirit_album_engine.py
Purpose: 건강 달성 기록에 따른 정령 도감 해금 및 정령 친밀도(SAL) 수식 계산 백엔드 엔진
"""

import random
from typing import Dict, Any, List

class SpiritAlbumEngine:
    """
    정령 도감 해금 및 힐링 메모리 관리 엔진
    """

    @staticmethod
    def calculate_album_status(
        total_clean_meals: int,
        total_steps: int,
        consecutive_days: int
    ) -> Dict[str, Any]:
        """
        정령 친밀도(SAL) 계산 및 해금된 앨범 스냅샷 목록 반환
        """
        jitter = random.uniform(0.98, 1.02)

        # 친밀도 수식 (SAL)
        base_sal = (total_clean_meals * 12.0) + (total_steps / 5000.0) + (consecutive_days * 15.0)
        sal_score = round(base_sal * jitter, 1)

        # 앨범 해금 스냅샷 도출
        unlocked_snapshots = []
        
        if total_steps >= 50000:
            unlocked_snapshots.append({
                "id": "SNAP_001",
                "title": "🍃 바람의 언덕에서 보낸 첫 걸음",
                "desc": "누적 5만 보를 달성하여 바람의 정령과 함께 찍은 소중한 순간입니다."
            })
        
        if total_clean_meals >= 20:
            unlocked_snapshots.append({
                "id": "SNAP_002",
                "title": "🥩 담백한 스팀 오프닝",
                "desc": "정갈한 클린 식단 20회를 달성하여 정령의 정원이 더욱 맑아졌습니다."
            })

        if consecutive_days >= 7:
            unlocked_snapshots.append({
                "id": "SNAP_003",
                "title": "✨ 7일 연속 온기의 약속",
                "desc": "일주일 동안 매일 정령을 돌봐주며 단단한 유대감을 형성했습니다."
            })

        return {
            "spirit_affinity_level": sal_score,
            "unlocked_count": len(unlocked_snapshots),
            "snapshots": unlocked_snapshots,
            "next_unlock_hint": "다음 해금: 누적 10만 보 달성 시 '은하수 방패 정령' 스냅샷 해금 🌌"
        }

if __name__ == "__main__":
    engine = SpiritAlbumEngine()
    res = engine.calculate_album_status(total_clean_meals=25, total_steps=62000, consecutive_days=10)
    print(f"[Spirit Album Engine Output] {res}")