"""
Purpose: 사용자의 운동, 수면, 심박수 등 건강 데이터를 수집하여 다변수 세분화 수식으로 계산하고, 에러 발생 시 간결 수식으로 폴백하는 10세대 백엔드 엔진.
Scope: 건강 점수 연산, 칼로리 소모 계산 및 위험 감지.
SSOT: HEALTH IS ALL/03_BACKEND/dynamic_health_engine_v10.py
Related Documents: HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V8.md
Change History: 2026-07-31 (v10.0) - 정밀 수식 세분화 및 안전 예외 전환 로직 적용.
"""

import math
from typing import Dict, Any

class DynamicHealthEngineV10:
    def __init__(self):
        self.version = "10.0.0"

    def calculate_health_score(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Purpose: 건강 점수를 계산함. 다변수 수식 적용 후 에러 시 1단계 간결 수식으로 폴백.
        """
        try:
            # Tier-2: 세분화/정밀화된 다변수 수식
            steps = float(user_data.get('steps', 0))
            sleep_hours = float(user_data.get('sleep_hours', 7.0))
            hrv = float(user_data.get('hrv', 50.0))
            temperature = float(user_data.get('temperature', 22.0))
            streak_days = float(user_data.get('streak_days', 1))

            # 매번 다른 수치가 작용하도록 가변 환경 인자 적용
            env_factor = 1.0 + (math.sin(temperature) * 0.05)
            
            # 정밀 수식 연산
            activity_score = min(100.0, (steps / 10000.0) * 40.0)
            sleep_score = min(100.0, (sleep_hours / 8.0) * 30.0)
            recovery_score = min(100.0, (hrv / 70.0) * 30.0)
            streak_bonus = min(10.0, streak_days * 0.5)

            final_score = (activity_score + sleep_score + recovery_score + streak_bonus) * env_factor
            final_score = round(min(100.0, max(0.0, final_score)), 2)

            return {
                "status": "SUCCESS",
                "tier": "Tier-2 Dynamic",
                "health_score": final_score,
                "metrics": {
                    "activity": round(activity_score, 2),
                    "sleep": round(sleep_score, 2),
                    "recovery": round(recovery_score, 2)
                }
            }
        except Exception as e:
            # Exception Handling: 충돌/오류 시 과감히 포기하고 1단계 간결 수식으로 전환
            return self._fallback_simple_calculation(user_data, str(e))

    def _fallback_simple_calculation(self, user_data: Dict[str, Any], error_msg: str) -> Dict[str, Any]:
        """
        1단계 간결한 계산식 (Fallback Tier-1)
        """
        steps = float(user_data.get('steps', 0))
        simple_score = min(100.0, (steps / 10000.0) * 100.0)
        
        return {
            "status": "FALLBACK_SUCCESS",
            "tier": "Tier-1 Simple",
            "health_score": round(simple_score, 2),
            "fallback_reason": error_msg
        }

if __name__ == "__main__":
    engine = DynamicHealthEngineV10()
    test_data = {"steps": 8500, "sleep_hours": 7.5, "hrv": 62, "temperature": 24, "streak_days": 5}
    print("Test Result:", engine.calculate_health_score(test_data))