"""
Purpose: 영양 섭취 데이터를 바탕으로 정령의 성장 및 기분 상태를 연산하고 식단-정령 시너지를 제공하는 v10 백엔드 엔진.
Scope: 식단 영양 분석 및 정령 성장 경험치 연산.
SSOT: HEALTH IS ALL/03_BACKEND/diet_spirit_engine_v10.py
Related Documents: HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V8.md
Change History: 2026-07-31 (v10.0) - 식단 다변수 정밀 경험치 수식 및 예외 대처 구현.
"""

from typing import Dict, Any

class DietSpiritEngineV10:
    def __init__(self):
        self.version = "10.0.0"

    def process_diet_synergy(self, diet_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Purpose: 식단 데이터를 기반으로 정령 시너지 및 성장 경험치를 연산함.
        """
        try:
            calories = float(diet_data.get('calories', 0))
            protein = float(diet_data.get('protein', 0))
            carbs = float(diet_data.get('carbs', 0))
            fat = float(diet_data.get('fat', 0))
            veggie_ratio = float(diet_data.get('veggie_ratio', 0.0))

            if calories <= 0:
                raise ValueError("Calories must be greater than zero.")

            # 세분화된 단백질/탄수화물/지방 균형 가중치
            p_ratio = (protein * 4) / calories
            c_ratio = (carbs * 4) / calories
            f_ratio = (fat * 9) / calories

            # 균형도 다변수 연산
            balance_penalty = abs(p_ratio - 0.3) + abs(c_ratio - 0.5) + abs(f_ratio - 0.2)
            synergy_multiplier = max(0.5, 1.5 - balance_penalty) + (veggie_ratio * 0.3)

            base_exp = (calories / 50.0)
            earned_exp = round(base_exp * synergy_multiplier, 2)

            return {
                "status": "SUCCESS",
                "tier": "Tier-2 Dynamic",
                "earned_exp": earned_exp,
                "spirit_mood": "HAPPY" if synergy_multiplier >= 1.2 else "NORMAL",
                "synergy_multiplier": round(synergy_multiplier, 2)
            }
        except Exception as e:
            # 에러 발생 시 간결한 1단계 계산식으로 전환
            return self._fallback_simple_exp(diet_data, str(e))

    def _fallback_simple_exp(self, diet_data: Dict[str, Any], error_reason: str) -> Dict[str, Any]:
        """
        1단계 간결한 계산식 (Fallback Tier-1)
        """
        calories = float(diet_data.get('calories', 0))
        simple_exp = round(calories / 50.0, 2) if calories > 0 else 10.0

        return {
            "status": "FALLBACK_SUCCESS",
            "tier": "Tier-1 Simple",
            "earned_exp": simple_exp,
            "spirit_mood": "NORMAL",
            "fallback_reason": error_reason
        }

if __name__ == "__main__":
    engine = DietSpiritEngineV10()
    print("Diet Engine Result:", engine.process_diet_synergy({"calories": 600, "protein": 35, "carbs": 60, "fat": 15, "veggie_ratio": 0.4}))