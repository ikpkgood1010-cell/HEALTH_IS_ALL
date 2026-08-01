"""
================================================================================
Purpose:
  HEALTH IS ALL 프로젝트의 건강 데이터 정밀 계산, dynamic 계산식 적용 및
  게임 시스템(정령 성장, 퀘스트 보상)과의 듀얼 밸런스 시너지를 제공하는 핵심 엔진.

Scope:
  - 심박수 기반 다변수 칼로리 소모량 산출
  - 식단 영양소 시너지 및 혈당부하(GL) 지수 반영 점수화
  - 건강 점수 기반 게임 보상 촉매(Catalyst) 및 감쇄(Anti-Grind) 수식 적용
  - 센서 미수신 또는 계산 오류 발생 시 한 단계 간결한 표준식으로의 Fallback 자동 전환

SSOT:
  - HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V8.mdux
  - HEALTH IS ALL/03_GAME_SYSTEM/HEALTH_GAME_DUAL_BALANCE_SPEC_V3.mdux

Definitions:
  - BMR: Basal Metabolic Rate (기초대사량)
  - MET: Metabolic Equivalent of Task (운동 강도 지표)
  - HRV: Heart Rate Variability (심박 변이도)
  - GL: Glycemic Load (추정 혈당 부하)

Runtime:
  - Python 3.10+
  - Dependencies: math, dataclass, typing, json, logging

Rules:
  1. 건강 지표와 게임 보상의 듀얼 밸런스를 1:1로 유지하며 어느 한쪽이 우세하게 편향되지 않도록 함.
  2. 다변수 세분화 공식을 우선 적용하되, 입력값 이상 발생 시 100% 안전한 Fallback 수식으로 즉시 전환.
  3. 모든 결과는 이용자 친화적 피드백 메시지와 함께 표준 Dict 형태로 반환.

State:
  - UserHealthState: 체중, 연령, 성별, 평소 심박수, 수면 효율
  - ExerciseLogState: 운동 종류, 시간, 평균/최고 심박수, HRV
  - DietLogState: 칼로리, 탄/단/지 질량, 식이섬유량, 당류

Event:
  - CALCULATE_HEALTH_SCORE_REQUESTED
  - CALCULATE_EXERCISE_CALORIE_REQUESTED
  - FALLBACK_TRIGGERED_EVENT

Example:
  engine = DynamicHealthEngineV11()
  result = engine.calculate_dynamic_workout_energy(user_state, exercise_log)

Exception:
  - InvalidInputDataError: 입력 데이터 누락 또는 음수 값 발생 시 Fallback 작동
  - CalculationOverflowError: 극단적 수치 인입 시 기본 안전 상한값으로 보정

Related Documents:
  - HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V10_SPEC.mdux
  - HEALTH IS ALL/03_BACKEND/ENGINE_RULES.mdux
  - HEALTH IS ALL/03_GAME_SYSTEM/DYNAMIC_REWARD_CALCULATOR_SPEC.mdux

Change History:
  - v10.0: 단일 변수 가중치 계산 엔진 구현
  - v11.0: 다변수 세분화 수식, 자동 Fallback 안전키, 12단계 구조 표준 완전 반영 및 v11 승격
================================================================================
"""

import math
import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DynamicHealthEngineV11")

@dataclass
class UserProfile:
    age: int
    weight_kg: float
    height_cm: float
    is_male: bool
    resting_hr: float = 60.0

@dataclass
class ExerciseInput:
    duration_minutes: float
    avg_hr: Optional[float] = None
    max_hr: Optional[float] = None
    met_value: float = 4.0
    hrv_ms: Optional[float] = None

@dataclass
class DietInput:
    total_calories: float
    carbs_g: float
    protein_g: float
    fat_g: float
    fiber_g: float = 0.0
    sugar_g: float = 0.0

