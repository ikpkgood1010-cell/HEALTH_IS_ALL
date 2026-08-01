"""
HEALTH IS ALL - Dynamic Nutrition & Workout Quest Engine
Filename: nutrition_quest_engine.py
Path: HEALTH IS ALL/backend/nutrition_quest_engine.py
Purpose: 유저 신체 컨디션 수치 기반 동적 퀘스트 생성 및 보상 산출 백엔드 엔진
"""

import random
from typing import List, Dict, Any

class NutritionQuestEngine:
    """
    맞춤형 일일 건강 퀘스트 및 보상 엔진
    """

    @staticmethod
    def generate_daily_quests(
        recovery_score: float,
        streak_days: int = 1,
        spirit_affinity_lvl: int = 1
    ) -> Dict[str, Any]:
        """
        회복 지수($RS$)를 고려하여 안전하고 다채로운 일일 퀘스트 3종 추천
        """
        quests = []
        jitter = random.uniform(0.97, 1.03)

        # 보상 산출 배율 수식
        reward_multiplier = (1.0 + (streak_days * 0.03)) * (1.0 + (spirit_affinity_lvl * 0.015)) * jitter

        # 컨디션 저조 시 피로 방지 가벼운 퀘스트 발행
        if recovery_score < 40.0:
            quests.append({
                "quest_id": "Q_REST_01",
                "title": "🌿 정령과 함께 편안한 15분 산책하기",
                "category": "WORKOUT",
                "target_val": 3000,
                "unit": "걸음",
                "reward_gold": int(150 * reward_multiplier),
                "reward_affinity": int(20 * reward_multiplier)
            })
            quests.append({
                "quest_id": "Q_DIET_01",
                "title": "🥗 따뜻한 수분 및 채소 섭취 인증하기",
                "category": "NUTRITION",
                "target_val": 1,
                "unit": "회",
                "reward_gold": int(120 * reward_multiplier),
                "reward_affinity": int(15 * reward_multiplier)
            })
        else:
            quests.append({
                "quest_id": "Q_WORK_02",
                "title": "🏃‍♂️ 활력 넘치는 7,000보 달성하기",
                "category": "WORKOUT",
                "target_val": 7000,
                "unit": "걸음",
                "reward_gold": int(300 * reward_multiplier),
                "reward_affinity": int(35 * reward_multiplier)
            })
            quests.append({
                "quest_id": "Q_DIET_02",
                "title": "🥩 목표 단백질 밸런스 채우기",
                "category": "NUTRITION",
                "target_val": 1,
                "unit": "달성",
                "reward_gold": int(250 * reward_multiplier),
                "reward_affinity": int(30 * reward_multiplier)
            })

        # 공통 퀘스트: 정령 터치 응원
        quests.append({
            "quest_id": "Q_SPIRIT_01",
            "title": "✨ 정령 교감 팝업으로 따뜻한 응원 주고받기",
            "category": "INTERACTION",
            "target_val": 1,
            "unit": "회",
            "reward_gold": int(100 * reward_multiplier),
            "reward_affinity": int(25 * reward_multiplier)
        })

        friendly_greeting = (
            "오늘 몸 상태에 딱 맞춘 건강 미션이 도착했어요! 무리하지 말고 정령과 차근차근 함께해요 🌿"
            if recovery_score >= 40.0 else
            "오늘은 정령이 당신의 휴식을 진심으로 응원합니다. 가볍게 소화할 수 있는 퀘스트로 준비했어요 ☕"
        )

        return {
            "quests": quests,
            "friendly_greeting": friendly_greeting,
            "streak_bonus_pct": round((streak_days * 3.0), 1),
            "is_fallback": False
        }

if __name__ == "__main__":
    engine = NutritionQuestEngine()
    res = engine.generate_daily_quests(recovery_score=85.0, streak_days=5)
    print(f"[Nutrition Quest Engine Output] {res}")