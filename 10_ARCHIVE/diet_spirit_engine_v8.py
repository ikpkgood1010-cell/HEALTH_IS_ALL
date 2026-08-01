"""
HEALTH IS ALL - Diet Spirit Engine V8
식단 영양 성분(대체당, 정제당, 단백질비율) 정밀 분석 및 정령 친밀도/감정 상태 계산 엔진
"""

import logging
from typing import Dict, Any

logger = logging.getLogger("DietSpiritEngineV8")

class DietSpiritEngineV8:
    def __init__(self):
        self.version = "8.0.0"

    def evaluate_diet_for_spirit(
        self,
        protein_g: float,
        sugar_g: float,
        sugar_substitute_g: float,
        is_steamed_or_healthy_cook: bool = True
    ) -> Dict[str, Any]:
        """
        식단 구성을 분석하여 정령 성장 포인트 및 감정 상태 반환
        """
        try:
            # 기본 점수 산출 (단백질 + 보너스)
            base_score = protein_g * 2.0
            
            # 정제당 감점 및 대체당 가점 수식
            sugar_penalty = sugar_g * 1.5
            substitute_bonus = sugar_substitute_g * 1.2
            
            # 찌기/건강 조리법 가수치
            cooking_multiplier = 1.25 if is_steamed_or_healthy_cook else 1.0
            
            total_affinity = (base_score - sugar_penalty + substitute_bonus) * cooking_multiplier
            total_affinity = max(round(total_affinity, 2), 0.0) # 음수 방지

            # 정령 반응 결정
            if total_affinity >= 50.0:
                spirit_emotion = "DELIGHTED"
                dialogue = "정말 건강하고 훌륭한 식단이에요! 기운이 솟아나요!"
            elif total_affinity >= 20.0:
                spirit_emotion = "HAPPY"
                dialogue = "좋은 영양분이에요! 꾸준히 함께해 볼까요?"
            else:
                spirit_emotion = "NEUTRAL"
                dialogue = "다음엔 정제당을 조금 줄이고 건강한 재료로 채워봐요!"

            return {
                "spirit_affinity_gained": total_affinity,
                "spirit_emotion": spirit_emotion,
                "companion_dialogue": dialogue,
                "status": "SUCCESS"
            }
        except Exception as e:
            logger.error(f"식단 정령 연산 에러: {e}")
            return {
                "spirit_affinity_gained": 10.0,
                "spirit_emotion": "NEUTRAL",
                "companion_dialogue": "식단 기록을 완료했어요! 차근차근 시작해 봐요.",
                "status": "FALLBACK"
            }

if __name__ == "__main__":
    engine = DietSpiritEngineV8()
    res = engine.evaluate_diet_for_spirit(protein_g=35.0, sugar_g=0.0, sugar_substitute_g=5.0, is_steamed_or_healthy_cook=True)
    print("식단 정령 분석 결과:", res)