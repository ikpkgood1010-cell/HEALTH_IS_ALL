# -*- coding: utf-8 -*-
"""
File Path: HEALTH IS ALL/04_FRONTEND/health_tip_ui_controller_v1.py
Description:
    'HEALTH IS ALL' V1 팁 UI 애니메이션 컨트롤러.
    HEALTH_TIP_UI_ANIMATION_SPEC_V1.mdux 규격을 준수하여 팝업, 타자기 효과,
    정령 모션 및 보상 파티클 트랜지션을 관리합니다.
"""

import time
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HealthTipUIControllerV1")

class HealthTipUIControllerV1:
    def __init__(self):
        self.state = "HIDDEN"
        self.current_tip_data = None

    def trigger_tip_popup(self, api_response: Dict[str, Any]) -> None:
        """
        백엔드 API 응답 전달받아 UI 애니메이션 시퀀스 개시
        """
        if not api_response.get("success", False):
            logger.error("[UI Controller] API 응답이 올바르지 않습니다.")
            return

        self.current_tip_data = api_response["data"]
        
        # 1. ENTERING 상태
        self.state = "ENTERING"
        logger.info(f"[UI State: {self.state}] 말풍선 스케일업(Ease-Out Back 250ms) 및 정령 반짝임 연출")
        
        # 2. READING 상태 (타자기 효과 시뮬레이션)
        self.state = "READING"
        tip_text = self.current_tip_data["dialogue_bubble"]["text"]
        logger.info(f"[UI State: {self.state}] 텍스트 타자기 연출 시작 (글자당 15ms)")
        print(f"\n--- [정령 말풍선 UI 출력] ---")
        print(tip_text)
        print("------------------------------\n")

    def handle_user_tap(self) -> Dict[str, Any]:
        """
        사용자가 말풍선을 터치했을 때 보상 연출 및 종료 처리
        """
        if self.state != "READING":
            logger.warning("[UI Controller] 터치할 수 없는 상태입니다.")
            return {"status": "IGNORED"}

        # 3. REWARDING 상태
        self.state = "REWARDING"
        rewards = self.current_tip_data["rewards"]
        logger.info(
            f"[UI State: {self.state}] 파티클 이펙트 발동! "
            f"(정령 친밀도 +{rewards['spirit_affinity_bonus']}, 골드 +{rewards['micro_gold']})"
        )

        # 4. EXITING 상태
        self.state = "EXITING"
        logger.info(f"[UI State: {self.state}] 말풍선 Fade-Out 및 화면 정리 완료")
        
        self.state = "HIDDEN"
        return {
            "status": "COMPLETED",
            "claimed_rewards": rewards
        }


# 인터랙션 시뮬레이션 테스트
if __name__ == "__main__":
    controller = HealthTipUIControllerV1()

    # API 응답 가상 데이터
    mock_api_response = {
        "success": True,
        "data": {
            "user_id": "USER_7701",
            "dialogue_bubble": {
                "text": "오늘 수분 섭취가 조금 부족해요!\n따뜻한 물 한 잔으로 몸도 정령도 촉촉하게 채워볼까요?",
                "line_count": 2,
                "style": "FRIENDLY_POPUP"
            },
            "rewards": {
                "spirit_affinity_bonus": 2,
                "micro_gold": 5
            }
        }
    }

    # 1. 팝업 트리거
    controller.trigger_tip_popup(mock_api_response)

    # 2. 사용자 터치 반응 시뮬레이션
    time.sleep(0.5)
    tap_result = controller.handle_user_tap()
    print(f"터치 결과: {tap_result}")