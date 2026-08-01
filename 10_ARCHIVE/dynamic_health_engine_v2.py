"""
Purpose: 다중 변수를 활용한 정밀 건강 점수 및 칼로리 동적 계산 엔진 V2
Scope: Backend Engine Calculation Service
SSOT: HEALTH IS ALL/03_BACKEND/dynamic_health_engine_v2.py
"""

import math
import random

class DynamicHealthEngineV2:
    def __init__(self):
        self.version = "2.0"

    def calculate_dynamic_score(self, base_cal: float, sleep_efficiency: float, diet_cleanliness: float) -> dict:
        """
        매번 지루하지 않은 수치 제공을 위한 다중 변수 동적 계산식 적용
        """
        try:
            # 미세한 무작위 변동 변수 추가 (지루함 방지, ±1.5%)
            random_variance = random.uniform(0.985, 1.015)
            
            # 시너지 계산
            synergy_bonus = 1.05 if diet_cleanliness >= 0.9 else 1.0
            
            calculated_score = ((base_cal * 0.4) + (sleep_efficiency * 0.3) + (diet_cleanliness * 100 * 0.3)) * random_variance * synergy_bonus
            
            return {
                "status": "success",
                "version": self.version,
                "final_score": round(calculated_score, 2),
                "applied_variance": round(random_variance, 4)
            }
        except ZeroDivisionError as e:
            return {
                "status": "fallback",
                "error": str(e),
                "final_score": base_cal * 0.5  # 간결한 백업 공식
            }

if __name__ == "__main__":
    engine = DynamicHealthEngineV2()
    print(engine.calculate_dynamic_score(500, 85.0, 0.95))