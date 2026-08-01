# 파일 저장 경로: HEALTH IS ALL/03_BACKEND/diet_spirit_engine_v6.py
# SSOT: HEALTH IS ALL/03_BACKEND/diet_spirit_engine_v6.py
# Related Documents: HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V6_SPEC.md
# Change History: V5 -> V6 (영양소 다변수 촉매 반응 및 2중 폴백 추가)

import math
from typing import Dict, Any

class DietSpiritEngineV6:
    """
    V6 정령 식단 촉매 연산 백엔드 엔진
    건강 목적을 최우선으로 하되 정령 반응 시각화를 유기적으로 계산
    """
    
    def __init__(self):
        self.version = "6.0.0"

    def calculate_catalyst_effect(self, meal_data: Dict[str, Any], spirit_affinity: float) -> Dict[str, Any]:
        """
        식단 영양소 기반 정령 시너지 및 성장 경험치 계산 (폴백 안전장치 포함)
        """
        try:
            calories = float(meal_data.get("calories", 0))
            carbs = float(meal_data.get("carbs", 0))
            protein = float(meal_data.get("protein", 0))
            fat = float(meal_data.get("fat", 0))
            
            if calories <= 0:
                return self._fallback_response("칼로리 입력값 0 이하")

            # 영양소 균형 점수 연산 (탄 50%, 단 30%, 지 20% 최적 기준)
            p_ratio = (protein * 4) / calories if calories > 0 else 0
            c_ratio = (carbs * 4) / calories if calories > 0 else 0
            f_ratio = (fat * 9) / calories if calories > 0 else 0
            
            balance_score = 1.0 - (abs(0.3 - p_ratio) + abs(0.5 - c_ratio) + abs(0.2 - f_ratio))
            balance_score = max(0.1, min(1.0, balance_score))

            # 동적 정령 변수 (매번 정체되지 않는 변동 보상)
            dynamic_factor = 1.0 + 0.1 * math.sin(calories / 100.0)
            exp_gained = int(calories * 0.1 * balance_score * (1.0 + spirit_affinity * 0.05) * dynamic_factor)

            return {
                "status": "SUCCESS",
                "engine_version": self.version,
                "balance_score": round(balance_score, 2),
                "exp_gained": exp_gained,
                "spirit_reaction": "HAPPY" if balance_score > 0.7 else "NEUTRAL",
                "message": "영양 균형이 훌륭하여 정령이 크게 성장했습니다!" if balance_score > 0.7 else "균형 잡힌 식단에 한 걸음 다가서 보세요!"
            }

        except Exception as e:
            return self._fallback_response(str(e))

    def _fallback_response(self, reason: str) -> Dict[str, Any]:
        """예외 발생 시 시스템 안정을 위한 안전 폴백 연산"""
        return {
            "status": "FALLBACK",
            "engine_version": self.version,
            "balance_score": 0.5,
            "exp_gained": 10,
            "spirit_reaction": "CALM",
            "message": "기본 식단 정보가 기록되었습니다.",
            "fallback_reason": reason
        }