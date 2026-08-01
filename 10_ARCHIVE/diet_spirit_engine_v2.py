"""
Purpose: 클린 식단(당, 밀가루, 튀김 제외 및 찜 요리 선호 등)과 정령 성장 촉진을 연결하는 엔진 V2
Scope: Backend Diet-Spirit Catalyst Service
SSOT: HEALTH IS ALL/03_BACKEND/diet_spirit_engine_v2.py
"""

class DietSpiritEngineV2:
    def __init__(self):
        self.catalyst_multiplier = 1.25

    def evaluate_meal_for_spirit(self, meal_tags: list) -> dict:
        """
        식단 성격에 따른 정령 진화 촉진 지수 계산
        """
        clean_keywords = ["steamed", "steam", "sugar_free", "low_carb", "찜", "무가당"]
        clean_count = sum(1 for tag in meal_tags if tag.lower() in clean_keywords)
        
        catalyst_effect = clean_count * self.catalyst_multiplier
        
        return {
            "status": "success",
            "clean_score_boost": catalyst_effect,
            "spirit_evolution_ready": catalyst_effect >= 2.0
        }