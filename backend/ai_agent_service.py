"""AI-style feedback service without vendor lock-in."""
from __future__ import annotations

from typing import Any, Dict

from backend.config import utc_now


class HealthIAgentService:
    def __init__(self) -> None:
        self.agent_name = "건강이"

    def generate_feedback(
        self,
        consumed_calories: int,
        target_calories: int,
        workout_minutes: int,
        water_liters: float,
        streak_days: int,
    ) -> Dict[str, Any]:
        try:
            calorie_ratio = consumed_calories / max(target_calories, 1)
            workout_score = min(workout_minutes / 40.0, 1.0)
            water_score = min(water_liters / 2.0, 1.0)
            calorie_score = max(0.0, 1.0 - abs(1.0 - calorie_ratio))
            total_score = (workout_score * 0.4) + (water_score * 0.3) + (calorie_score * 0.3)

            if total_score >= 0.85:
                emotion = "최고의 행복"
                dialogue = f"연속 {streak_days}일째 정말 멋져요. 오늘도 건강한 흐름을 잘 이어가고 있어요!"
            elif total_score >= 0.60:
                emotion = "활기참"
                dialogue = "좋아요. 수분과 가벼운 활동을 조금만 더 챙기면 더 안정적이에요."
            elif total_score >= 0.30:
                emotion = "평온함"
                dialogue = "무리하지 않아도 괜찮아요. 물 한 잔과 짧은 스트레칭부터 시작해봐요."
            else:
                emotion = "응원함"
                dialogue = "지금부터 다시 시작하면 충분해요. 가장 쉬운 건강 행동 하나만 기록해볼까요?"

            return {
                "agent_name": self.agent_name,
                "emotion_state": emotion,
                "dialogue": dialogue,
                "health_score": round(total_score * 100, 1),
                "timestamp": utc_now().isoformat(),
            }
        except Exception:
            return {
                "agent_name": self.agent_name,
                "emotion_state": "평온함",
                "dialogue": "오늘도 차분하게 건강 루틴을 이어가요.",
                "health_score": 50.0,
                "timestamp": utc_now().isoformat(),
            }
