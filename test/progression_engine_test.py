from datetime import timedelta

from backend.config import utc_now

from backend.health_calculator import DynamicHealthCalculator
from backend.progression_engine import ProgressionEngine


def test_daily_exp_cap():
    engine = ProgressionEngine()
    result = engine.calculate_exp_gain(action_type="workout_log", current_daily_exp=280, last_action_time=None)
    assert result["exp_gained"] == 20
    assert result["current_daily_exp"] == 300


def test_anti_farming_10min_rule():
    engine = ProgressionEngine()
    recent_time = utc_now() - timedelta(minutes=5)
    result = engine.calculate_exp_gain(action_type="meal_log", current_daily_exp=50, last_action_time=recent_time)
    assert result["exp_gained"] == 0
    assert "연속 입력 제한" in result["reason"]


def test_dynamic_workout_calorie_calculation():
    calc = DynamicHealthCalculator()
    cals = calc.calculate_workout_calories(workout_type="running", duration_minutes=30, weight_kg=70.0, intensity="vigorous")
    assert cals > 0
    fallback_cals = calc.calculate_workout_calories(workout_type="unknown_type", duration_minutes=30, weight_kg=70.0)
    assert fallback_cals > 0