class DynamicHealthEngineV11:
    """
    건강-게임 듀얼 밸런스를 지원하는 정밀 계산 백엔드 엔진 v11
    """

    def __init__(self):
        self.version = "11.0.0"

    def calculate_bmr(self, user: UserProfile) -> float:
        """Mifflin-St Jeor 공식을 이용한 기초대사량 계산"""
        try:
            bmr = (10 * user.weight_kg) + (6.25 * user.height_cm) - (5 * user.age)
            bmr += 5 if user.is_male else -161
            return max(bmr, 1000.0)
        except Exception as e:
            logger.warning(f"BMR 계산 중 오류 발생, 표준 기본값 적용: {e}")
            return 1500.0

    def calculate_dynamic_workout_energy(self, user: UserProfile, exercise: ExerciseInput) -> Dict[str, Any]:
        """
        [세분화 수식] 심박수, HRV, 연령, 체중을 반영한 정밀 칼로리 소모량 계산
        오류 또는 데이터 부족 시 [Fallback] 기본 METs 수식으로 자동 전환
        """
        # 1. 정밀 세분화 공식 시도
        try:
            if exercise.duration_minutes <= 0 or user.weight_kg <= 0:
                raise ValueError("운동 시간 및 체중은 양수여야 합니다.")

            if exercise.avg_hr and exercise.avg_hr > user.resting_hr:
                # Keytel 공식을 변형한 정밀 칼로리 소모 수식
                if user.is_male:
                    cal_per_min = (-55.0969 + (0.6309 * exercise.avg_hr) + (0.1988 * user.weight_kg) + (0.2017 * user.age)) / 4.184
                else:
                    cal_per_min = (-20.4022 + (0.4472 * exercise.avg_hr) - (0.1263 * user.weight_kg) + (0.074 * user.age)) / 4.184
                
                cal_per_min = max(cal_per_min, 1.0)
                raw_calories = cal_per_min * exercise.duration_minutes

                # HRV 피로도 보정 계수 (지루함 방지 변수 적용)
                hrv_factor = 1.0
                if exercise.hrv_ms:
                    hrv_factor = max(0.85, min(1.15, 1.0 + ((exercise.hrv_ms - 50.0) / 200.0)))

                final_calories = round(raw_calories * hrv_factor, 2)
                game_exp = int(final_calories * 1.2)

                return {
                    "status": "SUCCESS",
                    "mode": "PRECISION_DYNAMIC",
                    "burned_calories": final_calories,
                    "game_exp_reward": game_exp,
                    "hrv_bonus_applied": hrv_factor != 1.0,
                    "message": f"정밀 심박 측정으로 {final_calories} kcal 소모가 기록되었습니다! 정령이 무럭무럭 자랍니다. 🌿"
                }
            else:
                raise ValueError("심박수 데이터가 유효 범위를 벗어났습니다. Fallback 수식으로 전환합니다.")

        # 2. 안전 Fallback 공식 (1단계 간결 수식)
        except Exception as e:
            logger.info(f"정밀 계산 대신 Fallback METs 수식을 적용합니다. (사유: {e})")
            
            basic_calories = round((exercise.met_value * 3.5 * user.weight_kg / 200.0) * exercise.duration_minutes, 2)
            basic_exp = int(basic_calories * 1.0)

            return {
                "status": "SUCCESS_FALLBACK",
                "mode": "STANDARD_METS_FALLBACK",
                "burned_calories": max(basic_calories, 10.0),
                "game_exp_reward": max(basic_exp, 10),
                "hrv_bonus_applied": False,
                "message": f"표준 운동 강도(METs) 기준으로 {basic_calories} kcal 소모를 계산했어요. 안정적인 성장을 이뤄내고 있습니다! 💪"
            }

    def calculate_diet_synergy_score(self, diet: DietInput) -> Dict[str, Any]:
        """
        [세분화 수식] 영양소 비율, 식이섬유 및 당류 비율을 반영한 식단 건강 점수 및 게임 촉매 계산
        """
        try:
            if diet.total_calories <= 0:
                raise ValueError("총 칼로리는 0보다 커야 합니다.")

            # 1. 탄단지 에너지 비율 정밀 산출
            carb_cal = diet.carbs_g * 4
            protein_cal = diet.protein_g * 4
            fat_cal = diet.fat_g * 9

            carb_ratio = carb_cal / diet.total_calories
            protein_ratio = protein_cal / diet.total_calories
            fat_ratio = fat_cal / diet.total_calories

            # 이상적인 탄단지 권장 비율 (5:3:2)과의 이격도 계산
            ratio_penalty = abs(carb_ratio - 0.5) + abs(protein_ratio - 0.3) + abs(fat_ratio - 0.2)
            base_score = max(50.0, 100.0 - (ratio_penalty * 80.0))

            # 2. 식이섬유 가산점 & 당류 감산점
            fiber_bonus = min(diet.fiber_g * 1.5, 15.0)
            sugar_penalty = min(diet.sugar_g * 1.0, 20.0)

            final_diet_score = round(max(30.0, min(100.0, base_score + fiber_bonus - sugar_penalty)), 1)
            
            # 3. 게임 시스템 연동 촉매 배율 (Game Catalyst)
            spirit_catalyst_multiplier = round(0.8 + (final_diet_score / 250.0), 2)  # 0.92 ~ 1.20 배율

            return {
                "status": "SUCCESS",
                "mode": "DYNAMIC_NUTRITION_SPEC",
                "diet_score": final_diet_score,
                "spirit_catalyst_multiplier": spirit_catalyst_multiplier,
                "message": f"오늘의 영양 균형 점수는 {final_diet_score}점입니다! 정령 성장 속도 배율이 x{spirit_catalyst_multiplier}로 적용됩니다. 🥗"
            }

        except Exception as e:
            logger.warning(f"식단 계산 예외 발생, 표준 균형 점수 적용: {e}")
            return {
                "status": "SUCCESS_FALLBACK",
                "mode": "STANDARD_DIET_FALLBACK",
                "diet_score": 70.0,
                "spirit_catalyst_multiplier": 1.0,
                "message": "식단 정보가 표준값으로 기록되었습니다. 균형 잡힌 식단을 유지하도록 도와드릴게요! ✨"
            }

# 테스트 실행 코드
if __name__ == "__main__":
    engine = DynamicHealthEngineV11()
    user = UserProfile(age=30, weight_kg=70.0, height_cm=175.0, is_male=True, resting_hr=62.0)
    
    # 1. 정밀 측정 테스트
    ex_precision = ExerciseInput(duration_minutes=45, avg_hr=145.0, max_hr=168.0, hrv_ms=65.0)
    res1 = engine.calculate_dynamic_workout_energy(user, ex_precision)
    print("\n--- [1] 정밀 운동 계산 결과 ---")
    print(res1)

    # 2. Fallback 테스트 (심박수 데이터 미수신 시)
    ex_fallback = ExerciseInput(duration_minutes=45, avg_hr=None, met_value=6.0)
    res2 = engine.calculate_dynamic_workout_energy(user, ex_fallback)
    print("\n--- [2] Fallback 자동 전환 결과 ---")
    print(res2)

    # 3. 식단 시너지 계산 테스트
    diet_sample = DietInput(total_calories=650, carbs_g=70, protein_g=40, fat_g=18, fiber_g=8, sugar_g=5)
    res3 = engine.calculate_diet_synergy_score(diet_sample)
    print("\n--- [3] 식단 시너지 & 게임 촉매 계산 결과 ---")
    print(res3)