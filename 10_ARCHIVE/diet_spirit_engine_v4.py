"""
File Path: HEALTH IS ALL/03_BACKEND/diet_spirit_engine_v4.py
Description: 철저한 식단 준수(설탕/밀가루/튀김 배제)에 따라 정령의 진화와 촉매 작용을 관리하는 엔진 V4
"""

class DietSpiritEngineV4:
    def __init__(self):
        self.version = "4.0"

    def evaluate_catalyst_effect(self, sugar_free: bool, flour_free: bool, fried_free: bool, steam_meal_used: bool) -> int:
        """
        식단 원칙 준수 여부 및 건강식(찜 요리 등) 활용에 따른 정령 진화 포인트 산출
        """
        points = 0
        if sugar_free:
            points += 25
        if flour_free:
            points += 25
        if fried_free:
            points += 25
        if steam_meal_used:
            points += 25  # 건강한 조리법 우대 보너스
            
        return points

    def get_spirit_evolution_status(self, total_points: int) -> str:
        if total_points >= 100:
            return "Pristine Spirit (최상위 순수 진화 상태)"
        elif total_points >= 50:
            return "Balanced Spirit (안정적 성장 상태)"
        else:
            return "Developing Spirit (관리 필요 상태)"

if __name__ == "__main__":
    engine = DietSpiritEngineV4()
    sample_points = engine.evaluate_catalyst_effect(True, True, True, True)
    print(f"Diet Spirit Engine V{engine.version} | Points: {sample_points} | Status: {engine.get_spirit_evolution_status(sample_points)}")