"""Run the layer-zero candidate economy through 30 deterministic rebirths."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.constellation_economy import (
    REBIRTH_MINIMUM_FLOOR,
    layer_zero_branch,
    rebirth_star_shards,
    run_power_multiplier,
)
from backend.idle_battle_engine import advance_battle


HERO_ORDER = ("TANKER", "WARRIOR", "MAGE", "ARCHER", "ROGUE", "HEALER")
SETTLEMENT_SECONDS = 15 * 60
REBIRTH_COUNT = 30


def simulate() -> dict:
    recruited = {"TANKER"}
    star_shards = 0
    total_hours = 0.0
    run_results = []

    for run_number in range(1, REBIRTH_COUNT + 1):
        floor_number = 1
        room_position = 1
        carry_seconds = 0.0
        gold = 0
        unlocked: set[str] = set()
        run_seconds = 0

        for _ in range(4 * 24 * 30):  # hard guard: 30 days per run
            small_count = sum(code.split("_")[-1].startswith("S") for code in unlocked)
            medium_count = sum(code.split("_")[-1].startswith("M") for code in unlocked)
            battle = advance_battle(
                tower_floor=floor_number,
                room_position=room_position,
                carry_seconds=carry_seconds,
                elapsed_seconds=SETTLEMENT_SECONDS,
                advancement_tiers=[0] * len(recruited),
                run_power_multiplier=run_power_multiplier(
                    small_nodes=small_count,
                    medium_nodes=medium_count,
                ),
            )
            floor_number = battle.end_floor
            room_position = battle.end_room
            carry_seconds = battle.carry_seconds
            gold += battle.gold_earned
            run_seconds += SETTLEMENT_SECONDS

            # Focus one branch at a time so every completed path creates a
            # visible party-size milestone instead of five half-built branches.
            branch_order = (
                [code for code in HERO_ORDER if code not in recruited]
                + [code for code in HERO_ORDER if code in recruited and code != "TANKER"]
            )
            for hero_code in branch_order:
                branch = layer_zero_branch(hero_code)
                while True:
                    next_node = next(
                        (node for node in branch if node.node_code not in unlocked),
                        None,
                    )
                    if next_node is None:
                        recruited.add(hero_code)
                        break
                    if gold < next_node.gold_cost:
                        break
                    gold -= next_node.gold_cost
                    unlocked.add(next_node.node_code)
                if any(node.node_code not in unlocked for node in branch):
                    break

            if floor_number >= REBIRTH_MINIMUM_FLOOR:
                break
        else:
            raise RuntimeError("candidate economy failed to reach rebirth within 30 days")

        earned_shards = rebirth_star_shards(floor_number)
        star_shards += earned_shards
        total_hours += run_seconds / 3600
        run_results.append(
            {
                "run": run_number,
                "hours": round(run_seconds / 3600, 2),
                "floor": floor_number,
                "recruited_heroes": len(recruited),
                "run_nodes": len(unlocked),
                "unspent_gold_reset": gold,
                "star_shards_earned": earned_shards,
                "star_shards_total": star_shards,
            }
        )

    return {
        "status": "LAYER_ZERO_BALANCE_CANDIDATE",
        "rebirths": REBIRTH_COUNT,
        "total_hours": round(total_hours, 2),
        "average_hours_per_rebirth": round(total_hours / REBIRTH_COUNT, 2),
        "all_six_recruited_on_run": next(
            result["run"] for result in run_results if result["recruited_heroes"] == 6
        ),
        "star_shards_total": star_shards,
        "runs": run_results,
    }


def main() -> None:
    print(json.dumps(simulate(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
