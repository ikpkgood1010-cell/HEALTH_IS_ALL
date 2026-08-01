# -*- coding: utf-8 -*-
"""
File Path: HEALTH IS ALL/03_BACKEND/health_dynamic_tip_feeder_v3.py
Description:
    'HEALTH IS ALL' 다변수 정밀 계산 기반 1~3줄 맞춤형 건강/식단 꿀팁 동적 피딩 엔진.
    사용자 친화적 톤앤매너 가공 및 Fallback 알고리즘 내장.
"""

import math
import logging
from typing import Dict, Any, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HealthDynamicTipFeederV3")

class HealthDynamicTipFeederV3:
    def __init__(self):
        # 다변수 동적 공식 가중치
        self.alpha = 0.35  # 건강점수 결핍 가중치
        self.beta = 0.25   # 수분 결핍 가중치
        self.gamma = 0.25  # 수면/회복 미달 가중치
        self.delta = 0.15  # 정령 상태 가중치

        # 팁 라이브러리 (친화적 문구 적용)
        self.tip_database = {
            "hydration": [
                "오늘 수분 섭취가 조금 부족해요! 따뜻한 물 한 잔으로 몸을 한결 가볍게 만들어볼까요?",
                "수분이 채워지면 정령도 한층 더 반짝여요. 지금 바로 시원한 물 한 잔 챙겨드세요!"
            ],
            "diet_steamed": [
                "정제 탕류나 튀김 대신, 오늘은 따뜻하게 찌거나 삶은 담백한 건강식을 즐겨보세요!",
                "자극적인 양념을 살짝 줄이고 식재료 본연의 맛을 느끼면 몸이 정말 좋아해요."
            ],
            "recovery": [
                "오늘 회복 지수가 조금 낮네요. 가벼운 스트레칭과 깊은 숨으로 몸을 다독여주세요.",
                "지친 하루 끝에는 수면 환경을 아늑하게 조성하고 편안한 휴식을 취해볼까요?"
            ],
            "general": [
                "오늘도 건강한 하루를 향해 나아가는 당신의 모습을 정령이 항상 응원하고 있어요!",
                "작은 건강 습관 하나가 모여 내일의 거대한 활력이 됩니다. 함께 힘내봐요!"
            ]
        }

    def calculate_priority_score(self, health_data: Dict[str, Any]) -> Tuple[float, str]:
        """
        다변수 세분화 계산 공식을 통한 우선순위 점수 산출
        오류 또는 데이터 부족 시 1단계 간결 수식(Fallback)으로 자동 전환
        """
        try:
            h_score = float(health_data.get("health_score", 70.0))
            delta_hydration = float(health_data.get("hydration_deficit_ratio", 0.0)) # 0.0 ~ 1.0
            s_recovery = float(health_data.get("sleep_recovery_index", 1.0))         # 0.0 ~ 1.0
            psi_spirit = float(health_data.get("spirit_mood_weight", 1.0))          # 0.8 ~ 1.2

            # 입력값 범위 검증
            if not (0 <= h_score <= 100 and 0.0 <= delta_hydration <= 1.0 and 0.0 <= s_recovery <= 1.0):
                raise ValueError("입력 데이터 범위를 벗어났습니다.")

            # 정밀 세분화 수식 연산
            score = (
                self.alpha * (100.0 - h_score) +
                self.beta * (delta_hydration * 100.0) +
                self.gamma * ((1.0 - s_recovery) * 100.0) +
                self.delta * (psi_spirit * 10.0)
            )
            return round(score, 2), "PRECISION"

        except Exception as e:
            logger.warning(f"[Fallback Triggered] 원인: {e}. 1단계 간결 공식으로 전환합니다.")
            # 1단계 간결 수식 (Fallback)
            h_score = float(health_data.get("health_score", 70.0))
            delta_hydration = float(health_data.get("hydration_deficit_ratio", 0.0))
            simple_score = (100.0 - h_score) * 0.6 + (delta_hydration * 40.0)
            return round(simple_score, 2), "FALLBACK"

    def select_and_format_tip(self, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        우선순위에 따른 맞춤형 팁 선정 및 친화적 응답 가공
        """
        score, mode = self.calculate_priority_score(health_data)
        
        delta_hydration = health_data.get("hydration_deficit_ratio", 0.0)
        s_recovery = health_data.get("sleep_recovery_index", 1.0)
        sugar_high = health_data.get("sugar_intake_exceeded", False)

        # 팁 카테고리 선정
        if delta_hydration >= 0.3:
            category = "hydration"
            tip_text = self.tip_database["hydration"][0]
        elif sugar_high or health_data.get("prefer_steamed_diet", False):
            category = "diet_steamed"
            tip_text = self.tip_database["diet_steamed"][0]
        elif s_recovery < 0.6:
            category = "recovery"
            tip_text = self.tip_database["recovery"][0]
        else:
            category = "general"
            tip_text = self.tip_database["general"][0]

        return {
            "status": "SUCCESS",
            "calculation_mode": mode,
            "priority_score": score,
            "category": category,
            "tip_message": tip_text,
            "game_reward": {
                "spirit_affinity_bonus": 2,
                "micro_gold": 5
            },
            "ui_display_config": {
                "auto_line_break": True,
                "max_lines": 3,
                "style": "FRIENDLY_POPUP"
            }
        }

# 단체 테스트 코드
if __name__ == "__main__":
    feeder = HealthDynamicTipFeederV3()
    
    # 정상 케이스
    sample_data = {
        "health_score": 62.5,
        "hydration_deficit_ratio": 0.45,
        "sleep_recovery_index": 0.5,
        "spirit_mood_weight": 1.1,
        "sugar_intake_exceeded": True
    }
    result = feeder.select_and_format_tip(sample_data)
    print("=== [정상 계산 결과] ===")
    print(f"모드: {result['calculation_mode']} | 점수: {result['priority_score']}")
    print(f"꿀팁 메시지:\n{result['tip_message']}\n")

    # 오류 상황 (Fallback 동작 확인)
    corrupted_data = {"health_score": "INVALID_VALUE"}
    fallback_result = feeder.select_and_format_tip(corrupted_data)
    print("=== [Fallback 계산 결과] ===")
    print(f"모드: {fallback_result['calculation_mode']} | 점수: {fallback_result['priority_score']}")
    print(f"꿀팁 메시지:\n{fallback_result['tip_message']}")