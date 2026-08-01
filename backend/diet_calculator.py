"""Meal quality scoring utilities."""
from __future__ import annotations

from typing import Any, Dict

from backend.config import utc_now


class DynamicDietCalculator:
    def __init__(self) -> None:
        pass

    def analyze_meal_quality(
        self,
        calories: float,
        carbs: float = 0.0,
        protein: float = 0.0,
        fat: float = 0.0,
        fiber: float = 0.0,
        meal_time: str = "lunch",
    ) -> Dict[str, Any]:
        try:
            total_macro_cals = (carbs * 4.0) + (protein * 4.0) + (fat * 9.0)
            if total_macro_cals > 0:
                protein_ratio = (protein * 4.0) / total_macro_cals
            else:
                protein_ratio = 0.20

            protein_score = min(protein_ratio / 0.25, 1.2)
            current_hour = utc_now().hour
            night_penalty = 0.85 if current_hour >= 21 or current_hour <= 4 else 1.0
            satiety_factor = 1.0 + min(fiber * 0.02, 0.15)
            quality_score = round(min(80.0 * protein_score * night_penalty * satiety_factor, 100.0), 1)
            exp_modifier = round((quality_score - 70.0) / 100.0, 2)
            return {
                "quality_score": quality_score,
                "protein_ratio_pct": round(protein_ratio * 100, 1),
                "satiety_factor": round(satiety_factor, 2),
                "exp_modifier": exp_modifier,
                "is_night_meal": night_penalty < 1.0,
                "meal_time": meal_time,
                "calories": calories,
            }
        except Exception:
            return {
                "quality_score": 70.0,
                "protein_ratio_pct": 20.0,
                "satiety_factor": 1.0,
                "exp_modifier": 0.0,
                "is_night_meal": False,
                "meal_time": meal_time,
                "calories": calories,
            }
