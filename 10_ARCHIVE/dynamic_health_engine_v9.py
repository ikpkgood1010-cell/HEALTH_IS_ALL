# 파일 경로: HEALTH IS ALL/03_BACKEND/dynamic_health_engine_v9.py
# 파일명: dynamic_health_engine_v9.py
# 설명: 다변수 기반 동적 건강/영양/칼로리 계산 백엔드 엔진 v9

import math
import random
from typing import Dict, Any

class DynamicHealthEngineV9:
    """
    HEALTH IS ALL - Dynamic Variable Calculation Engine v9
    사용자 생체 변수, 시간대 변수, 심박 지표를 종합하여 
    매번 유기적으로 변화하는 정밀 건강/게임 지표를 산출합니다.
    """

    def __init__(self):
        self.version = "9.0.0"

    def calculate_dynamic_energy_expenditure(
        self,
        base_metabolic_rate: float,
        activity_duration_minutes: float,
        avg_heart_rate: float,
        resting_heart_rate: float,
        time_of_day_hour: int,
        stress_score: float = 50.0
    ) -> Dict[str, Any]:
        """
        활동 소비 칼로리 및 정령 에너지 다변수 산출 로직
        """
        try:
            # 1. 심박수 변동 및 강도 가중치 (HR Ratio)
            hr_ratio = max(1.0, avg_heart_rate / max(1.0, resting_heart_rate))
            hr_intensity_factor = math.pow(hr_ratio, 1.25)

            # 2. 시간대 생체 주기 가중치 (Circadian Rhythm Multiplier)
            circadian_factor = 1.0 + 0.08 * math.sin((time_of_day_hour - 6) * math.pi / 12)

            # 3. 스트레스/피로도 미세 보정 변수 (Noise Matrix)
            stress_modifier = 1.0 - ((stress_score - 50.0) / 500.0)
            micro_variance = random.uniform(0.97, 1.03)

            # 4. 종합 동적 소비 칼로리 연산
            base_expenditure = (base_metabolic_rate / 1440.0) * activity_duration_minutes
            dynamic_calories = (
                base_expenditure * 
                hr_intensity_factor * 
                circadian_factor * 
                stress_modifier * 
                micro_variance
            )

            # 5. 게임 전환 포인트 (Game Spirit Vitality)
            spirit_exp = round(dynamic_calories * 1.5 + (activity_duration_minutes * 0.8))

            return {
                "status": "SUCCESS",
                "calculated_calories": round(dynamic_calories, 2),
                "spirit_exp_gained": spirit_exp,
                "circadian_factor": round(circadian_factor, 3),
                "formula_used": "DYNAMIC_MULTI_VARIABLE_V9"
            }

        except Exception as e:
            # 충돌 또는 오류 발생 시 안정적인 1단계 간결 폴백 수식으로 전환
            return self._fallback_expenditure_calculation(
                base_metabolic_rate, activity_duration_minutes
            )

    def _fallback_expenditure_calculation(
        self, 
        bmr: float, 
        duration: float
    ) -> Dict[str, Any]:
        """안정성 보장을 위한 1단계 폴백 간결 계산식"""
        simple_calories = (bmr / 1440.0) * duration * 3.5
        return {
            "status": "FALLBACK_APPLIED",
            "calculated_calories": round(simple_calories, 2),
            "spirit_exp_gained": int(simple_calories),
            "formula_used": "SIMPLE_FALLBACK_V1"
        }

if __name__ == "__main__":
    engine = DynamicHealthEngineV9()
    res = engine.calculate_dynamic_energy_expenditure(
        base_metabolic_rate=1650.0,
        activity_duration_minutes=45,
        avg_heart_rate=135,
        resting_heart_rate=65,
        time_of_day_hour=14
    )
    print("Engine V9 Result:", res)