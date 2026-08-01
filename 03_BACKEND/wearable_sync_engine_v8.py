"""
HEALTH IS ALL - Wearable Sync Engine V8
웨어러블 심박수 및 활동 데이터 수신, 데이터 유효성 검증 및 안전 폴백 동기화 모듈
"""

import logging
from typing import Dict, Any, List
from dynamic_health_engine_v8 import DynamicHealthEngineV8

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WearableSyncEngineV8")

class WearableSyncEngineV8:
    def __init__(self):
        self.version = "8.0.0"
        self.health_engine = DynamicHealthEngineV8()

    def process_wearable_payload(self, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        웨어러블에서 수신된 원시 데이터를 검증하고 건강 칼로리를 연산함
        """
        try:
            met_value = float(payload.get("met_value", 4.0))
            duration_hours = float(payload.get("duration_hours", 0.5))
            weight_kg = float(payload.get("weight_kg", 70.0))
            heart_rate_avg = payload.get("heart_rate_avg")

            if heart_rate_avg is not None:
                heart_rate_avg = float(heart_rate_avg)

            # 건강 엔진 연산 실행
            calc_result = self.health_engine.calculate_calories_burned(
                weight_kg=weight_kg,
                duration_hours=duration_hours,
                met_value=met_value,
                heart_rate_avg=heart_rate_avg
            )

            logger.info(f"사용자 {user_id} 데이터 동기화 완료: {calc_result['formula_type']}")
            return {
                "user_id": user_id,
                "sync_status": "COMPLETED",
                "result": calc_result
            }

        except Exception as e:
            logger.error(f"웨어러블 페이로드 처리 중 오류 발생: {e}")
            return {
                "user_id": user_id,
                "sync_status": "FAILED_FALLBACK_DEFAULT",
                "result": {
                    "calories": 100.0,
                    "formula_type": "SAFE_DEFAULT",
                    "status": "ERROR_HANDLED"
                }
            }

if __name__ == "__main__":
    sync_engine = WearableSyncEngineV8()
    # 정상 데이터 수신 테스트
    sample_payload = {"met_value": 4.5, "duration_hours": 2.0, "weight_kg": 72.0, "heart_rate_avg": 130.0}
    res = sync_engine.process_wearable_payload("USER_123", sample_payload)
    print("동기화 결과:", res)