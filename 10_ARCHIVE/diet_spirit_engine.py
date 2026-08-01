"""
HEALTH IS ALL - Dynamic Diet & Spirit Catalyst Engine
Filename: diet_spirit_engine.py
Path: HEALTH IS ALL/backend/diet_spirit_engine.py
Purpose: 식단 영양소 동적 평가 및 정령 성장 촉진제(Catalyst) 산출 백엔드 로직
"""

import math
import random
from typing import Dict, Any, Optional

class DietSpiritEngine:
    """
    영양소 정밀 평가 및 정령 게임 보상을 계산하는 동적 엔진
    """

    @staticmethod
    def evaluate_diet(
        calories: float,
        protein_g: float,
        carbs_g: float,
        fat_g: float,
        fiber_g: Optional[float] = None,
        added_sugar_g: Optional[float] = None,
        clean_streak: int = 0,
        spirit_affinity: int = 1
    ) -> Dict[str, Any]:
        """
        식단 영양 점수(NBS)와 정령 촉진제 보상 계산
        데이터 유무에 따라 Fallback 자동 전환
        """
        # 이상치 예외 처리 (Exception Rule)
        if calories <= 0 or calories > 3500:
            calories = 500.0
            protein_g, carbs_g, fat_g = 25.0, 60.0, 15.0

        is_fallback = (fiber_g is None or added_sugar_g is None)

        if not is_fallback:
            # 1. 정밀 수식 (Precision Formula)
            total_cal = max(calories, 1.0)
            protein_ratio = (protein_g * 4.0) / total_cal
            
            # 단백질 점수 (최대 40점)
            protein_score = min(40.0, protein_ratio * 150.0)
            
            # 식이섬유 점수 (목표 12g 기준, 최대 30점)
            fiber_score = min(30.0, (fiber_g / 12.0) * 30.0)
            
            # 기본 베이스 점수 (30점)
            base_nbs = protein_score + fiber_score + 30.0
            
            # 정제당 감점 (총 칼로리의 10% 초과 시 감점)
            sugar_ratio = (added_sugar_g * 4.0) / total_cal
            sugar_penalty = max(0.0, sugar_ratio - 0.10) * 120.0
            
            nbs = max(10.0, min(100.0, base_nbs - sugar_penalty))
        else:
            # 2. Fallback 간이 수식 (Caloric Ratio Only)
            total_cal = max(calories, 1.0)
            p_ratio = (protein_g * 4.0) / total_cal
            # 표준 단백질 비율(20%~30%) 접근 시 높은 점수
            nbs = min(90.0, max(30.0, 50.0 + (p_ratio * 100.0)))

        # 3. 정령 감정 상태(Spirit Mood) 확정
        if nbs >= 85:
            mood = "JOYFUL"
            mood_dialogue = "몸도 마음도 가벼워요! 정령 에센스가 넘쳐납니다!"
        elif nbs >= 65:
            mood = "SATISFIED"
            mood_dialogue = "깔끔한 영양 공급이군요. 순조롭게 성장을 시작합니다."
        elif nbs >= 40:
            mood = "SLUGGISH"
            mood_dialogue = "조금 더 신선한 식이섬유와 단백질이 필요한 느낌이에요..."
        else:
            mood = "DISTRESSED"
            mood_dialogue = "윽... 정제당이 너무 많아요. 에센스 에너지가 정체됩니다."

        # 4. 정령 성장 촉진제(Catalyst Essence) 및 EXP 동적 산출
        streak_bonus = 1.0 + math.log(1.0 + max(0, clean_streak)) * 0.08
        affinity_bonus = 1.0 + (spirit_affinity * 0.005)
        fluctuator = random.uniform(0.95, 1.05)  # 5% 변동성

        catalyst_gained = int((nbs * 1.8) * streak_bonus * affinity_bonus * fluctuator)
        exp_gained = int((nbs * 1.2) * streak_bonus * fluctuator)

        return {
            "nutrient_balance_score": round(nbs, 1),
            "spirit_mood": mood,
            "spirit_dialogue": mood_dialogue,
            "catalyst_gained": max(5, catalyst_gained),
            "exp_gained": max(10, exp_gained),
            "is_fallback_used": is_fallback,
            "streak_bonus_pct": round((streak_bonus - 1.0) * 100, 1)
        }

if __name__ == "__main__":
    # 백엔드 엔진 테스트
    engine = DietSpiritEngine()
    # 클린 식단 테스트
    res_clean = engine.evaluate_diet(
        calories=550, protein_g=35, carbs_g=50, fat_g=12,
        fiber_g=14, added_sugar_g=2, clean_streak=5, spirit_affinity=10
    )
    print(f"[Clean Diet Test] {res_clean}")