"""
HEALTH IS ALL - Dynamic Raid Dungeon & Weekly Health Quest Engine
Filename: raid_quest_engine.py
Path: HEALTH IS ALL/backend/raid_quest_engine.py
Purpose: 건강 행동 데이터를 레이드 보스 스탯 및 타격 딜량으로 환산하는 백엔드 수식 엔진
"""

import math
import random
from typing import Dict, Any, Optional, List

class RaidQuestEngine:
    """
    주간 건강 달성도 및 레이드 보스 매커니즘 산출 엔진
    """

    @staticmethod
    def generate_weekly_boss(user_historical_whs: float) -> Dict[str, Any]:
        """
        사용자의 지난 건강 지표(Historical WHS)를 기반으로 이번 주 보스 스탯 생성
        """
        safe_whs = max(10.0, min(100.0, user_historical_whs))
        
        # 보스 체력 수식: 기본 10,000 HP + 로그 성장 곡선
        hp_factor = 1.0 + math.log10(1.0 + (safe_whs / 100.0))
        boss_max_hp = int(10000 * hp_factor)
        
        return {
            "boss_id": f"BOSS_WEEK_{random.randint(100, 999)}",
            "boss_name": "타락한 태만 골렘",
            "boss_max_hp": boss_max_hp,
            "boss_current_hp": boss_max_hp,
            "is_enraged": False,
            "target_whs": safe_whs
        }

    @staticmethod
    def calculate_raid_damage(
        workout_minutes: float,
        today_nbs: float,
        clean_streak: int,
        cardio_ratio: float = 0.5,
        recent_3wk_avg_min: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        일일 건강 활동에 따른 레이드 딜량(Damage) 정밀 수식 산출
        """
        is_fallback_used = False

        # 1. 데이터 미비 시 Fallback (최근 3주 이동 평균 적용)
        if workout_minutes <= 0 and recent_3wk_avg_min is not None:
            workout_minutes = recent_3wk_avg_min * 0.7
            is_fallback_used = True

        safe_workout = max(0.0, min(300.0, workout_minutes))
        safe_nbs = max(10.0, min(100.0, today_nbs))

        # 2. 운동 스케일 인자 (로그 감소 적용으로 고강도 폭증 방지)
        workout_factor = 1.0 + math.log(1.0 + safe_workout / 15.0)

        # 3. 식단 영양 가중치 인자 (0.1 ~ 1.0)
        nutrition_factor = safe_nbs / 100.0

        # 4. 연속 달성 보너스 (Clean Streak)
        streak_bonus = 1.0 + min(0.35, clean_streak * 0.05)

        # 5. 유산소/무산소 밸런스 가중치 (0.5 균형일 때 최대)
        balance_bonus = 1.0 + (0.15 - abs(cardio_ratio - 0.5) * 0.3)

        # 6. 미세 동적 변동 난수 (0.92 ~ 1.08)
        jitter = random.uniform(0.92, 1.08)

        # 최종 딜량 수식
        base_damage = 500.0
        final_damage = int(base_damage * workout_factor * nutrition_factor * streak_bonus * balance_bonus * jitter)

        # 회복 또는 크리티컬 판정
        is_critical = (safe_nbs >= 85 and safe_workout >= 45)

        if is_critical:
            final_damage = int(final_damage * 1.5)

        return {
            "damage_dealt": max(50, final_damage),
            "is_critical": is_critical,
            "workout_factor": round(workout_factor, 2),
            "nutrition_factor": round(nutrition_factor, 2),
            "streak_bonus_pct": round((streak_bonus - 1.0) * 100, 1),
            "is_fallback_used": is_fallback_used
        }

if __name__ == "__main__":
    # 테스트
    engine = RaidQuestEngine()
    boss = engine.generate_weekly_boss(user_historical_whs=75.0)
    print(f"[Boss Generated] {boss}")

    dmg = engine.calculate_raid_damage(
        workout_minutes=50, today_nbs=88.5, clean_streak=4, cardio_ratio=0.5
    )
    print(f"[Damage Calculated] {dmg}")