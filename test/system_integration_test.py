"""
HEALTH IS ALL - End-to-End System Pipeline Integration Test
Execution: pytest test/system_integration_test.py
"""

import pytest
from datetime import datetime, timedelta
from backend.health_calculator import DynamicHealthCalculator
from backend.diet_calculator import DynamicDietCalculator
from backend.ai_agent_service import HealthIAgentService
from backend.quest_engine import DynamicQuestEngine
from backend.progression_engine import ProgressionEngine


def test_full_health_to_game_pipeline():
    """건강 기록 입력 -> 동적 계산 -> Exp 부여 -> AI 코칭 생성 -> 퀘스트 보상 검증"""

    # 1. 모듈 초기화
    workout_calc = DynamicHealthCalculator()
    diet_calc = DynamicDietCalculator()
    progression = ProgressionEngine()
    ai_agent = HealthIAgentService()
    quest_engine = DynamicQuestEngine()

    # 2. 운동 칼로리 및 식단 포만감 연산
    burned_cals = workout_calc.calculate_workout_calories("running", 30.0, 70.0, "vigorous")
    diet_analysis = diet_calc.analyze_meal_quality(600.0, carbs=70, protein=35, fat=15, fiber=8)

    assert burned_cals > 200.0
    assert diet_analysis["quality_score"] > 70.0

    # 3. ProgressionEngine Exp 계산 (상한선 300 유지)
    engine_res = progression.calculate_exp_gain(
        action_type="workout_log",
        current_daily_exp=100,
        last_action_time=None
    )
    assert engine_res["exp_gained"] == 50
    assert engine_res["current_daily_exp"] == 150

    # 4. AI '건강이' 피드백 생성
    feedback = ai_agent.generate_feedback(
        consumed_calories=1500,
        target_calories=2000,
        workout_minutes=45,
        water_liters=1.8,
        streak_days=3
    )
    assert feedback["agent_name"] == "건강이"
    assert "최고의 행복" in feedback["emotion_state"] or "활기참" in feedback["emotion_state"]

    # 5. 일일 동적 퀘스트 수령
    quests = quest_engine.get_daily_quests(streak_days=3)
    assert len(quests) == 3
    assert quests[0]["reward_exp"] >= 40
