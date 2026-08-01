"""
HEALTH IS ALL - Social Guild Challenge Engine
Filename: guild_challenge_engine.py
Path: HEALTH IS ALL/backend/guild_challenge_engine.py
Purpose: 길드원 활동 데이터 집계, 개인 기여도 계산 및 길드 수호 정령 진화 판정 엔진
"""

import random
from typing import List, Dict, Any

class GuildChallengeEngine:
    """
    길드 챌린지 및 수호 정령 거대진화 엔진
    """

    GUARDIAN_STAGES = [
        "BABY_GUARD",     # 1단계: 귀여운 수호 정령
        "SKY_WARDEN",     # 2단계: 하늘의 파수꾼
        "COSMIC_AEGIS",   # 3단계: 은하의 방패
        "IMMORTAL_SPIRIT" # 4단계: 불멸의 신화 정령
    ]

    @staticmethod
    def calculate_guild_progress(
        member_activities: List[Dict[str, Any]],
        guild_target_steps: int = 50000,
        current_guild_exp: float = 0.0
    ) -> Dict[str, Any]:
        """
        길드원 활동 합산, 개인 기여도 계산 및 길드 정령 진화 상태 도출
        """
        if not member_activities:
            return GuildChallengeEngine._build_fallback_guild()

        jitter = random.uniform(0.96, 1.04)
        total_steps = 0
        total_contribution_exp = 0.0
        member_results = []

        for member in member_activities:
            # 안전장치: 개인 걸음 수 15,000보 캡 적용
            capped_steps = min(15000, member.get("steps", 0))
            nutri_score = member.get("nutri_balance_score", 70.0)
            streak = member.get("streak_days", 1)

            # 개인 기여 점수 수식
            contrib_score = (
                (capped_steps / 1000.0) * 15.0 + (nutri_score * 0.8)
            ) * (1.0 + (streak * 0.02)) * jitter

            total_steps += capped_steps
            total_contribution_exp += contrib_score

            member_results.append({
                "user_id": member.get("user_id", "UNKNOWN"),
                "user_name": member.get("user_name", "길드원"),
                "contribution_score": round(contrib_score, 1),
                "steps": capped_steps
            })

        # 새로운 길드 누적 경험치
        new_guild_exp = current_guild_exp + total_contribution_exp
        achievement_rate = min(100.0, (total_steps / max(1, guild_target_steps)) * 100.0)

        # 수호 정령 단계 판정 (1000 exp 당 1단계 상승)
        stage_idx = min(3, int(new_guild_exp // 1000))
        guardian_stage = GuildChallengeEngine.GUARDIAN_STAGES[stage_idx]

        # 다정한 호감형 길드 메시지 생성
        friendly_message = (
            f"오늘 길드원들과 함께 총 {total_steps:,}보를 모으셨어요! "
            f"수호 정령이 든든한 온기를 머금고 성장 중입니다 ✨"
        )

        return {
            "total_guild_steps": total_steps,
            "guild_target_steps": guild_target_steps,
            "achievement_rate_pct": round(achievement_rate, 1),
            "guild_exp": round(new_guild_exp, 1),
            "guardian_stage": guardian_stage,
            "member_contributions": member_results,
            "friendly_message": friendly_message,
            "is_fallback": False
        }

    @staticmethod
    def _build_fallback_guild() -> Dict[str, Any]:
        return {
            "total_guild_steps": 12000,
            "guild_target_steps": 30000,
            "achievement_rate_pct": 40.0,
            "guild_exp": 450.0,
            "guardian_stage": "BABY_GUARD",
            "member_contributions": [],
            "friendly_message": "AI 서포터 정령이 길드원들과 함께 따뜻하게 걸음을 모으고 있어요 🌿",
            "is_fallback": True
        }

if __name__ == "__main__":
    engine = GuildChallengeEngine()
    dummy_members = [
        {"user_id": "U1", "user_name": "민우", "steps": 8500, "nutri_balance_score": 88.0, "streak_days": 4},
        {"user_id": "U2", "user_name": "지현", "steps": 10200, "nutri_balance_score": 92.0, "streak_days": 7}
    ]
    res = engine.calculate_guild_progress(dummy_members, guild_target_steps=20000)
    print(f"[Guild Challenge Engine Output] {res}")