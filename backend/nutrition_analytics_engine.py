"""
HEALTH IS ALL - Deep AI Nutrition Analytics Engine
Filename: nutrition_analytics_engine.py
Path: HEALTH IS ALL/backend/nutrition_analytics_engine.py
Purpose: 식단 데이터 분석, 미량 요소 결핍 탐지 및 클린 건강 레시피 추천 엔진
"""

import random
from typing import Dict, Any

class NutritionAnalyticsEngine:
    """
    AI 식단 영양 심화 분석 및 맞춤 레시피 추천 엔진
    """

    @staticmethod
    def analyze_nutrition_balance(
        target_kcal: float,
        consumed_kcal: float,
        protein_g: float,
        target_protein_g: float,
        fiber_g: float,
        target_fiber_g: float,
        water_ml: float
    ) -> Dict[str, Any]:
        """
        영양 섭취 데이터 분석 및 결핍 지수($NDI$) 산출
        """
        if target_kcal <= 0 or target_protein_g <= 0:
            return NutritionAnalyticsEngine._build_fallback_analytics()

        jitter = random.uniform(0.97, 1.03)

        # 1. 영양소 격차 계산
        p_gap = max(0.0, target_protein_g - protein_g)
        f_gap = max(0.0, target_fiber_g - fiber_g)

        # 2. 영양 결핍 지수 ($NDI$) 계산
        raw_ndi = (p_gap / target_protein_g) * 0.5 + (f_gap / target_fiber_g) * 0.5
        ndi = round(min(1.0, max(0.0, raw_ndi * jitter)), 2)

        # 3. 결핍 요소별 클린 레시피 필터링 매칭
        if p_gap > 15.0 and f_gap > 5.0:
            recipe_title = "🧅 양파 소고기 아삭 야채 찜"
            recipe_desc = "단백질과 식이섬유를 깔끔하게 담아낸 영양 만점 스팀 요리입니다."
        elif p_gap > 15.0:
            recipe_title = "🥩 담백한 돼지목살 양파 찜"
            recipe_desc = "부드럽게 스팀으로 익혀 기름기를 줄이고 단백질을 채우는 요리입니다."
        elif f_gap > 5.0:
            recipe_title = "🥗 파프리카 브로콜리 따뜻한 샐러드"
            recipe_desc = "비타민과 풍부한 식이섬유로 장 건강과 정령의 풀 속성을 다스립니다."
        else:
            recipe_title = "✨ 수채화 밸런스 균형 식단"
            recipe_desc = "오늘 섭취 밸런스가 아주 훌륭해요! 수분을 충분히 보충해 주세요."

        # 4. 정령 호감형 분석 가이드 문구
        if ndi < 0.2:
            spirit_advice = "완벽에 가까운 영양 밸런스예요! 정령의 빛 아우라가 가득 채워졌습니다 ✨"
        elif p_gap > f_gap:
            spirit_advice = "오늘 식단에 단백질을 조금 더 더해주시면 정령이 힘차게 불꽃을 피울 거예요 💪"
        else:
            spirit_advice = "싱그러운 야채와 수분을 조금 더 채워주시면 정령이 더욱 예쁜 싹을 틔울 거예요 🌿"

        return {
            "deficiency_index": ndi,
            "protein_gap_g": round(p_gap, 1),
            "fiber_gap_g": round(f_gap, 1),
            "recommended_recipe": recipe_title,
            "recipe_description": recipe_desc,
            "spirit_advice": spirit_advice,
            "is_fallback": False
        }

    @staticmethod
    def _build_fallback_analytics() -> Dict[str, Any]:
        return {
            "deficiency_index": 0.25,
            "protein_gap_g": 10.0,
            "fiber_gap_g": 4.0,
            "recommended_recipe": "🥩 담백한 돼지목살 양파 찜",
            "recipe_description": "자극적이지 않고 정갈하게 수분과 단백질을 챙기는 클린 식단입니다.",
            "spirit_advice": "오늘 식단을 따뜻하게 채워볼까요? 정령이 곁에서 응원하고 있어요 🌿",
            "is_fallback": True
        }

if __name__ == "__main__":
    engine = NutritionAnalyticsEngine()
    res = engine.analyze_nutrition_balance(
        target_kcal=2100, consumed_kcal=1850,
        protein_g=65.0, target_protein_g=95.0,
        fiber_g=14.0, target_fiber_g=25.0, water_ml=1500
    )
    print(f"[Nutrition Analytics Engine Output] {res}")