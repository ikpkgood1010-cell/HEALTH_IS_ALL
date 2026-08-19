from backend.idle_battle_engine import (
    BattleTuning,
    advance_battle,
    calculate_party_power,
    room_required_seconds,
)


def test_party_growth_reduces_time_without_changing_room_order():
    starter_power = calculate_party_power([0])
    full_party_power = calculate_party_power([0, 0, 0, 0, 0, 0])
    advanced_power = calculate_party_power([3, 3, 3, 3, 3, 3])
    assert starter_power == 100
    assert full_party_power == 600
    assert advanced_power > full_party_power
    assert room_required_seconds(
        tower_floor=20, room_position=1, party_power=advanced_power
    ) <= room_required_seconds(
        tower_floor=20, room_position=1, party_power=starter_power
    )


def test_five_normal_rooms_then_boss_advances_floor_deterministically():
    tuning = BattleTuning(
        offline_cap_seconds=1000,
        normal_room_base_seconds=10,
        boss_room_base_seconds=20,
        minimum_room_seconds=1,
        maximum_normal_room_seconds=100,
        maximum_boss_room_seconds=100,
    )
    result = advance_battle(
        tower_floor=1,
        room_position=1,
        carry_seconds=0,
        elapsed_seconds=70,
        advancement_tiers=[0],
        tuning=tuning,
    )
    assert result.rooms_cleared == 6
    assert result.bosses_cleared == 1
    assert result.end_floor == 2
    assert result.end_room == 1
    assert result.gold_earned > 0


def test_offline_time_is_capped_and_partial_room_progress_is_retained():
    tuning = BattleTuning(
        offline_cap_seconds=30,
        normal_room_base_seconds=45,
        minimum_room_seconds=1,
        maximum_normal_room_seconds=100,
    )
    result = advance_battle(
        tower_floor=1,
        room_position=1,
        carry_seconds=5,
        elapsed_seconds=9999,
        advancement_tiers=[0],
        tuning=tuning,
    )
    assert result.credited_seconds == 30
    assert result.rooms_cleared == 0
    assert result.carry_seconds == 35
    assert result.end_floor == 1
    assert result.end_room == 1
