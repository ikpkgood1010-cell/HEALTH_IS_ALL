"""Deterministic automatic-battle math for the canonical idle game.

The values in ``BattleTuning`` are isolated balance candidates, not live economy
promises.  Keeping the engine pure makes it possible to run long simulations
before promoting any value to the canonical balance table.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import ceil, floor, pow


ROOMS_PER_FLOOR = 6
BOSS_ROOM_POSITION = 6


@dataclass(frozen=True)
class BattleTuning:
    offline_cap_seconds: int = 12 * 60 * 60
    base_hero_power: float = 100.0
    advancement_power_per_tier: float = 0.40
    floor_difficulty_growth: float = 1.08
    normal_room_base_seconds: float = 45.0
    boss_room_base_seconds: float = 90.0
    minimum_room_seconds: int = 8
    maximum_normal_room_seconds: int = 120
    maximum_boss_room_seconds: int = 240
    normal_gold_base: float = 8.0
    boss_gold_base: float = 35.0
    gold_floor_exponent: float = 0.70


DEFAULT_TUNING = BattleTuning()


@dataclass(frozen=True)
class BattleAdvance:
    credited_seconds: int
    consumed_seconds: float
    carry_seconds: float
    start_floor: int
    start_room: int
    end_floor: int
    end_room: int
    rooms_cleared: int
    bosses_cleared: int
    gold_earned: int
    party_power: int
    current_room_kind: str
    current_room_required_seconds: int


def calculate_party_power(
    advancement_tiers: list[int] | tuple[int, ...],
    *,
    tuning: BattleTuning = DEFAULT_TUNING,
) -> int:
    """Return power from recruited heroes only; an empty party cannot battle."""
    total = sum(
        tuning.base_hero_power * (1 + max(0, tier) * tuning.advancement_power_per_tier)
        for tier in advancement_tiers
    )
    return max(0, floor(total))


def room_required_seconds(
    *,
    tower_floor: int,
    room_position: int,
    party_power: int,
    tuning: BattleTuning = DEFAULT_TUNING,
) -> int:
    if party_power <= 0:
        raise ValueError("party power must be positive")
    safe_floor = max(1, tower_floor)
    # Limit the exponent defensively. Long-running accounts should remain
    # calculable even before the final late-game curve is approved.
    difficulty = tuning.base_hero_power * pow(
        tuning.floor_difficulty_growth,
        min(safe_floor - 1, 500),
    )
    boss = room_position == BOSS_ROOM_POSITION
    base_seconds = (
        tuning.boss_room_base_seconds if boss else tuning.normal_room_base_seconds
    )
    maximum = (
        tuning.maximum_boss_room_seconds if boss else tuning.maximum_normal_room_seconds
    )
    calculated = ceil(base_seconds * difficulty / party_power)
    return max(tuning.minimum_room_seconds, min(maximum, calculated))


def room_gold_reward(
    *,
    tower_floor: int,
    room_position: int,
    tuning: BattleTuning = DEFAULT_TUNING,
) -> int:
    base = (
        tuning.boss_gold_base
        if room_position == BOSS_ROOM_POSITION
        else tuning.normal_gold_base
    )
    return max(1, floor(base * pow(max(1, tower_floor), tuning.gold_floor_exponent)))


def advance_battle(
    *,
    tower_floor: int,
    room_position: int,
    carry_seconds: float,
    elapsed_seconds: int,
    advancement_tiers: list[int] | tuple[int, ...],
    tuning: BattleTuning = DEFAULT_TUNING,
) -> BattleAdvance:
    """Advance one run deterministically using credited server elapsed time."""
    start_floor = max(1, tower_floor)
    start_room = min(ROOMS_PER_FLOOR, max(1, room_position))
    current_floor = start_floor
    current_room = start_room
    credited = max(0, min(int(elapsed_seconds), tuning.offline_cap_seconds))
    available = max(0.0, carry_seconds) + credited
    initial_available = available
    party_power = calculate_party_power(advancement_tiers, tuning=tuning)
    if party_power <= 0:
        raise ValueError("at least one recruited hero is required")

    rooms_cleared = 0
    bosses_cleared = 0
    gold_earned = 0
    # The cap and minimum room duration already bound this loop. This explicit
    # guard prevents a future tuning mistake from producing an unbounded request.
    max_iterations = tuning.offline_cap_seconds // max(1, tuning.minimum_room_seconds) + 1
    while rooms_cleared < max_iterations:
        required = room_required_seconds(
            tower_floor=current_floor,
            room_position=current_room,
            party_power=party_power,
            tuning=tuning,
        )
        if available < required:
            break
        available -= required
        gold_earned += room_gold_reward(
            tower_floor=current_floor,
            room_position=current_room,
            tuning=tuning,
        )
        rooms_cleared += 1
        if current_room == BOSS_ROOM_POSITION:
            bosses_cleared += 1
            current_floor += 1
            current_room = 1
        else:
            current_room += 1

    current_required = room_required_seconds(
        tower_floor=current_floor,
        room_position=current_room,
        party_power=party_power,
        tuning=tuning,
    )
    # Carry is progress in the current room, so it must never exceed that room.
    safe_carry = min(available, max(0.0, current_required - 1e-6))
    return BattleAdvance(
        credited_seconds=credited,
        consumed_seconds=initial_available - safe_carry,
        carry_seconds=safe_carry,
        start_floor=start_floor,
        start_room=start_room,
        end_floor=current_floor,
        end_room=current_room,
        rooms_cleared=rooms_cleared,
        bosses_cleared=bosses_cleared,
        gold_earned=gold_earned,
        party_power=party_power,
        current_room_kind="BOSS" if current_room == BOSS_ROOM_POSITION else "NORMAL",
        current_room_required_seconds=current_required,
    )
