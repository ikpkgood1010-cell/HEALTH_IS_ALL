# -*- coding: utf-8 -*-
"""
File Path: HEALTH IS ALL/03_BACKEND/health_push_scheduler_v1.py
Description:
    'HEALTH IS ALL' V1 맞춤형 팁 푸시 알림 동적 스케줄러.
    HEALTH_PUSH_SCHEDULER_SPEC_V1.mdux 규격을 준수하며,
    사용자 상태 계산 후 80자 이내 1~3줄 푸시 메세지를 발송합니다.
"""

import datetime
import logging
from typing import Dict, Any
from health_dynamic_tip_feeder_v3 import HealthDynamicTipFeederV3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HealthPushSchedulerV1")

class HealthPushSchedulerV1:
    def __init__(self):
        self.feeder_engine = HealthDynamicTipFeederV3()
        # 야간 방해 금지 시간 (22:30 ~ 07:00)
        self.quiet_start_hour = 22
        self.quiet_start_min = 30
        self.quiet_end_hour = 7

    def is_quiet_hours(self, current_time: datetime.datetime) -> bool:
        """현재 시간이 야간 방해 금지 시간대인지 검사"""
        hour = current_time.hour
        minute = current_time.minute

        if hour > self.quiet_start_hour or (hour == self.quiet_start_hour and minute >= self.quiet_start_min):
            return True
        if hour < self.quiet_end_hour:
            return True
        return False

    def process_user_push_schedule(self, user_id: str, health_data: Dict[str, Any], now: datetime.datetime = None) -> Dict[str, Any]:
        """
        사용자 상태 검사 후 푸시 알림 메시지 생성 및 발송
        """
        if now is None:
            now = datetime.datetime.now()

        # 1. 야간 방해 금지 시간 체크
        if self.is_quiet_hours(now):
            logger.info(f"[Push Muted] 사용자 {user_id}: 야간 방해 금지 시간대({now.strftime('%H:%M')})로 푸시가 차단되었습니다.")
            return {"status": "SLEEP_MUTE", "reason": "Quiet Hours Active"}

        # 2. 동적 팁 계산
        tip_result = self.feeder_engine.select_and_format_tip(health_data)
        raw_message = tip_result["tip_message"]

        # 3. 푸시 알림용 80자/3줄 이내 가공
        push_message = raw_message[:80]

        # 4. 푸시 발송 시뮬레이션
        push_payload = {
            "title": "✨ 정령이 보내온 오늘의 꿀팁!",
            "body": push_message,
            "data": {
                "category": tip_result["category"],
                "reward_affinity": tip_result["game_reward"]["spirit_affinity_bonus"],
                "reward_gold": tip_result["game_reward"]["micro_gold"]
            }
        }

        logger.info(f"[Push Dispatched] 사용자 {user_id}에게 푸시 알림을 성공적으로 발송했습니다.")
        return {
            "status": "DISPATCHED",
            "timestamp": now.isoformat(),
            "user_id": user_id,
            "push_payload": push_payload
        }


# 백그라운드 크론 시뮬레이션 테스트
if __name__ == "__main__":
    scheduler = HealthPushSchedulerV1()

    # 테스트 유저 데이터
    sample_user_health = {
        "health_score": 58.0,
        "hydration_deficit_ratio": 0.55,
        "sleep_recovery_index": 0.4,
        "spirit_mood_weight": 1.2
    }

    print("=== [주간 정상 시간대 푸시 테스트 (오후 3:30)] ===")
    day_time = datetime.datetime(2026, 7, 31, 15, 30)
    res_day = scheduler.process_user_push_schedule("USER_7701", sample_user_health, day_time)
    print(f"발송 상태: {res_day['status']}")
    if res_day['status'] == "DISPATCHED":
        print(f"제목: {res_day['push_payload']['title']}")
        print(f"내용:\n{res_day['push_payload']['body']}\n")

    print("=== [야간 방해금지 시간대 푸시 테스트 (밤 11:15)] ===")
    night_time = datetime.datetime(2026, 7, 31, 23, 15)
    res_night = scheduler.process_user_push_schedule("USER_7701", sample_user_health, night_time)
    print(f"발송 상태: {res_night['status']} (사유: {res_night.get('reason')})\n")