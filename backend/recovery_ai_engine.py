"""
HEALTH IS ALL - AI Recovery Score & Rest Skill Engine
Filename: recovery_ai_engine.py
Path: HEALTH IS ALL/backend/recovery_ai_engine.py
Purpose: 수면 quality, HRV 및 피로도 기반 회복 지수(RS) 산출, AI 운동 권장 및 정령 휴식 스킬 연동 백엔드 엔진
"""

import math
import random
from typing import Dict, Any, Optional

class RecoveryAIEngine:
    """
    수면/HRV 기반 회복 지수 및 AI 코칭 산출 엔진
    """

    @staticmethod
    def calculate_recovery_score(
        sleep_hours: float,
        deep_sleep_ratio: float,
        rem_sleep_ratio: float,
        hrv_ms: float,
        subjective_fatigue: int = 5,  # 1(최상) ~ 10(극심한 피로)
        is_sensor_available: bool = True,
        recent_3day_avg_rs: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        다변수 수면/HRV 정밀 수식 및 Fallback 기반 회복 지수 산출
        """
        # 1. 이상치 검증 (Exception handling)
        if sleep_hours < 1.0 or sleep_hours > 18.0:
            if recent_3day_avg_rs is not None:
                return RecoveryAIEngine._build_response(
                    score=recent_3day_avg_rs,
                    is_fallback=True,
                    reason="수면 시간 이상치 검출로 최근 3일 평균값 보정"
                )
            sleep_hours = 7.0  # 기본값 보정

        is_fallback_used = False

        if is_sensor_available and hrv_ms > 0:
            # A. 수면 효율성 점수 (Sleep Efficiency Score, 0~100)
            # 권장 수면시간 7.5시간 기준
            duration_factor = min(1.0, sleep_hours / 7.5)
            quality_factor = (deep_sleep_ratio * 1.8) + (rem_sleep_ratio * 1.2)
            sleep_score = min(100.0, (duration_factor * 60.0) + (quality_factor * 40.0))

            # B. HRV 회복 점수 (HRV Score, 기준값 60ms)
            hrv_score = min(100.0, (hrv_ms / 65.0) * 100.0)

            # C. 피로도 차감 인자
            fatigue_penalty = (subjective_fatigue - 1) * 3.5

            # D. 동적 미세 난수 인자 (0.95 ~ 1.05)
            jitter = random.uniform(0.95, 1.05)

            # 종합 회복 지수 수식
            raw_rs = ((sleep_score * 0.45) + (hrv_score * 0.45) - fatigue_penalty) * jitter
            final_rs = max(10.0, min(100.0, raw_rs))
        else:
            # Fallback 수식: 자가 피로도 및 수면 시간 기반 간이 계산
            is_fallback_used = True
            base_score = (sleep_hours / 8.0) * 70.0
            fatigue_adj = (10 - subjective_fatigue) * 3.0
            final_rs = max(15.0, min(95.0, base_score + fatigue_adj))

        return RecoveryAIEngine._build_response(
            score=round(final_rs, 1),
            is_fallback=is_fallback_used
        )

    @staticmethod
    def _build_response(score: float, is_fallback: bool, reason: str = "") -> Dict[str, Any]:
        """
        회복 지수에 따른 AI 맞춤형 운동 권장 및 정령 휴식 스킬 처방
        """
        if score >= 80.0:
            intensity = "HIGH"
            recommendation = "신체 회복 상태가 최상입니다! 고강도 웨이트/인터벌 운동을 추천합니다."
            skill_name = "정령의 신성한 활력 (Vitality Aura)"
            stamina_buff_pct = 20.0
        elif score >= 60.0:
            intensity = "MODERATE"
            recommendation = "적정 회복 상태입니다. 중강도 유산소 및 근력 운동이 적합합니다."
            skill_name = "정령의 평온한 호흡 (Calm Breath)"
            stamina_buff_pct = 10.0
        elif score >= 40.0:
            intensity = "LIGHT"
            recommendation = "피로가 누적되어 있습니다. 가벼운 조깅이나 요가를 권장합니다."
            skill_name = "정령의 수호 방패 (Guardian Shield)"
            stamina_buff_pct = 5.0
        else:
            intensity = "REST"
            recommendation = "오버트레이닝 위험! 오늘은 완전 휴식 또는 정적 스트레칭을 적극 권장합니다."
            skill_name = "정령의 깊은 안식 (Deep Slumber)"
            stamina_buff_pct = 0.0

        return {
            "recovery_score": score,
            "recommended_intensity": intensity,
            "ai_recommendation": recommendation,
            "rest_skill_name": skill_name,
            "stamina_buff_pct": stamina_buff_pct,
            "is_fallback_used": is_fallback,
            "note": reason
        }

if __name__ == "__main__":
    engine = RecoveryAIEngine()
    res = engine.calculate_recovery_score(
        sleep_hours=7.2, deep_sleep_ratio=0.22, rem_sleep_ratio=0.20,
        hrv_ms=58.5, subjective_fatigue=3
    )
    print(f"[Recovery Score Result] {res}")