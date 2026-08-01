# [중복문서-덮어쓰기, 교체] Diet Spirit Engine V3
class DietSpiritEngineV3:
    """
    Purpose: 사용자의 건강한 식단 기록을 정령의 성장 에너지로 변환하는 백엔드 엔진.
    Scope: 식단-정령 시너지 및 성장치 계산.
    SSOT: 식단 기반 정령 성장 로직의 표준.
    """

    @staticmethod
    def calculate_spirit_exp_gain(clean_diet_score: float, workout_intensity: float) -> int:
        # 식단 점수와 운동 강도를 복합 반영한 정령 경험치 산출
        base_exp = int(clean_diet_score * 1.5)
        intensity_multiplier = 1.0 + (workout_intensity * 0.1)
        total_exp = int(base_exp * intensity_multiplier)
        return max(total_exp, 10)

    @staticmethod
    def check_evolution_milestone(current_exp: int, current_tier: int) -> bool:
        required_exp = current_tier * 1000
        return current_exp >= required_exp

# Related Documents:
# - HEALTH IS ALL/03_GAME_SYSTEM/SPIRIT_EVOLUTION_EXPANSION_SPEC.md
# Change History:
# - v3.0 (2026-07-31): 복합 경험치 산출 및 진화 마일스톤 로직 고도화