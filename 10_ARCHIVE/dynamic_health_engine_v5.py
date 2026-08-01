"""
HEALTH IS ALL - Dynamic Health Engine v5
Dynamic multi-variable health, calorie, and recovery calculation engine with Fallback logic.
"""

from typing import Dict, Any, Optional
import math
import logging

logger = logging.getLogger("DynamicHealthEngineV5")

class DynamicHealthEngineV5:
    """
    정밀 건강 지표 계산 및 Fallback 안전장치를 탑재한 v5 백엔드 엔진
    """

    @staticmethod
    def calculate_bmr_mifflin_st_jeor(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
        """기본 Mifflin-St Jeor BMR 계산식"""
        gender_offset = 5 if gender.lower() in ['male', 'm', '남성'] else -161
        return (10.0 * weight_kg) + (6.25 * height_cm) - (5.0 * age) + gender_offset

    @classmethod
    def calculate_precision_tdee(
        cls,
        weight_kg: float,
        height_cm: float,
        age: int,
        gender: str,
        daily_steps: int,
        active_workout_minutes: int,
        hrv_ms: Optional[float] = None,
        baseline_hrv_ms: Optional[float] = None,
        sleep_quality_score: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        다변수 정밀 TDEE 및 회복 지수 계산
        센서 미비 시 Fallback Level 1 적용
        """
        try:
            # 1. Base BMR
            bmr = cls.calculate_bmr_mifflin_st_jeor(weight_kg, height_cm, age, gender)

            # 2. Activity Multiplier
            step_factor = min(daily_steps / 10000.0, 1.5) * 0.35
            workout_factor = (active_workout_minutes / 60.0) * 0.25
            activity_multiplier = 1.2 + step_factor + workout_factor

            # 3. Dynamic Recovery Factor (HRV & Sleep)
            is_fallback = False
            recovery_factor = 1.0

            if hrv_ms and baseline_hrv_ms and baseline_hrv_ms > 0:
                hrv_ratio = hrv_ms / baseline_hrv_ms
                recovery_factor *= max(0.85, min(1.15, hrv_ratio))
            else:
                is_fallback = True

            if sleep_quality_score is not None:
                # sleep_quality_score 0~100 -> 0.9 ~ 1.1
                sleep_factor = 0.9 + (max(0.0, min(100.0, sleep_quality_score)) / 100.0) * 0.2
                recovery_factor *= sleep_factor

            # Final Calculation
            final_tdee = bmr * activity_multiplier * recovery_factor

            return {
                "status": "SUCCESS",
                "mode": "FALLBACK_LEVEL_1" if is_fallback else "PRECISION_MODE",
                "bmr": round(bmr, 2),
                "tdee": round(final_tdee, 2),
                "activity_multiplier": round(activity_multiplier, 3),
                "recovery_factor": round(recovery_factor, 3),
                "health_score_bonus": round((recovery_factor - 1.0) * 100, 1)
            }

        except Exception as e:
            logger.error(f"Precision TDEE Calculation failed: {str(e)}. Falling back to basic formula.")
            # Fallback Level 1 Graceful Recovery
            fallback_bmr = cls.calculate_bmr_mifflin_st_jeor(weight_kg, height_cm, age, gender)
            return {
                "status": "FALLBACK_SUCCESS",
                "mode": "FALLBACK_LEVEL_1",
                "bmr": round(fallback_bmr, 2),
                "tdee": round(fallback_bmr * 1.375, 2),
                "activity_multiplier": 1.375,
                "recovery_factor": 1.0,
                "health_score_bonus": 0.0
            }

    @staticmethod
    def calculate_water_intake_target(weight_kg: float, workout_minutes: int) -> float:
        """권장 수분 섭취량(L) 동적 계산식"""
        base_water_liters = weight_kg * 0.033
        workout_extra_liters = (workout_minutes / 30.0) * 0.35
        return round(base_water_liters + workout_extra_liters, 2)