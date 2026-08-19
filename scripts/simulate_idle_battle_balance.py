"""Compare provisional idle-battle tuning across 30 equal settlement windows."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.idle_battle_engine import advance_battle


SCENARIOS = {
    "starter_tier_0": [0],
    "full_party_tier_0": [0, 0, 0, 0, 0, 0],
    "full_party_tier_3": [3, 3, 3, 3, 3, 3],
}
WINDOW_SECONDS = 60 * 60
WINDOW_COUNT = 30


def simulate(tiers: list[int]) -> dict:
    tower_floor = 1
    room_position = 1
    carry = 0.0
    total_rooms = 0
    total_bosses = 0
    total_gold = 0
    for _ in range(WINDOW_COUNT):
        result = advance_battle(
            tower_floor=tower_floor,
            room_position=room_position,
            carry_seconds=carry,
            elapsed_seconds=WINDOW_SECONDS,
            advancement_tiers=tiers,
        )
        tower_floor = result.end_floor
        room_position = result.end_room
        carry = result.carry_seconds
        total_rooms += result.rooms_cleared
        total_bosses += result.bosses_cleared
        total_gold += result.gold_earned
    return {
        "settlement_windows": WINDOW_COUNT,
        "hours_per_window": WINDOW_SECONDS // 3600,
        "end_floor": tower_floor,
        "end_room": room_position,
        "rooms_cleared": total_rooms,
        "bosses_cleared": total_bosses,
        "gold_earned": total_gold,
    }


def main() -> None:
    print(
        json.dumps(
            {
                "status": "BALANCE_CANDIDATE_ONLY",
                "warning": (
                    "This is a 30-window combat comparison, not the required "
                    "30-rebirth economy approval simulation."
                ),
                "scenarios": {
                    name: simulate(tiers) for name, tiers in SCENARIOS.items()
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
