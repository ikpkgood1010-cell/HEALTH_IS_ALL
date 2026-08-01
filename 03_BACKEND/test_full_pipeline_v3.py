# -*- coding: utf-8 -*-
"""
File Path: HEALTH IS ALL/03_BACKEND/test_full_pipeline_v3.py
Description:
    'HEALTH IS ALL' V3 전체 시스템 통합 E2E 테스트 스크립트.
    모든 .mdux 규격과 구현 모듈(.py)의 정상 연동을 종합 검증합니다.
"""

import datetime
import logging
from api_tip_feeder_router_v3 import ApiTipFeederRouterV3
from health_tip_ui_controller_v1 import HealthTipUIControllerV1
from health_push_scheduler_v1 import HealthPushSchedulerV1

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FullPipelineTestV3")

def run_integration_test():
    logger.info("=== [HEALTH IS ALL V3 통합 파이프라인 테스트 시작] ===")

    # 1. 모듈 초기화
    api_router = ApiTipFeederRouterV3()
    ui_controller = HealthTipUIControllerV1()
    push_scheduler = HealthPushSchedulerV1()

    # 2. 정상 시나리오 테스트 (식단/수분 결핍)
    print("\n--- 시나리오 1: 정상 API 요청 및 인앱 UI 출력 ---")
    payload = {
        "user_id": "USER_7701",
        "health_data": {
            "health_score": 62.0,
            "hydration_deficit_ratio": 0.45,
            "sleep_recovery_index": 0.5,
            "spirit_mood_weight": 1.1,
            "prefer_steamed_diet": True
        }
    }
    
    # 백엔드 API 연산
    api_response = api_router.handle_tip_request(payload)
    assert api_response["success"] is True, "API 요청 실패"
    
    # 프론트엔드 UI 및 애니메이션 제어
    ui_controller.trigger_tip_popup(api_response)
    tap_result = ui_controller.handle_user_tap()
    assert tap_result["status"] == "COMPLETED", "UI 보상 수령 실패"

    # 3. Fallback 시나리오 테스트 (손상된 데이터 입력)
    print("\n--- 시나리오 2: 예외 상황 (Fallback 수식 자동 전환) ---")
    corrupted_payload = {
        "user_id": "USER_7701",
        "health_data": {"health_score": -10.0} # invalid value
    }
    fallback_response = api_router.handle_tip_request(corrupted_payload)
    assert fallback_response["data"]["mode"] == "FALLBACK", "Fallback 전환 실패"
    logger.info(f"Fallback 점수 정상 산출: {fallback_response['data']['score']}")

    # 4. 백그라운드 푸시 스케줄러 테스트 (Quiet Hours 및 주간 푸시)
    print("\n--- 시나리오 3: 백그라운드 푸시 스케줄러 검증 ---")
    sample_health = payload["health_data"]
    
    # 주간 푸시
    day_time = datetime.datetime(2026, 7, 31, 14, 0)
    day_push = push_scheduler.process_user_push_schedule("USER_7701", sample_health, day_time)
    assert day_push["status"] == "DISPATCHED", "주간 푸시 발송 실패"
    
    # 야간 푸시 차단 (Quiet Hours)
    night_time = datetime.datetime(2026, 7, 31, 23, 0)
    night_push = push_scheduler.process_user_push_schedule("USER_7701", sample_health, night_time)
    assert night_push["status"] == "SLEEP_MUTE", "야간 방해금지 차단 실패"

    logger.info("\n=== [모든 통합 파이프라인 테스트 성공 완료] ===")

if __name__ == "__main__":
    run_integration_test()