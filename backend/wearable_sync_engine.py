"""
HEALTH IS ALL - Wearable Device Real-time Sync Engine
Filename: wearable_sync_engine.py
Path: HEALTH IS ALL/backend/wearable_sync_engine.py
Purpose: 스마트 워치 실시간 생체 데이터 파싱, 이상치 필터링 및 연결 상태 관리 백엔드 엔진
"""

import random
from typing import Dict, Any, List

class WearableSyncEngine:
    """
    스마트 워치 및 웨어러블 디바이스 실시간 동기화 엔진
    """

    MIN_VALID_HR = 40
    MAX_VALID_HR = 210

    @staticmethod
    def process_biometric_packet(
        raw_packet: Dict[str, Any],
        user_age: int = 30
    ) -> Dict[str, Any]:
        """
        수신된 생체 신호 데이터 파싱 및 이상치 보정
        """
        if not raw_packet or "heart_rate" not in raw_packet:
            return WearableSyncEngine._build_fallback_packet()

        raw_hr = raw_packet.get("heart_rate", 75)
        raw_steps = raw_packet.get("realtime_steps", 0)
        device_name = raw_packet.get("device_name", "Smart Watch")

        # 1. 심박수 이상치 필터링
        if raw_hr < WearableSyncEngine.MIN_VALID_HR or raw_hr > WearableSyncEngine.MAX_VALID_HR:
            valid_hr = 72  # 안전 기본값 대체
            confidence = 0.5
        else:
            valid_hr = raw_hr
            confidence = 0.98

        # 2. 과도한 심박수 안전 검증 (Max HR 85% 초과 여부)
        max_safe_hr = int((220 - user_age) * 0.85)
        is_warning_zone = valid_hr > max_safe_hr

        # 3. 다정한 심박 상태 메시지 생성
        if is_warning_zone:
            sync_message = (
                f"심장이 힘차게 뛰고 있어요! ({valid_hr} BPM) "
                f"수호 정령이 잠시 그늘 아래서 미소 지으며 휴식을 권하고 있습니다 🌿"
            )
        else:
            sync_message = (
                f"스마트 워치와 정령이 같은 박자로 호흡 중입니다 ✨ ({valid_hr} BPM)"
            )

        return {
            "device_name": device_name,
            "validated_hr": valid_hr,
            "realtime_steps": raw_steps,
            "confidence_score": confidence,
            "is_warning_zone": is_warning_zone,
            "sync_message": sync_message,
            "is_fallback": False
        }

    @staticmethod
    def _build_fallback_packet() -> Dict[str, Any]:
        return {
            "device_name": "스마트 워치 (연결 대기)",
            "validated_hr": 72,
            "realtime_steps": 0,
            "confidence_score": 0.8,
            "is_warning_zone": False,
            "sync_message": "스마트 워치가 잠시 쉬고 있어요 🌿 손목을 가볍게 토닥여 다시 연결해 볼까요?",
            "is_fallback": True
        }

if __name__ == "__main__":
    engine = WearableSyncEngine()
    dummy_packet = {"device_name": "Galaxy Watch 6", "heart_rate": 138, "realtime_steps": 4200}
    res = engine.process_biometric_packet(dummy_packet, user_age=32)
    print(f"[Wearable Sync Engine Output] {res}")