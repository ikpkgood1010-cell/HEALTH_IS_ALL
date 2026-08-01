"""Workout calories and reward calculation."""
from __future__ import annotations

import math
from typing import Any, Dict, Optional

from backend.config import utc_now


class DynamicHealthCalculator:
    def __init__(self) -> None:
        self.met_table = {
            "walking": 3.8,
            "running": 8.0,
            "cycling": 6.8,
            "swimming": 7.0,
            "strength_training": 5.0,
            "hiking": 6.5,
        }

    def calculate_workout_calories(
        self,
        workout_type: str,
        duration_minutes: float,
        weight_kg: float,
        intensity: str = "moderate",
        heart_rate_avg: Optional[int] = None,
    ) -> float:
        try:
            base_met = self.met_table.get(workout_type.lower(), 4.0)
            intensity_multiplier = {
                "light": 0.85,
                "moderate": 1.0,
                "vigorous": 1.25,
                "extreme": 1.4,
            }.get(intensity.lower(), 1.0)
            heart_rate_factor = 1.0
            if heart_rate_avg and heart_rate_avg > 0:
                heart_rate_factor = min(max(heart_rate_avg / 130.0, 0.8), 1.3)
            current_hour = utc_now().hour
            circadian_factor = 1.03 if 14 <= current_hour <= 18 else 0.97
            duration_hours = duration_minutes / 60.0
            calories = base_met * weight_kg * duration_hours * intensity_multiplier * heart_rate_factor * circadian_factor
            return round(calories, 1)
        except Exception:
            return round(4.0 * weight_kg * (duration_minutes / 60.0), 1)

    def calculate_activity_reward(
        self,
        record_type: str,
        raw_value: float,
        weight_kg: float = 70.0,
        streak_days: int = 1,
    ) -> Dict[str, Any]:
        base_exp_map = {"meal_log": 30, "workout_log": 50, "habit_complete": 20}
        base_exp = base_exp_map.get(record_type, 15)
        streak_bonus = min(streak_days * 0.02, 0.20)
        second_variance = (utc_now().second % 7 - 3) * 0.01
        dynamic_factor = 1.0 + streak_bonus + second_variance
        calculated_exp = math.floor(base_exp * dynamic_factor)
        return {
            "calculated_exp": calculated_exp,
            "dynamic_factor": round(dynamic_factor, 3),
            "detail_summary": f"기본 {base_exp} Exp + 연속 달성 보너스({int(streak_bonus * 100)}%)",
            "raw_value": raw_value,
            "weight_kg": weight_kg,
        }
