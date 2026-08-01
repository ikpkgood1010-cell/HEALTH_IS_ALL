"""Sleep quality and habit reward calculation."""
from __future__ import annotations

import math
from typing import Any, Dict


class DynamicHabitSleepCalculator:
    def __init__(self) -> None:
        pass

    def calculate_sleep_quality(
        self,
        sleep_hours: float,
        target_hours: float = 7.5,
        bedtime_hour: int = 23,
        streak_days: int = 1,
    ) -> Dict[str, Any]:
        try:
            duration_ratio = min(sleep_hours / max(target_hours, 1.0), 1.2)
            duration_score = duration_ratio * 41.67
            if 22 <= bedtime_hour or bedtime_hour <= 1:
                circadian_score = 30.0
            elif 2 <= bedtime_hour <= 3:
                circadian_score = 20.0
            else:
                circadian_score = 10.0
            streak_score = min(streak_days * 2.0, 20.0)
            total_score = round(min(duration_score + circadian_score + streak_score, 100.0), 1)
            base_exp = 30
            calculated_exp = math.floor(base_exp * (total_score / 100.0))
            return {
                "sleep_score": total_score,
                "calculated_exp": max(calculated_exp, 10),
                "duration_ratio_pct": round(duration_ratio * 100, 1),
                "summary": f"수면 점수 {total_score}점 -> {max(calculated_exp, 10)} Exp",
            }
        except Exception:
            return {
                "sleep_score": 75.0,
                "calculated_exp": 25,
                "duration_ratio_pct": 100.0,
                "summary": "기본 수면 기록 수용 -> 25 Exp",
            }

    def calculate_habit_exp(self, habit_difficulty: str = "medium", streak_days: int = 1) -> int:
        try:
            diff_multiplier = {"easy": 0.8, "medium": 1.0, "hard": 1.3}.get(habit_difficulty.lower(), 1.0)
            streak_bonus = min(streak_days * 0.02, 0.20)
            return math.floor(20 * diff_multiplier * (1.0 + streak_bonus))
        except Exception:
            return 20
