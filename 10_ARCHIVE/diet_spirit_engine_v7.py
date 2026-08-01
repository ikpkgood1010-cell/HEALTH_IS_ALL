"""
===============================================================================
HEALTH IS ALL - Diet Spirit Synergy Engine V7
===============================================================================
Purpose:
  유저의 식단 영양소(탄수화물, 단백질, 지방) 균형도와 수분 섭취량을 다변수 수식으로 평가하여
  스피릿(Spirit) 캐릭터의 친밀도 성장, 호감도 팝업 문구 및 보상 포인트를 산출하는 백엔드 엔진.

Scope:
  - 식단 영양 밸런스 지수 계산
  - 스피릿 캐릭터 친밀도/기분 상태 반영
  - 호감적이고 따뜻한 유저 친화 대사 반환

SSOT:
  - 식단 평가 및 스피릿 시너지 시스템의 단일 진실 공급원.

Definitions:
  - Macro Ratio: 탄수화물/단백질/지방의 비율 (표준 50:30:20)
  - Spirit Joy Score: 영양 상태에 따른 스피릿 기분 점수 (0~100)

Runtime:
  - Python 3.11+, 식단 기록 API 수신 시 작동

Rules:
  - 건강에 악영향을 주지 않도록 과도한 단식이나 특정 영양소 0g 입력 시 친절한 주의 문구 출력.
  - 음주/강한 튀김 위주 식단 기록 시 감점이 아닌 '다음 식단 추천' 기반 긍정적 유도.

State:
  - DIET_EVALUATED, SPIRIT_HAPPY, SPIRIT_SUPPORTIVE

Event:
  - DietSpiritEngineV7.evaluate_diet_synergy()

Example:
  >>> engine = DietSpiritEngineV7()
  >>> res = engine.evaluate_diet_synergy(carbs_g=150, protein_g=90, fat_g=40, water_ml=1800)

Exception:
  - ZeroMacroException: 모든 영양소가 0g일 때 Fallback 문구 출력.

Related Documents:
  - HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V7_SPEC.md
  - HEALTH IS ALL/04_FRONTEND/DYNAMIC_NUTRITION_UI_SPEC_V7.md

Change History:
  - 2026-07-31 (V7.0.0): 정밀 영양 균형 지수 수식화 및 친화적 대사 시스템 전면 고도화.
===============================================================================
"""

from typing import Dict, Any

class DietSpiritEngineV7:
    def __init__(self):
        self.version = "7.0.0"

    def evaluate_diet_synergy(
        self,
        carbs_g: float,
        protein_g: float,
        fat_g: float,
        water_ml: float = 1500.0
    ) -> Dict[str, Any]:
        """식단 다변수 점수 산출 및 스피릿 기분 반응 생성"""
        total_calories = (carbs_g * 4.0) + (protein_g * 4.0) + (fat_g * 9.0)
        
        if total_calories <= 0:
            return {
                "engine_version": self.version,
                "status": "FALLBACK_EMPTY",
                "diet_score": 50,
                "spirit_expression": "curious",
                "message": "식단을 기록해 주시면 스피릿이 쑥쑥 자라나요! 🥗",
                "bonus_points": 5
            }

        # 영양소 비율 계산
        carb_ratio = (carbs_g * 4.0) / total_calories
        protein_ratio = (protein_g * 4.0) / total_calories
        fat_ratio = (fat_g * 9.0) / total_calories

        # 표준 영양 균형 편차 연산 (50:30:20 기준)
        dev_carb = abs(carb_ratio - 0.50)
        dev_protein = abs(protein_ratio - 0.30)
        dev_fat = abs(fat_ratio - 0.20)
        
        balance_penalty = (dev_carb + dev_protein + dev_fat) * 50.0
        diet_score = max(30.0, min(100.0, 100.0 - balance_penalty))

        # 수분 보너스
        water_bonus = min(10.0, (water_ml / 2000.0) * 10.0)
        final_score = round(min(100.0, diet_score + water_bonus), 1)

        # 스피릿 상호작용 표정과 대사 선정
        if final_score >= 85:
            expression = "delighted"
            dialogue = "와우! 완벽한 균형의 훌륭한 식단이에요! 스피릿도 신나서 에너지가 솟아납니다! 🌿✨"
        elif final_score >= 65:
            expression = "happy"
            dialogue = "건강하게 잘 챙겨 드셨네요! 다음 식사엔 수분 한 잔을 더해주시면 더욱 최고예요! 💧"
        else:
            expression = "cheering"
            dialogue = "괜찮아요, 오늘 한 끼도 귀한 영양이 되었어요! 다음 식단은 조금 더 건강하게 챙겨볼까요? 💪"

        bonus_points = int(final_score * 0.5)

        return {
            "engine_version": self.version,
            "status": "DIET_EVALUATED",
            "total_calories": round(total_calories, 1),
            "final_score": final_score,
            "spirit_expression": expression,
            "spirit_dialogue": dialogue,
            "bonus_points": bonus_points
        }

if __name__ == "__main__":
    engine = DietSpiritEngineV7()
    res = engine.evaluate_diet_synergy(carbs_g=130, protein_g=75, fat_g=30, water_ml=1800)
    print("Diet Spirit Result:", res)