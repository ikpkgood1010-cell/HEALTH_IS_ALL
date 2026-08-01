# 파일 저장 경로: HEALTH IS ALL/03_BACKEND/dynamic_health_engine_v6.py
# SSOT: HEALTH IS ALL/03_BACKEND/dynamic_health_engine_v6.py
# Related Documents: HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V6.md
# Change History: V5 -> V6 (다변수 파동 공식 적용 및 안전성 보장)

import math
from typing import Dict, Any

class DynamicHealthEngineV6:
    """
    V6 핵심 건강 동적 연산 백엔드 엔진
    """
    
    def __init__(self):
        self.version = "6.0.0"

    def calculate_daily_health_metrics(self, user_profile: Dict[str, Any], health_logs: Dict[str, Any]) -> Dict[str, Any]:
        """
        일일 정밀 건강 수치 동적 산출 (BMR, TDEE, HealthScore)
        """
        try:
            weight = float(user_profile.get("weight", 65.0))
            height = float(user_profile.get("height", 170.0))
            age = int(user_profile.get("age", 30))
            gender = user_profile.get("gender", "M")
            
            # 기본 BMR (Mifflin-St Jeor)
            gender_constant = 5 if gender == "M" else -161
            bmr_base = (10 * weight) + (6.25 * height) - (5 * age) + gender_constant

            # V6 동적 변수 반영 (HRV 및 수면 변동성)
            hrv_norm = float(health_logs.get("hrv_norm", 0.5))  # 0.0 ~ 1.0
            sleep_hours = float(health_logs.get("sleep_hours", 7.0))
            
            sleep_modifier = min(1.1, max(0.85, sleep_hours / 8.0))
            hrv_dynamic = 0.95 + 0.1 * math.sin(hrv_norm * math.pi)

            bmr_dynamic = bmr_base * sleep_modifier * hrv_dynamic
            
            # TDEE 계산 (활동성 계수 + 변동성)
            activity_level = float(health_logs.get("activity_level", 1.2)) # 기본 1.2
            tdee_dynamic = bmr_dynamic * activity_level

            # 종합 건강 점수 (100점 만점)
            health_score = int(min(100, max(10, (sleep_hours / 8.0 * 40) + (hrv_norm * 30) + (activity_level / 1.5 * 30))))

            return {
                "status": "SUCCESS",
                "engine_version": self.version,
                "bmr_dynamic": round(bmr_dynamic, 1),
                "tdee_dynamic": round(tdee_dynamic, 1),
                "health_score": health_score,
                "is_fallback": False
            }

        except Exception as e:
            return self._fallback_health_metrics(user_profile, str(e))

    def _fallback_health_metrics(self, user_profile: Dict[str, Any], error_msg: str) -> Dict[str, Any]:
        """폴백 연산: 기본 BMR 수치만 반환하여 서비스 연속성 유지"""
        weight = float(user_profile.get("weight", 65.0))
        height = float(user_profile.get("height", 170.0))
        age = int(user_profile.get("age", 30))
        bmr_base = (10 * weight) + (6.25 * height) - (5 * age) + 5

        return {
            "status": "FALLBACK",
            "engine_version": self.version,
            "bmr_dynamic": round(bmr_base, 1),
            "tdee_dynamic": round(bmr_base * 1.2, 1),
            "health_score": 70,
            "is_fallback": True,
            "fallback_reason": error_msg
        }