"""Deterministic long-horizon projection for all six permanent advancements."""
from __future__ import annotations

import json
import sys
from math import ceil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.advancement_economy import ADVANCEMENT_NAMES, advancement_spec
from backend.health_essence_service import DAILY_HEALTH_ESSENCE_CAP


def simulate() -> dict:
    tiers = []
    cumulative_essence = 0
    cumulative_shards = 0
    for tier in range(1, 7):
        specs = [advancement_spec(hero_code, tier) for hero_code in ADVANCEMENT_NAMES]
        tier_essence = sum(spec.health_essence_cost for spec in specs)
        tier_shards = sum(spec.star_shard_cost for spec in specs)
        cumulative_essence += tier_essence
        cumulative_shards += tier_shards
        tiers.append(
            {
                "tier": tier,
                "health_essence_for_six": tier_essence,
                "star_shards_for_six": tier_shards,
                "cumulative_health_days_at_cap": ceil(
                    cumulative_essence / DAILY_HEALTH_ESSENCE_CAP
                ),
                "cumulative_rebirths": cumulative_shards,
            }
        )
    return {
        "status": "ADVANCEMENT_BALANCE_CANDIDATE",
        "daily_health_essence_cap": DAILY_HEALTH_ESSENCE_CAP,
        "all_six_total_health_essence": cumulative_essence,
        "all_six_total_star_shards": cumulative_shards,
        "minimum_days_at_daily_cap": ceil(
            cumulative_essence / DAILY_HEALTH_ESSENCE_CAP
        ),
        "tiers": tiers,
    }


if __name__ == "__main__":
    print(json.dumps(simulate(), ensure_ascii=False, indent=2))
