from backend.game_balance_engine import build_game_overview, calculate_hbi, dungeon_room_type


def test_hbi_uses_minimum_and_average_formula():
    # minimum 40 * .6 + average 65 * .4 = 50
    assert calculate_hbi([90, 50, 40, 80]) == 50.0


def test_low_hbi_is_non_punitive():
    overview = build_game_overview(
        level=1,
        current_exp=0,
        calories=0,
        target_calories=2000,
        workout_minutes=0,
        target_workout_minutes=45,
        water_liters=0,
        target_water_liters=2,
        streak_days=0,
    )
    assert overview.environment_type == "RESTING_MIST"
    assert overview.reward_multiplier == 1.0
    assert overview.tower_floor >= 1


def test_room_distribution_guardrails():
    assert dungeon_room_type(99, position=0, room_count=8) == "COMBAT"
    assert dungeon_room_type(10, position=7, room_count=8) == "BOSS"
    assert dungeon_room_type(10, position=6, room_count=8) == "REST"
    assert dungeon_room_type(11, position=6, room_count=8) == "SHOP"
    assert dungeon_room_type(0, position=3, room_count=8) == "COMBAT"
    assert dungeon_room_type(55, position=3, room_count=8) == "EVENT"
