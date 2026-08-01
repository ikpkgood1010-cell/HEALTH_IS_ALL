# -*- coding: utf-8 -*-
"""
File Path: HEALTH IS ALL/03_BACKEND/api_tip_feeder_router_v3.py
Description:
    'HEALTH IS ALL' V3 동적 팁 피더 API 라우터.
    사용자 친화적 다이얼로그 매니저(user_friendly_dialogue_manager_v3)와 연동되어
    최종 1~3줄 맞춤형 꿀팁 및 마이크로 게임 보상을 클라이언트에 전달합니다.
"""

import logging
from typing import Dict, Any
from health_dynamic_tip_feeder_v3 import HealthDynamicTipFeederV3

logger = logging.getLogger("ApiTipFeederRouterV3")

class ApiTipFeederRouterV3:
    def __init__(self):
        self.feeder_engine = HealthDynamicTipFeederV3()

    def handle_tip_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        클라이언트 요청 처리 엔드포인트
        :param payload: 사용자 데이터 및 앱 상태 정보
        :return: UI 서빙용 가공 결과 JSON
        """
        user_id = payload.get("user_id", "UNKNOWN_USER")
        health_data = payload.get("health_data", {})

        logger.info(f"[API Request] Tip generation requested for User: {user_id}")

        # 1. 동적 팁 산출 및 톤앤매너 가공
        tip_result = self.feeder_engine.select_and_format_tip(health_data)

        # 2. 클라이언트 전달용 최종 데이터 패키징
        response_payload = {
            "success": True,
            "data": {
                "user_id": user_id,
                "engine_version": "V3.0.0",
                "mode": tip_result["calculation_mode"],
                "score": tip_result["priority_score"],
                "category": tip_result["category"],
                "dialogue_bubble": {
                    "text": tip_result["tip_message"],
                    "line_count": len(tip_result["tip_message"].split("\n")),
                    "style": tip_result["ui_display_config"]["style"]
                },
                "rewards": tip_result["game_reward"]
            }
        }

        return response_payload


# 통합 테스트
if __name__ == "__main__":
    router = ApiTipFeederRouterV3()

    # 식단 및 수분 섭취 시뮬레이션 데이터
    request_data = {
        "user_id": "USER_7701",
        "health_data": {
            "health_score": 68.0,
            "hydration_deficit_ratio": 0.40,
            "sleep_recovery_index": 0.85,
            "spirit_mood_weight": 1.0,
            "sugar_intake_exceeded": False,
            "prefer_steamed_diet": True
        }
    }

    response = router.handle_tip_request(request_data)
    print("=== [API 라우터 반환 데이터 시뮬레이션] ===")
    print(f"사용자 ID: {response['data']['user_id']}")
    print(f"계산 모드: {response['data']['mode']} (점수: {response['data']['score']})")
    print(f"말풍선 출력:\n{response['data']['dialogue_bubble']['text']}")
    print(f"보상: 정령 친밀도 +{response['data']['rewards']['spirit_affinity_bonus']}, 골드 +{response['data']['rewards']['micro_gold']}")