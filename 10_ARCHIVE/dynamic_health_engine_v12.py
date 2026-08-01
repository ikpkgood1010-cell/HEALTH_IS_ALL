# -*- coding: utf-8 -*-
"""
HEALTH IS ALL - Dynamic Health & Game Reward Engine v12
File Path: HEALTH IS ALL/03_BACKEND/dynamic_health_engine_v12.py

SSOT Reference: HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V11_SPEC.md
Change History:
- v11: Dynamic calculation routines added.
- v12: Integrated multi-variable micro-variations, strict fallback exception handlers,
       and complete user-friendly dialogue responses.
"""

import math
import random
import time
from typing import Dict, Any, Tuple

class DynamicHealthEngineV12:
    """
    건강 목적과 게임 요소의 듀얼 밸런스를 유지하며,
    매번 정밀하고 색다른 보상 수치를 산출하는 핵심 엔진 클래스.
    """

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.version = "v12.0"

    def calculate_daily_rewards(self, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        다변수 세분화 수식을 활용한 정밀 보상 계산 메서드.
        오류/충돌 발생 시 간결 수식(Fallback)으로 즉시 안전 전환.
        """
        try:
            # 1. 입력 데이터 추출
            steps = float(health_data.get("steps", 0))
            sleep_hours = float(health_data.get("sleep_hours", 7.0))
            water_ml = float(health_data.get("water_ml", 1500))
            streak_days = int(health_data.get("streak_days", 1))
            hrv_ms = float(health_data.get("hrv_ms", 50.0))  # 심박 변이도

            # 입력값 범위 검증 (이상 수치 감지 시 Exception 유발하여 Fallback 이동)
            if steps < 0 or sleep_hours < 0 or water_ml < 0 or hrv_ms <= 0:
                raise ValueError("입력 데이터 수치가 유효 범위를 벗어났증니다.")

            # 2. 복합 세분화 다변수 산출식 (매번 지루하지 않은 수치 생성)
            # 타임스탬프와 유저 ID 기반 시드 생성 (결정론적 미세 변동성)
            time_factor = (int(time.time()) % 100) * 0.001
            circadian_modifier = 1.0 + 0.05 * math.sin(time.time() / 3600.0)
            
            # 수면 및 HRV 가중치 연산
            recovery_index = (sleep_hours / 8.0) * 0.6 + (hrv_ms / 60.0) * 0.4
            recovery_index = min(max(recovery_index, 0.5), 1.5)

            # 세분화된 건강 점수 계산
            raw_health_score = (
                (steps / 10000.0) * 40.0 +
                (water_ml / 2000.0) * 20.0 +
                (recovery_index * 40.0)
            ) * circadian_modifier + time_factor

            final_health_score = round(min(max(raw_health_score, 0.0), 100.0), 2)

            # 게임 경험치(EXP) 산출식 (건강 점수에 연동되되 게임성이 건강을 압도하지 않음)
            streak_multiplier = 1.0 + min(streak_days * 0.02, 0.3)  # 최대 30% 연속 달성 보너스
            game_exp = int(final_health_score * 1.5 * streak_multiplier)

            # 호감형 유저 대화 메시지 선택
            dialogue = self._generate_user_dialogue(final_health_score, streak_days)

            return {
                "status": "SUCCESS_COMPLEX",
                "version": self.version,
                "user_id": self.user_id,
                "health_score": final_health_score,
                "game_exp": game_exp,
                "streak_bonus_pct": round((streak_multiplier - 1.0) * 100, 1),
                "user_dialogue": dialogue,
                "calculation_mode": "MULTI_VARIABLE_PRECISION"
            }

        except Exception as e:
            # 충돌 및 오류 발생 시 1초 이내 간결 계산식으로 전환 (Rule 9 준수)
            return self._fallback_simple_calculation(health_data, str(e))

    def _fallback_simple_calculation(self, health_data: Dict[str, Any], error_msg: str) -> Dict[str, Any]:
        """
        수식 오류 시 가동되는 간결하고 안전한 대체 계산 알고리즘.
        """
        steps = float(health_data.get("steps", 0))
        # 단순 가누기 식
        simple_score = min((steps / 10000.0) * 100.0, 100.0)
        simple_exp = int(simple_score * 1.2)

        return {
            "status": "SUCCESS_FALLBACK",
            "version": self.version,
            "user_id": self.user_id,
            "health_score": round(simple_score, 1),
            "game_exp": simple_exp,
            "user_dialogue": "오늘도 건강을 향해 멋진 한 걸음을 내딛으셨어요! 차근차근 함께해 봐요.",
            "calculation_mode": "SIMPLE_FALLBACK_BASELINE",
            "handled_exception": error_msg
        }

    def _generate_user_dialogue(self, score: float, streak: int) -> str:
        """
        이용자 친화적 및 호감형 대화 팝업 멘트 생성기
        """
        if score >= 90:
            return f"와우! 완벽한 하루를 보내셨네요! {streak}일 연속 달성이라니 정말 대단해요! 🌟"
        elif score >= 70:
            return f"훌륭한 리듬을 유지하고 계시네요! 지금처럼 꾸준히 하면 정령도 더 기뻐할 거예요! 😊"
        else:
            return f"오늘도 수고 많으셨어요! 작은 실천이 모여 놀라운 변화를 만든답니다. 힘내세요! 💪"


# 테스트 실행 코드
if __name__ == "__main__":
    engine = DynamicHealthEngineV12("user_test_01")
    sample_data = {
        "steps": 8420,
        "sleep_hours": 7.5,
        "water_ml": 1800,
        "streak_days": 4,
        "hrv_ms": 55.0
    }
    result = engine.calculate_daily_rewards(sample_data)
    print("Execution Result:", result)