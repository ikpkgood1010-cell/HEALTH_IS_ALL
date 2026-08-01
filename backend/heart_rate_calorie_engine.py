"""
HEALTH IS ALL - Heart Rate Dynamic Calorie Engine
Filename: heart_rate_calorie_engine.py
Path: HEALTH IS ALL/backend/heart_rate_calorie_engine.py
Purpose: 실시간 심박수 기반 동적 소모 칼로리(DAB) 및 정령 속성 에너지 전환 산출 백엔드 엔진
"""

import random
from typing import Dict, Any

class HeartRateCalorieEngine:
    """
    심박수 기반 정밀 칼로리 및 정령 속성 에너징 산출 엔진
    """

    @staticmethod
    def calculate_dynamic_burn(
        avg_hr: float,
        duration_minutes: float,
        user_age: int = 30,
        weight_kg: float = 68.0,
        gender: str = "MALE"
    ) -> Dict[str, Any]:
        """
        Keytel 공식을 응용한 정밀 칼로리 산출 및 정령 속성 경험치 전환
        """
        if duration_minutes <= 0 or avg_hr <= 0:
            return HeartRateCalorieEngine._build_fallback_calorie()

        jitter = random.uniform(0.96, 1.04)

        # 1. 성별 및 심박수 기반 Dynamic Active Burn (DAB) 계산 수식
        if gender.upper() == "MALE":
            raw_kcal = (
                (user_age * 0.2017) + (weight_kg * 0.1988) + (avg_hr * 0.6309) - 55.0969
            ) * (duration_minutes / 4.184)
        else:
            raw_kcal = (
                (user_age * 0.074) - (weight_kg * 0.1263) + (avg_hr * 0.4472) - 20.4022
            ) * (duration_minutes / 4.184)

        dab_kcal = round(max(0.0, raw_kcal * jitter), 1)

        # 2. 심박 구역에 따른 정령 속성 에너지 분배
        # Zone 1 (<110 BPM): 빛 속성 (회복/안정)
        # Zone 2 (110~140 BPM): 바람 속성 (유산소/지구력)
        # Zone 3 (>140 BPM): 불꽃 속성 (고강도/에너지 explosion)
        if avg_hr >= 140:
            primary_element = "FLAME"
            flame_energy = round(dab_kcal * 1.2, 1)
            wind_energy = round(dab_kcal * 0.3, 1)
            light_energy = 5.0
        elif avg_hr >= 110:
            primary_element = "WIND"
            flame_energy = round(dab_kcal * 0.4, 1)
            wind_energy = round(dab_kcal * 1.1, 1)
            light_energy = 15.0
        else:
            primary_element = "LIGHT"
            flame_energy = 5.0
            wind_energy = round(dab_kcal * 0.2, 1)
            light_energy = round(dab_kcal * 1.0, 1)

        # 3. 호감형 알림 문구
        message = (
            f"오늘 운동으로 {dab_kcal} kcal의 건강한 열량을 소모하셨어요! "
            f"정령에게 {primary_element} 속성의 에너지가 가득 채워졌습니다 ✨"
        )

        return {
            "dab_kcal": dab_kcal,
            "primary_element": primary_element,
            "flame_energy": flame_energy,
            "wind_energy": wind_energy,
            "light_energy": light_energy,
            "engine_message": message,
            "is_fallback": False
        }

    @staticmethod
    def _build_fallback_calorie() -> Dict[str, Any]:
        return {
            "dab_kcal": 120.5,
            "primary_element": "WIND",
            "flame_energy": 25.0,
            "wind_energy": 90.0,
            "light_energy": 15.0,
            "engine_message": "가볍고 정갈한 산책으로 바람의 정령이 살랑살랑 기뻐합니다 🌿",
            "is_fallback": True
        }

if __name__ == "__main__":
    engine = HeartRateCalorieEngine()
    res = engine.calculate_dynamic_burn(avg_hr=132, duration_minutes=35, user_age=31, weight_kg=70.0)
    print(f"[Heart Rate Calorie Engine Output] {res}")