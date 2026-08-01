"""
HEALTH IS ALL - Diet Spirit Engine v5
Translates meal nutrition metrics into Spirit growth experience, affinity, and item drop rates.
"""

from typing import Dict, Any

class DietSpiritEngineV5:
    """
    영양 밸런스 및 클린 식단(정제당/튀김 제한 등) 입력을 게임 스피릿 시스템으로 변환하는 엔진
    """

    @classmethod
    def process_meal_for_spirit(
        cls,
        protein_g: float,
        carbs_g: float,
        fat_g: float,
        fiber_g: float = 0.0,
        sugar_g: float = 0.0,
        is_processed_flour: bool = False,
        is_fried_food: bool = False,
        is_alcohol: bool = False
    ) -> Dict[str, Any]:
        """
        식단 영양 성분별 스피릿 경험치 및 촉매 드랍 지수 계산
        """
        # 1. Base Calorie & Macro Ratio calculation
        total_calories = (protein_g * 4) + (carbs_g * 4) + (fat_g * 9)
        if total_calories <= 0:
            return {
                "spirit_exp": 0,
                "affinity_delta": 0,
                "catalyst_drop_rate": 0.0,
                "message": "식단 정보가 비어있습니다."
            }

        protein_ratio = (protein_g * 4) / total_calories
        
        # 2. Clean Meal Penalty & Bonus Factors
        clean_bonus = 1.0
        feedback_notes = []

        if is_alcohol:
            clean_bonus -= 0.5
            feedback_notes.append("음주로 인해 스피릿 활력 감소")
        if is_fried_food:
            clean_bonus -= 0.2
            feedback_notes.append("튀김류 섭취로 스피릿 방어력 저하")
        if is_processed_flour:
            clean_bonus -= 0.15
            feedback_notes.append("정제 밀가루 제한 권장")

        # 식이섬유 보상 및 당류 감점
        if fiber_g >= 8.0:
            clean_bonus += 0.15
            feedback_notes.append("풍부한 식이섬유로 스피릿 친밀도 상승!")
        if sugar_g > 25.0:
            clean_bonus -= 0.2
            feedback_notes.append("과도한 당류 섭취 주의")

        clean_bonus = max(0.2, min(1.8, clean_bonus))

        # 3. Spirit EXP & Affinity Delta Calculation
        base_exp = int(total_calories * 0.1)
        protein_synergy = 1.0 + (protein_ratio * 0.5)  # 단백질 비율 높을수록 가속
        
        final_spirit_exp = int(base_exp * protein_synergy * clean_bonus)
        affinity_delta = 2 if clean_bonus >= 1.0 else -1

        # 4. Catalyst Drop Rate Bonus
        catalyst_drop_rate = round(min(0.25, 0.05 * clean_bonus), 3)

        return {
            "status": "SUCCESS",
            "spirit_exp": final_spirit_exp,
            "affinity_delta": affinity_delta,
            "clean_bonus_factor": round(clean_bonus, 2),
            "catalyst_drop_rate": catalyst_drop_rate,
            "feedback": feedback_notes if feedback_notes else ["최상의 클린 식단입니다! 스피릿이 크게 성장합니다."]
        }