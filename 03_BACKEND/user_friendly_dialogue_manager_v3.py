# -*- coding: utf-8 -*-
"""
HEALTH IS ALL - User Friendly Dialogue & Dynamic Tip Engine v3
파일 저장 경로: HEALTH IS ALL/03_BACKEND/user_friendly_dialogue_manager_v3.py

본 모듈은 사용자의 다변수 건강 수치(HRV, 식사 간격, 수분 섭취, 활동 피로도)를 정밀 산출하고,
이를 바탕으로 1~3줄의 이용자 친화적이고 호감 가는 건강 꿀팁과 정령 피드백을 동적으로 생성합니다.
"""

import math
from typing import Dict, Any, Tuple

class UserFriendlyDialogueManagerV3:
    def __init__(self, spirit_name: str = "파이론"):
        self.spirit_name = spirit_name

    def calculate_dynamic_health_multiplier(
        self, 
        hrv: float, 
        meal_interval_hours: float, 
        hydration_ratio: float, 
        rpe: float
    ) -> Tuple[float, bool]:
        """
        다변수 기반 정밀 건강 가중치를 계산합니다.
        오류 또는 범위 초과 발생 시 안전하게 1단계 간결 수식(Fallback)으로 전환합니다.
        """
        try:
            # 변수 범위 유효성 검증
            if not (0 <= hrv <= 150 and 0 <= meal_interval_hours <= 24 and 0 <= hydration_ratio <= 2.0):
                raise ValueError("입력 데이터 범위 초과")

            # 정밀 다변수 수식 적용
            hrv_factor = 1.0 + ((hrv - 50.0) / 100.0)
            meal_factor = 1.0 - (0.05 * abs(meal_interval_hours - 4.0))
            hydration_factor = 1.0 + (0.1 * hydration_ratio)
            rpe_factor = 1.0 - (0.02 * max(0.0, rpe - 6.0))

            multiplier = hrv_factor * meal_factor * hydration_factor * rpe_factor
            
            # 수치 안정성 보장 (0.5 ~ 2.0 범위 제한)
            final_multiplier = max(0.5, min(2.0, round(multiplier, 3)))
            return final_multiplier, False

        except Exception as e:
            # 충돌/오류 위험 시 과감히 포기하고 한 단계 간결한 수식으로 전환 (Fallback)
            fallback_multiplier = 1.0
            return fallback_multiplier, True

    def generate_friendly_tip(
        self, 
        health_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        사용자 건강 데이터를 입력받아 1~3줄 형태의 호감적 꿀팁과 정령 대화를 생성합니다.
        """
        hrv = health_data.get("hrv", 50.0)
        meal_interval = health_data.get("meal_interval_hours", 4.0)
        hydration = health_data.get("hydration_ratio", 0.8)
        rpe = health_data.get("rpe", 4.0)

        multiplier, is_fallback = self.calculate_dynamic_health_multiplier(
            hrv, meal_interval, hydration, rpe
        )

        # 수치 구간별 호감형 대화 및 꿀팁 구성 (1~3줄 유지)
        if multiplier >= 1.2:
            dialogue = (
                f"오늘 컨디션이 정말 최고예요! {self.spirit_name}(이)도 신나서 에너지가 넘치고 있어요.\n"
                f"💡 꿀팁: 수분과 식사 균형이 훌륭해요. 지금처럼 가벼운 스트레칭으로 이 느낌을 유지해 보세요!"
            )
            reward_exp = int(100 * multiplier)
        elif multiplier >= 0.9:
            dialogue = (
                f"차근차근 아주 잘해내고 계세요. {self.spirit_name}(이)와 함께라면 오늘도 건강하게 보낼 수 있어요!\n"
                f"💡 꿀팁: 식사 후 따뜻한 물 한 잔은 소화를 돕고 몸의 순환을 원활하게 해줍니다."
            )
            reward_exp = int(80 * multiplier)
        else:
            dialogue = (
                f"오늘 조금 피곤하셨죠? 괜찮아요, {self.spirit_name}(이)가 곁에서 든든하게 응원할게요.\n"
                f"💡 꿀팁: 무리한 운동보다는 5분간 깊은 호흡과 함께 편안한 휴식을 취해 보세요."
            )
            reward_exp = int(50 * multiplier)

        return {
            "spirit_name": self.spirit_name,
            "dialogue_text": dialogue,
            "dynamic_multiplier": multiplier,
            "reward_exp": reward_exp,
            "is_fallback_applied": is_fallback
        }


if __name__ == "__main__":
    # 모듈 자체 검증 및 테스트
    manager = UserFriendlyDialogueManagerV3(spirit_name="파이론")
    sample_data = {
        "hrv": 65.0,
        "meal_interval_hours": 4.2,
        "hydration_ratio": 1.1,
        "rpe": 5.0
    }
    result = manager.generate_friendly_tip(sample_data)
    print("=== 검증 결과 ===")
    print(f"가중치: {result['dynamic_multiplier']}")
    print(f"보상 경험치: {result['reward_exp']}")
    print(f"대화 및 팁:\n{result['dialogue_text']}")