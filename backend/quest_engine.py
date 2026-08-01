"""Dynamic quest engine."""
from __future__ import annotations

import math
import random
from typing import Any, Dict, List


class DynamicQuestEngine:
    def __init__(self) -> None:
        self.default_quests = [
            {"id": "q_meal", "title": "건강한 식단 2회 기록", "category": "meal", "base_exp": 40, "target": 2},
            {"id": "q_workout", "title": "오늘 운동 30분 달성", "category": "workout", "base_exp": 60, "target": 30},
            {"id": "q_water", "title": "수분 1.5L 이상 섭취", "category": "water", "base_exp": 30, "target": 1.5},
        ]

    def get_daily_quests(self, streak_days: int = 1) -> List[Dict[str, Any]]:
        quests: List[Dict[str, Any]] = []
        for quest in self.default_quests:
            reward = self._calculate_quest_exp(quest["base_exp"], streak_days)
            quests.append(
                {
                    "quest_id": quest["id"],
                    "title": quest["title"],
                    "category": quest["category"],
                    "target_value": quest["target"],
                    "reward_exp": reward["exp"],
                    "exp_detail": reward["detail"],
                    "is_completed": False,
                }
            )
        return quests

    def _calculate_quest_exp(self, base_exp: int, streak_days: int) -> Dict[str, Any]:
        streak_bonus = min(streak_days * 0.03, 0.30)
        variance = random.choice([-0.05, 0.0, 0.05, 0.10])
        final_exp = math.floor(base_exp * (1.0 + streak_bonus + variance))
        return {"exp": final_exp, "detail": f"기본 {base_exp} + 연속 달성({int(streak_bonus * 100)}%)"}
