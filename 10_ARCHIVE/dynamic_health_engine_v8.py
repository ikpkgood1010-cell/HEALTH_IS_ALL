"""
HEALTH IS ALL - Dynamic Health Engine V8
다변수 정밀 건강/운동 소모 칼로리 연산 및 안전 폴백 시스템 구현
"""

import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DynamicHealthEngineV8")

class DynamicHealthEngineV8:
    """건강 지표 세분화 계산 및 안정성 보장 백엔드 엔진"""

    def __init__(self):
        self.version = "8.0.0"

    def calculate_calories_burned(
        self,
        weight_kg: float,
        duration_hours: float,
        met_value: float,
        heart_rate_avg: float = None,
        heart_rate_rest: float = 60.0,
        heart_rate_max: float = 190.0
    ) -> Dict[str, Any]:
        """
        정밀 다변수 공식 및 폴백 공식을 통한 칼로리 연산
        """
        # 입력 데이터 기본 유효성 검증
        if weight_kg <= 0 or duration_hours <= 0 or met_value <= 0:
            logger.warning("유효하지 않은 기본 입력값. 기본 보정값 사용.")
            weight_kg = max(weight_kg, 60.0)
            duration_hours = max(duration_hours, 0.1)
            met_value = max(met_value, 1.0)

        # 다변수 정밀 계산 시도
        try:
            if heart_rate_avg and heart_rate_avg > heart_rate_rest:
                if heart_rate_max <= heart_rate_rest:
                    raise ValueError("최대 심박수는 안정 심박수보다 커야 합니다.")
                
                hr_factor = (heart_rate_avg - heart_rate_rest) / (heart_rate_max - heart_rate_rest)
                hr_factor = min(max(hr_factor, 0.0), 1.5) # 안전 범위 제한
                
                precision_calories = met_value * weight_kg * duration_hours * (1.0 + hr_factor)
                
                return {
                    "calories": round(precision_calories, 2),
                    "formula_type": "PRECISION_V8",
                    "hr_factor_applied": round(hr_factor, 3),
                    "status": "SUCCESS"
                }
        except Exception as e:
            logger.error(f"정밀 연산 중 예외 발생: {e}. 간결 수식으로 폴백합니다.")

        # 안전 폴백 계산식 (Simplified Fallback)
        fallback_calories = met_value * weight_kg * duration_hours
        return {
            "calories": round(fallback_calories, 2),
            "formula_type": "FALLBACK_V1",
            "hr_factor_applied": 0.0,
            "status": "FALLBACK_APPLIED"
        }

if __name__ == "__main__":
    engine = DynamicHealthEngineV8()
    # Test Case 1: 정밀 연산 (세차 등 고강도 수공업 활동 2시간 예시)
    result_precision = engine.calculate_calories_burned(
        weight_kg=72.0, duration_hours=2.0, met_value=4.5, heart_rate_avg=135.0
    )
    print("정밀 연산 결과:", result_precision)

    # Test Case 2: 심박수 누락 시 안전 폴백 테스트
    result_fallback = engine.calculate_calories_burned(
        weight_kg=72.0, duration_hours=2.0, met_value=4.5
    )
    print("폴백 연산 결과:", result_fallback)