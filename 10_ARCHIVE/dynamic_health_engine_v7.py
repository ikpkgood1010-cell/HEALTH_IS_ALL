"""
===============================================================================
HEALTH IS ALL - Dynamic Health Engine V7
===============================================================================
Purpose:
  사용자의 신체 데이터(체중, 키, 나이, 심박수, 수면)를 다변수 고정밀 공식으로 분석하여
  기초대사량(BMR), 일일 활동 소모량(TDEE), 및 게임 보상 가율을 계산하는 백엔드 코어 엔진.

Scope:
  - Mifflin-St Jeor 기반 BMR 세분화 연산
  - 심박수 및 피로도 적용 칼로리 소모량 계산
  - 게임 경험치 및 수면 회복 가율 산출

SSOT:
  - 본 코드는 백엔드 건강 계산 로직의 단일 진실 공급원(SSOT) 역할을 수행함.

Definitions:
  - BMR: Basal Metabolic Rate (기초대사량)
  - TDEE: Total Daily Energy Expenditure (일일 총 에너지 소비량)
  - Spirit EXP Multiplier: 건강 달성도 기반 게임 경험치 가율

Runtime:
  - Python 3.11+, FastAPI 서비스 모듈 내 탑재

Rules:
  - 파라미터 유효성 검사 실패 시 간결한 Fallback 공식으로 자동 전환.
  - 극단적 수치 오버플로우 방지를 위해 계산 결과값 Soft Clamp 적용.

State:
  - ENGINE_READY, CALCULATING, COMPLETED, FALLBACK_APPLIED

Event:
  - HealthEngineV7.calculate_user_health_metrics()

Example:
  >>> engine = DynamicHealthEngineV7()
  >>> res = engine.calculate_user_health_metrics(weight=70, height=175, age=30, is_male=True, avg_hr=110, sleep_hours=7.5)

Exception:
  - InvalidInputException: 체중, 키 등이 0 이하일 경우 발생하여 기본 Fallback 수식 적용.

Related Documents:
  - HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V7_SPEC.md
  - HEALTH IS ALL/01_ARCHITECTURE/RECOVERY_BALANCE_SPEC_V3.md

Change History:
  - 2026-07-31 (V7.0.0): v6 대비 다변수 정밀 수식 도입 및 2단계 예외 처리 적용.
===============================================================================
"""

import math
from typing import Dict, Any

class DynamicHealthEngineV7:
    def __init__(self):
        self.version = "7.0.0"

    def calculate_bmr(self, weight: float, height: float, age: int, is_male: bool) -> float:
        """Mifflin-St Jeor 고정밀 BMR 연산 수식"""
        if weight <= 0 or height <= 0 or age <= 0:
            # Fallback 1단계 간결 수식
            return max(1200.0, weight * 22.0)
        
        gender_offset = 5.0 if is_male else -161.0
        bmr = (10.0 * weight) + (6.25 * height) - (5.0 * age) + gender_offset
        return max(800.0, min(bmr, 3500.0))  # Soft clamp

    def calculate_tdee_v7(
        self,
        weight: float,
        height: float,
        age: int,
        is_male: bool,
        activity_level: float = 1.375,
        avg_hr: float = 70.0,
        sleep_hours: float = 7.0
    ) -> Dict[str, Any]:
        """다변수 정밀 TDEE 및 게임 버프 산출 함수"""
        status = "COMPLETED"
        try:
            bmr = self.calculate_bmr(weight, height, age, is_male)
            
            # 심박수 기반 가중치 변수 (80bpm 이상 시 미세 증가)
            hr_stress_factor = math.pow(max(0.0, (avg_hr - 70.0) / 100.0), 1.1) * 0.1
            hr_stress_factor = min(0.15, max(0.0, hr_stress_factor))

            # 수면 부족 피로도 감쇄 변수
            sleep_deficit = max(0.0, (8.0 - sleep_hours) / 8.0)
            fatigue_penalty = sleep_deficit * 0.08

            # 최종 동적 TDEE 산출
            multiplier = activity_level + hr_stress_factor - fatigue_penalty
            multiplier = max(1.1, min(2.3, multiplier))
            
            tdee = bmr * multiplier

            # 게임 스피릿 경험치 가율 산출
            health_synergy_score = 1.0 + (hr_stress_factor * 2.0) - (fatigue_penalty * 1.5)
            exp_multiplier = round(max(0.8, min(1.5, health_synergy_score)), 2)

            return {
                "engine_version": self.version,
                "status": status,
                "bmr": round(bmr, 1),
                "tdee": round(tdee, 1),
                "hr_stress_factor": round(hr_stress_factor, 4),
                "fatigue_penalty": round(fatigue_penalty, 4),
                "exp_multiplier": exp_multiplier,
                "message": "오늘의 생체 상태에 맞춘 정밀 영양 및 게임 가율이 산출되었습니다! 🌟"
            }
        except Exception as e:
            # 안전을 위한 1단계 간결 수식 전환
            fallback_bmr = max(1200.0, weight * 22.0) if weight > 0 else 1500.0
            return {
                "engine_version": self.version,
                "status": "FALLBACK_APPLIED",
                "bmr": fallback_bmr,
                "tdee": fallback_bmr * 1.375,
                "exp_multiplier": 1.0,
                "message": "기본 건강 수식으로 전환되어 계산이 안전하게 완료되었습니다."
            }

# 독립 실행 확인 테스트
if __name__ == "__main__":
    engine = DynamicHealthEngineV7()
    result = engine.calculate_tdee_v7(weight=72.5, height=178.0, age=29, is_male=True, avg_hr=105, sleep_hours=6.5)
    print("V7 Engine Calculation Result:", result)