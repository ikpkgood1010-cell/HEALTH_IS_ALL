"""
File Path: HEALTH IS ALL/03_BACKEND/dynamic_health_engine_v4.py
Description: 다변화된 수식과 엔트로피 팩터를 적용한 동적 건강/RPG 계산 엔진 V4
"""

import random
import math

class DynamicHealthEngineV4:
    def __init__(self):
        self.version = "4.0"
        
    def calculate_gained_exp(self, duration_min: float, intensity_level: int, streak_days: int) -> float:
        """
        운동 시간, 강도, 연속 달성일에 엔트로피 팩터를 적용하여 매번 다른 보상 산출
        """
        base_score = duration_min * intensity_level * 10.0
        streak_multiplier = 1.0 + (min(streak_days, 30) * 0.02)
        
        # -3% ~ +3% 사이의 미세한 변동치 부여 (단조로움 방지)
        entropy_factor = random.uniform(0.97, 1.03)
        
        total_exp = base_score * streak_multiplier * entropy_factor
        return round(total_exp, 2)

    def calculate_nutrition_penalty(self, sugar_intake: float, fried_intake: float) -> int:
        """
        철저한 식단 관리(당, 밀가루, 튀긴 음식 배제) 기준 위반 시 패널티 계산
        """
        penalty = (sugar_intake * 1.5) + (fried_intake * 2.0)
        return int(math.ceil(penalty))

if __name__ == "__main__":
    engine = DynamicHealthEngineV4()
    print(f"DynamicHealthEngine V{engine.version} initialized successfully.")