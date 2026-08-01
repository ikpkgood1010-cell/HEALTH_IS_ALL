# [중복문서-덮어쓰기, 교체] Dynamic Health Engine V3
import random
from datetime import datetime

class DynamicHealthEngineV3:
    """
    Purpose: 사용자 건강 데이터와 게임 요소를 결합한 고정밀 다변수 계산 백엔드 엔진.
    Scope: 칼로리, 식단 점수, 정령 촉매 반응 속도 계산.
    SSOT: 건강 데이터 산출 알고리즘의 기준 구현체.
    """
    
    @staticmethod
    def calculate_adjusted_calorie(base_calorie: float, streak_days: int, fatigue_index: float) -> float:
        # 다변수 동적 계산식 적용 (단조로우름 방지)
        random_factor = random.uniform(0.95, 1.05)
        streak_bonus = min(streak_days * 0.015, 0.30) # 최대 30% 보너스
        adjusted = base_calorie * (1.0 + streak_bonus - (fatigue_index * 0.05)) * random_factor
        return round(max(adjusted, 0.0), 2)

    @staticmethod
    def evaluate_diet_cleanliness(sugar_free: bool, flour_free: bool, fried_free: bool, steamed_used: bool) -> dict:
        score = 0.0
        if sugar_free: score += 30.0
        if flour_free: score += 30.0
        if fried_free: score += 30.0
        if steamed_used: score += 10.0
        
        # 무작위 촉매 공명 효과 추가
        resonance_bonus = random.choice([0, 5, 10, 15])
        total_score = min(score + resonance_bonus, 100.0)
        
        return {
            "base_score": score,
            "resonance_bonus": resonance_bonus,
            "total_score": total_score,
            "evaluated_at": datetime.now().isoformat()
        }

# Related Documents:
# - HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V3.md
# Change History:
# - v3.0 (2026-07-31): 랜덤 가중치 및 식단 클린도 정밀 평가 함수 추가