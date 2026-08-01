"""Core progression and anti-farming logic."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from backend.config import settings, utc_now


class ProgressionEngine:
    def __init__(self) -> None:
        self.daily_exp_cap = settings.DAILY_EXP_CAP
        self.anti_farming_minutes = settings.ANTI_FARMING_INTERVAL_MINUTES
        self.base_exp_map = {
            "meal_log": 30,
            "workout_log": 50,
            "habit_complete": 20,
            "water_log": 10,
        }

    def calculate_exp_gain(
        self,
        action_type: str,
        current_daily_exp: int,
        last_action_time: Optional[datetime] = None,
        streak_days: int = 1,
    ) -> Dict[str, Any]:
        try:
            if last_action_time is not None:
                time_diff = utc_now() - last_action_time
                if time_diff < timedelta(minutes=self.anti_farming_minutes):
                    remaining = timedelta(minutes=self.anti_farming_minutes) - time_diff
                    remain_sec = max(int(remaining.total_seconds()), 0)
                    return {
                        "exp_gained": 0,
                        "current_daily_exp": current_daily_exp,
                        "is_capped": False,
                        "reason": f"연속 입력 제한: {remain_sec // 60}분 {remain_sec % 60}초 후 다시 시도하세요.",
                    }

            if current_daily_exp >= self.daily_exp_cap:
                return {
                    "exp_gained": 0,
                    "current_daily_exp": self.daily_exp_cap,
                    "is_capped": True,
                    "reason": f"오늘의 최대 {self.daily_exp_cap} Exp에 도달했습니다.",
                }

            base_exp = self.base_exp_map.get(action_type, 15)
            # 연속 기록(streak) 보너스는 "이틀째부터" 누적된다.
            # streak_days=1(첫 기록)에는 아직 연속 기록이 성립하지 않으므로 보너스 0%.
            streak_bonus = min(max(streak_days - 1, 0) * 0.02, 0.20)
            calculated_exp = int(round(base_exp * (1.0 + streak_bonus)))
            final_exp = min(calculated_exp, self.daily_exp_cap - current_daily_exp)
            updated_total = current_daily_exp + final_exp
            return {
                "exp_gained": final_exp,
                "current_daily_exp": updated_total,
                "is_capped": updated_total >= self.daily_exp_cap,
                "reason": f"{final_exp} Exp가 반영되었습니다.",
            }
        except Exception:
            safe_gain = min(15, max(self.daily_exp_cap - current_daily_exp, 0))
            return {
                "exp_gained": safe_gain,
                "current_daily_exp": current_daily_exp + safe_gain,
                "is_capped": False,
                "reason": "안전 규칙에 따라 기본 Exp가 반영되었습니다.",
            }

    def update_health_i_status(self, habit_completion_rate: float, last_meal_hours_ago: float) -> Dict[str, str]:
        if habit_completion_rate >= 0.8 and last_meal_hours_ago <= 5.0:
            return {"emotion": "최고의 행복", "dialogue": "정말 훌륭해요. 오늘의 리듬이 아주 안정적이에요!"}
        if habit_completion_rate >= 0.5:
            return {"emotion": "활기참", "dialogue": "좋은 흐름이에요. 가벼운 실천을 하나 더 이어가 볼까요?"}
        return {"emotion": "평온함", "dialogue": "천천히 시작해도 괜찮아요. 작은 기록 하나면 충분해요."}
