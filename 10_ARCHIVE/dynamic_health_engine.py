"""
HEALTH IS ALL - Dynamic Health & RPG Calculation Engine
Filename: dynamic_health_engine.py
Path: HEALTH IS ALL/backend/dynamic_health_engine.py
Purpose: SSOT 문서(DYNAMIC_FORMULA_REGISTRY.md)에 의거한 정밀 건강 및 RPG 보상 동적 계산 백엔드 엔진
"""

import math
import random
from typing import Dict, Any, Optional

class DynamicHealthEngine:
    """
    건강 지표와 RPG 게이밍 요소를 정밀하게 계산하는 백엔드 코어 클래스.
    """

    @staticmethod
    def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
        """
        Mifflin-St Jeor 공식을 이용한 기초대사량(BMR) 산출.
        이상치 입력 시 기본값 적용(Fallback).
        """
        # 이상치 예외 처리
        if weight_kg <= 30 or weight_kg >= 250:
            weight_kg = 70.0 if gender.upper() == 'M' else 55.0
        if height_cm <= 100 or height_cm >= 230:
            height_cm = 175.0 if gender.upper() == 'M' else 162.0
        if age <= 5 or age >= 120:
            age = 30

        base_bmr = (10.0 * weight_kg) + (6.25 * height_cm) - (5.0 * age)
        if gender.upper() == 'M':
            return base_bmr + 5.0
        else:
            return base_bmr - 161.0

    @staticmethod
    def calculate_exercise_reward(
        duration_min: float,
        met_value: float,
        weight_kg: float,
        rpe: Optional[int] = 5,
        avg_hr: Optional[float] = None,
        max_hr: Optional[float] = None,
        streak_days: int = 0,
        spirit_affinity_level: int = 1
    ) -> Dict[str, Any]:
        """
        운동 소모 칼로리 및 동적 EXP 산출 로직.
        심박수 및 RPE 유무에 따른 Fallback 자동 전환 포함.
        """
        # 1. 소모 칼로리 계산 (Standard MET Formula)
        # Calories = Duration(min) * (MET * 3.5 * weight) / 200
        base_calories = duration_min * (met_value * 3.5 * weight_kg) / 200.0

        # 2. 강도 보정 인자 (Intensity Ratio)
        if avg_hr and max_hr and max_hr > 0:
            # 심박수 데이터 기반 정밀 강도 보정
            hr_ratio = avg_hr / max_hr
            intensity_ratio = max(0.8, min(1.5, hr_ratio * 1.4))
        elif rpe is not None:
            # RPE(주관적 자각도 1~10) 기반 보정
            intensity_ratio = 0.7 + (rpe / 10.0) * 0.6
        else:
            # Fallback 기본값
            intensity_ratio = 1.0

        caloric_expenditure = round(base_calories * intensity_ratio, 1)

        # 3. RPG EXP 산출
        base_exp = duration_min * met_value * 1.5
        streak_bonus = 1.0 + math.log(1.0 + max(0, streak_days)) * 0.05
        affinity_multiplier = 0.9 + min(0.4, (spirit_affinity_level * 0.008))
        
        # 지루함을 방지하는 5% 미세 무작위 난수 변동 인자
        fluctuator = random.uniform(0.95, 1.05)

        final_exp = int(base_exp * intensity_ratio * streak_bonus * affinity_multiplier * fluctuator)

        return {
            "calories_burned": caloric_expenditure,
            "exp_gained": max(10, final_exp),
            "intensity_ratio": round(intensity_ratio, 2),
            "streak_bonus_pct": round((streak_bonus - 1.0) * 100, 1),
            "is_fallback_used": (avg_hr is None and rpe is None)
        }

if __name__ == "__main__":
    # 테스트 실행
    engine = DynamicHealthEngine()
    bmr = engine.calculate_bmr(72.0, 178.0, 29, 'M')
    reward = engine.calculate_exercise_reward(
        duration_min=45,
        met_value=7.0,
        weight_kg=72.0,
        rpe=8,
        streak_days=12,
        spirit_affinity_level=15
    )
    print(f"[Engine Test] BMR: {bmr} kcal")
    print(f"[Engine Test] Reward: {reward}")