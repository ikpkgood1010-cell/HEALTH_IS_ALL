"""Pure candidate economy for run-scoped constellation paths.

The latest canonical loop spends run-only gold on SMALL/MEDIUM nodes. Completing
one layer-zero branch makes that hero's permanent LARGE recruitment node
available without random selection or another currency charge.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import ceil, floor, pow


LAYER_ZERO_SMALL_COUNT = 6
LAYER_ZERO_MEDIUM_COUNT = 2
SMALL_POWER_BONUS = 0.02
MEDIUM_POWER_BONUS = 0.05
BASE_NODE_GOLD = 1500
NODE_COST_GROWTH = 1.15
MEDIUM_COST_MULTIPLIER = 3.0
REBIRTH_MINIMUM_FLOOR = 100


@dataclass(frozen=True)
class RunNodeSpec:
    node_code: str
    hero_code: str
    layer: int
    node_size: str
    sequence: int
    gold_cost: int
    title: str
    effect_label: str


def layer_zero_branch(hero_code: str) -> tuple[RunNodeSpec, ...]:
    """Return SMALL×3 → MEDIUM → SMALL×3 → MEDIUM for one hero."""
    normalized = hero_code.strip().upper()
    sizes = ("SMALL", "SMALL", "SMALL", "MEDIUM", "SMALL", "SMALL", "SMALL", "MEDIUM")
    small_index = 0
    medium_index = 0
    result: list[RunNodeSpec] = []
    for sequence, size in enumerate(sizes, start=1):
        if size == "SMALL":
            small_index += 1
            ordinal = small_index
            multiplier = 1.0
            title = f"기초 단련 {ordinal}"
            effect = "이번 회차 파티 전투력 +2%"
        else:
            medium_index += 1
            ordinal = medium_index
            multiplier = MEDIUM_COST_MULTIPLIER
            title = f"성장의 이정표 {ordinal}"
            effect = "이번 회차 파티 전투력 +5%"
        raw_cost = BASE_NODE_GOLD * pow(NODE_COST_GROWTH, sequence - 1) * multiplier
        result.append(
            RunNodeSpec(
                node_code=f"L0_{normalized}_{size[0]}{ordinal:02d}",
                hero_code=normalized,
                layer=0,
                node_size=size,
                sequence=sequence,
                gold_cost=max(1, ceil(raw_cost / 10) * 10),
                title=title,
                effect_label=effect,
            )
        )
    return tuple(result)


def next_branch_node(
    hero_code: str,
    unlocked_node_codes: set[str] | frozenset[str],
) -> RunNodeSpec | None:
    return next(
        (
            node
            for node in layer_zero_branch(hero_code)
            if node.node_code not in unlocked_node_codes
        ),
        None,
    )


def run_power_multiplier(*, small_nodes: int, medium_nodes: int) -> float:
    return 1.0 + max(0, small_nodes) * SMALL_POWER_BONUS + max(0, medium_nodes) * MEDIUM_POWER_BONUS


def rebirth_star_shards(tower_floor: int) -> int:
    """Candidate prestige reward with slow sublinear growth from floor 100."""
    if tower_floor < REBIRTH_MINIMUM_FLOOR:
        return 0
    return max(1, floor(pow(tower_floor / REBIRTH_MINIMUM_FLOOR, 0.75)))


def branch_total_gold(hero_code: str) -> int:
    return sum(node.gold_cost for node in layer_zero_branch(hero_code))
