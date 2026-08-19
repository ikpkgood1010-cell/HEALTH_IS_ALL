from backend.advancement_economy import advancement_node_code, advancement_spec
from backend.health_essence_service import health_essence_candidate
from scripts.simulate_advancement_economy import simulate


def test_canonical_names_and_costs_are_deterministic():
    assert advancement_spec("TANKER", 1).name == "수호자"
    assert advancement_spec("WARRIOR", 6).name == "초신성 검신"
    assert advancement_spec("HEALER", 6).name == "은하의 구원자"
    assert advancement_spec("MAGE", 1).health_essence_cost == 12
    assert advancement_spec("MAGE", 6).health_essence_cost == 384
    assert advancement_spec("MAGE", 2).star_shard_cost == 2
    assert advancement_node_code("rogue", 4) == "L4_ADVANCE_ROGUE"


def test_health_rewards_are_bounded_and_not_calorie_or_step_scaled():
    assert health_essence_candidate("workout_log", 9) == 0
    assert health_essence_candidate("workout_log", 30) == 2
    assert health_essence_candidate("workout_log", 600) == 3
    assert health_essence_candidate("meal_log", 2000) == 1
    assert health_essence_candidate("water_log", 0.1) == 0
    assert health_essence_candidate("water_log", 0.25) == 1


def test_six_hero_projection_preserves_long_term_growth():
    result = simulate()
    assert result["all_six_total_health_essence"] == 4536
    assert result["all_six_total_star_shards"] == 180
    assert result["minimum_days_at_daily_cap"] == 567
