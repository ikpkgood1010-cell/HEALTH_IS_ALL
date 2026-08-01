"""
HEALTH IS ALL - Dynamic Nutrition & Metabolism Calculator Engine
Filename: dynamic_nutrition_calculator.py
Path: HEALTH IS ALL/backend/dynamic_nutrition_calculator.py
Purpose: Mifflin-St Jeor BMR, 영양소별 TEF, EPOC 및 정령 친밀도가 결합된 다변수 영양 대사 산출 엔진
"""

import random
from typing import Dict, Any

class DynamicNutritionCalculator:
    """
    정밀 다변수 영양 및 소비 대사량 계산기
    """

    @staticmethod
    def calculate_daily_metabolism(
        weight_kg: float,
        height_cm: float,
        age: int,
        gender: str,  # 'M' or 'F'
        protein_g: float,
        carbs_g: float,
        fat_g: float,
        workout_mets: float = 0.0,
        workout_min: float = 0.0,
        spirit_affinity_lvl: int = 1,
        recovery_score: float = 70.0
    ) -> Dict[str, Any]:
        """
        BMR + TEF + EPOC + 정령 가중치 + 미세 난수가 통합 적용된 대사량 정밀 계산
        """
        # 1. 입력 수치 안전성 검증
        if weight_kg < 30.0 or weight_kg > 250.0 or height_cm < 100.0 or height_cm > 230.0:
            return DynamicNutritionCalculator._build_fallback_metabolism(weight_kg, gender)

        # 2. Mifflin-St Jeor 기초대사량(BMR) 계산
        gender_offset = 5.0 if gender.upper() == 'M' else -161.0
        base_bmr = (10.0 * weight_kg) + (6.25 * height_cm) - (5.0 * age) + gender_offset

        # 3. 영양소별 식이성 열효과 (TEF) 정밀 산출
        # 단백질: 4kcal/g 의 25%, 탄수화물: 4kcal/g 의 8%, 지방: 9kcal/g 의 2.5%
        protein_kcal = protein_g * 4.0
        carbs_kcal = carbs_g * 4.0
        fat_kcal = fat_g * 9.0
        total_intake_kcal = protein_kcal + carbs_kcal + fat_kcal

        tef_kcal = (protein_kcal * 0.25) + (carbs_kcal * 0.08) + (fat_kcal * 0.025)

        # 4. 운동 소모 칼로리 및 EPOC (고강도 후속 대사) 산출
        # Activity Kcal = METs * weight * (min / 60)
        workout_kcal = workout_mets * weight_kg * (workout_min / 60.0)
        
        # METs가 6.0 이상인 고강도 운동 시 EPOC 8% 추가 가산
        epoc_kcal = (workout_kcal * 0.08) if workout_mets >= 6.0 else (workout_kcal * 0.02)

        # 5. 정령 친밀도 및 수면 회복 지수 기반 미세 가중치
        affinity_bonus = 1.0 + (spirit_affinity_lvl * 0.003)
        recovery_factor = 0.98 if recovery_score < 40.0 else 1.02  # 피로 시 대사율 약간 저하

        # 6. 매일 매번 다른 수치를 제공하는 미세 지터 난수 ($0.98 \sim 1.02$)
        jitter = random.uniform(0.98, 1.02)

        # 총 동적 일일 에너지 소비량 (TDEE)
        total_tdee = (base_bmr + tef_kcal + workout_kcal + epoc_kcal) * affinity_bonus * recovery_factor * jitter

        # 호감형 영양 상태 인터페이스 문구 생성
        feedback = DynamicNutritionCalculator._generate_friendly_feedback(total_intake_kcal, total_tdee)

        return {
            "base_bmr": round(base_bmr, 1),
            "tef_kcal": round(tef_kcal, 1),
            "workout_kcal": round(workout_kcal, 1),
            "epoc_kcal": round(epoc_kcal, 1),
            "total_intake_kcal": round(total_intake_kcal, 1),
            "total_dynamic_tdee": round(total_tdee, 1),
            "spirit_affinity_bonus_pct": round((affinity_bonus - 1.0) * 100, 2),
            "friendly_feedback": feedback,
            "is_fallback": False
        }

    @staticmethod
    def _build_fallback_metabolism(weight_kg: float, gender: str) -> Dict[str, Any]:
        """
        입력치 범주 초과 시 하리스-베네딕트 간이 수식 Fallback
        """
        safe_weight = max(40.0, min(120.0, weight_kg))
        simple_bmr = safe_weight * (24.0 if gender.upper() == 'M' else 22.0)
        return {
            "base_bmr": round(simple_bmr, 1),
            "tef_kcal": 150.0,
            "workout_kcal": 200.0,
            "epoc_kcal": 10.0,
            "total_intake_kcal": 1800.0,
            "total_dynamic_tdee": round(simple_bmr + 360.0, 1),
            "spirit_affinity_bonus_pct": 0.0,
            "friendly_feedback": "기본 표준 설정으로 정령이 에너지를 균형 있게 계산 중이에요 🌿",
            "is_fallback": True
        }

    @staticmethod
    def _generate_friendly_feedback(intake: float, tdee: float) -> str:
        diff = intake - tdee
        if abs(diff) < 200:
            return "✨ 영양 수용량이 거의 완벽하게 균형을 이루고 있어요! 정령이 매우 기뻐합니다."
        elif diff < 0:
            return "🌿 훌륭한 활동량입니다! 따뜻한 물과 건강한 단백질 간식으로 에너지를 채워주셔도 좋아요."
        else:
            return "💪 오늘 충분한 에너지가 충전되었습니다! 내일 정령과 함께 활기차게 소모해봐요!"

if __name__ == "__main__":
    calc = DynamicNutritionCalculator()
    res = calc.calculate_daily_metabolism(
        weight_kg=70.0, height_cm=175.0, age=30, gender='M',
        protein_g=110.0, carbs_g=180.0, fat_g=50.0,
        workout_mets=7.0, workout_min=40.0, spirit_affinity_lvl=5
    )
    print(f"[Dynamic Nutrition Engine Output] {res}")