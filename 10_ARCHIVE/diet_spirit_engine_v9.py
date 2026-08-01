# 파일 경로: HEALTH IS ALL/03_BACKEND/diet_spirit_engine_v9.py
# 파일명: diet_spirit_engine_v9.py
# 설명: 식단-정령 성장의 촉매 시너지 계산 엔진 v9

import math
from typing import Dict, Any, List

class DietSpiritEngineV9:
    """
    HEALTH IS ALL - Diet & Spirit Growth Synergy Engine v9
    사용자의 식단 특성과 조리 방식, 영양 균형을 동적으로 분석하여
    정령의 속성 능력치 및 친밀도 포인트를 계산합니다.
    """

    def __init__(self):
        self.version = "9.0.0"

    def calculate_spirit_diet_synergy(
        self,
        meal_components: List[str],
        cooking_method: str, # e.g. "STEAM", "GRILL", "FRIED"
        has_sugar_substitute: bool,
        water_intake_ml: float,
        current_spirit_affinity: int
    ) -> Dict[str, Any]:
        """
        식단 요소와 조리법 기반 정령 촉매 시너지 수식 연산
        """
        try:
            # 1. 조리 방식별 가중치 (Cooking Factor)
            cooking_factor = 1.0
            if cooking_method.upper() in ["STEAM", "STEAMED"]:
                cooking_factor = 1.35  # 영양소 보존율이 높고 건강한 찜 요리 가중치
            elif cooking_method.upper() == "FRIED":
                cooking_factor = 0.8   # 튀김류 감점 가중치

            # 2. 대체당/무설탕 보너스 계수
            sugar_bonus = 1.2 if has_sugar_substitute else 1.0

            # 3. 수분 섭취 보정 수식 (Hydration Factor)
            hydration_factor = min(1.3, max(0.9, water_intake_ml / 2000.0))

            # 4. 정령 친밀도 및 성장 포인트 산출
            base_point = len(meal_components) * 20.0
            total_synergy_exp = base_point * cooking_factor * sugar_bonus * hydration_factor

            new_affinity = current_spirit_affinity + int(total_synergy_exp * 0.1)

            return {
                "status": "SUCCESS",
                "synergy_exp_gained": round(total_synergy_exp, 2),
                "updated_spirit_affinity": new_affinity,
                "cooking_factor_applied": cooking_factor,
                "formula_used": "DIET_SPIRIT_CATALYST_V9"
            }

        except Exception:
            # 연산 실패 시 간결 폴백 로직 작동
            return {
                "status": "FALLBACK_APPLIED",
                "synergy_exp_gained": 50.0,
                "updated_spirit_affinity": current_spirit_affinity + 5,
                "formula_used": "SIMPLE_DIET_FALLBACK_V1"
            }

if __name__ == "__main__":
    engine = DietSpiritEngineV9()
    result = engine.calculate_spirit_diet_synergy(
        meal_components=["돼지고기 목살", "양파", "버섯"],
        cooking_method="STEAM",
        has_sugar_substitute=True,
        water_intake_ml=1800,
        current_spirit_affinity=120
    )
    print("Diet Spirit Engine V9 Result:", result)