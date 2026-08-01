"""
HEALTH IS ALL - Guild Synergy & Co-op Spirit Engine
Filename: guild_synergy_engine.py
Path: HEALTH IS ALL/backend/guild_synergy_engine.py
Purpose: 소셜 길드원들의 건강 활동 데이터를 합산하여 길드 정령 시너지 파워 및 협동 레이드 데미지를 계산하는 백엔드 엔진
"""

import math
import random
from typing import List, Dict, Any, Optional

class GuildSynergyEngine:
    """
    길드 협동 시너지 파워 및 레이드 진행률 계산 엔진
    """

    MAX_DAILY_USER_CONTRIBUTION = 1000.0  # 오버트레이닝 방지 1인당 최대 기여도 캡

    @staticmethod
    def calculate_guild_synergy(
        member_activities: List[Dict[str, Any]],
        boss_max_hp: float = 50000.0,
        current_boss_hp: float = 35000.0
    ) -> Dict[str, Any]:
        """
        길드원들의 활동 데이터(걸음수, 운동시간, 클린식단)를 수신하여 일일 시너지 파워를 산출
        """
        if not member_activities:
            # 1인 기본 모드 fallback
            return GuildSynergyEngine._build_single_user_fallback(boss_max_hp, current_boss_hp)

        total_raw_points = 0.0
        total_streaks = 0
        cheer_count_sum = 0

        for member in member_activities:
            steps = member.get("steps", 0)
            workout_min = member.get("workout_min", 0)
            clean_meals = member.get("clean_meals", 0)
            streak = member.get("streak_days", 1)
            cheers = member.get("cheers_sent", 0)

            # 개별 기여도 정밀 수식 (단위 변수별 가중치 적용)
            ind_point = (steps * 0.08) + (workout_min * 4.5) + (clean_meals * 40.0) + (cheers * 15.0)
            
            # 1인당 일일 기여도 캡(Cap) 적용하여 건강 안전 확보
            capped_point = min(GuildSynergyEngine.MAX_DAILY_USER_CONTRIBUTION, ind_point)
            
            total_raw_points += capped_point
            total_streaks += streak
            cheer_count_sum += cheers

        member_count = len(member_activities)
        avg_streak = total_streaks / member_count if member_count > 0 else 1.0

        # 동적 연속 출석(Streak) 배율 ($1.0 \sim 1.3$)
        streak_multiplier = min(1.3, 1.0 + (avg_streak * 0.015))

        # 미세 난수 인자 ($0.97 \sim 1.03$)를 적용하여 지루함 방지
        jitter = random.uniform(0.97, 1.03)

        # 최종 길드 시너지 파워 산출
        final_synergy_damage = total_raw_points * streak_multiplier * jitter

        # 보스 체력 차감
        new_boss_hp = max(0.0, current_boss_hp - final_synergy_damage)
        is_boss_defeated = (new_boss_hp == 0.0)

        # 유저 친화적 다정한 응원 팝업 문구 선택
        friendly_message = GuildSynergyEngine._get_encouraging_message(is_boss_defeated, cheer_count_sum)

        return {
            "guild_synergy_power": round(final_synergy_damage, 1),
            "previous_boss_hp": current_boss_hp,
            "remaining_boss_hp": round(new_boss_hp, 1),
            "boss_max_hp": boss_max_hp,
            "is_boss_defeated": is_boss_defeated,
            "streak_multiplier": round(streak_multiplier, 3),
            "friendly_encouragement": friendly_message,
            "is_single_fallback": False
        }

    @staticmethod
    def _build_single_user_fallback(boss_max_hp: float, current_boss_hp: float) -> Dict[str, Any]:
        """
        길드원 데이터가 없거나 1인 모드일 경우의 안전한 Fallback 계산
        """
        default_power = 350.0 * random.uniform(0.98, 1.02)
        new_hp = max(0.0, current_boss_hp - default_power)
        return {
            "guild_synergy_power": round(default_power, 1),
            "previous_boss_hp": current_boss_hp,
            "remaining_boss_hp": round(new_hp, 1),
            "boss_max_hp": boss_max_hp,
            "is_boss_defeated": new_hp == 0,
            "streak_multiplier": 1.0,
            "friendly_encouragement": "오늘도 나만의 정령과 함께 차근차근 걸어가고 있어요! 🌱",
            "is_single_fallback": True
        }

    @staticmethod
    def _get_encouraging_message(is_defeated: bool, cheers: int) -> str:
        if is_defeated:
            return "🎉 축하합니다! 길드원들의 따뜻한 실천이 모여 나태의 그림자를 물리쳤어요!"
        if cheers > 5:
            return "✨ 서로를 향한 응원의 온기가 정령의 전투력을 크게 높여주고 있습니다!"
        return "🌿 작은 실천이 모여 정령을 한층 더 든든하게 만듭니다. 오늘도 잘하고 계셔요!"

if __name__ == "__main__":
    test_members = [
        {"steps": 7500, "workout_min": 45, "clean_meals": 3, "streak_days": 5, "cheers_sent": 2},
        {"steps": 10200, "workout_min": 30, "clean_meals": 2, "streak_days": 12, "cheers_sent": 4},
    ]
    engine = GuildSynergyEngine()
    result = engine.calculate_guild_synergy(test_members)
    print(f"[Guild Synergy Engine Output] {result}")