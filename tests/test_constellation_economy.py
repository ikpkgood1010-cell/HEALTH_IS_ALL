import pytest

from backend.constellation_economy import (
    branch_total_gold,
    layer_zero_branch,
    next_branch_node,
    rebirth_star_shards,
    run_power_multiplier,
)


def test_layer_zero_branch_has_approved_small_medium_sequence():
    branch = layer_zero_branch("MAGE")
    assert [node.node_size for node in branch] == [
        "SMALL",
        "SMALL",
        "SMALL",
        "MEDIUM",
        "SMALL",
        "SMALL",
        "SMALL",
        "MEDIUM",
    ]
    small_costs = [node.gold_cost for node in branch if node.node_size == "SMALL"]
    medium_costs = [node.gold_cost for node in branch if node.node_size == "MEDIUM"]
    assert small_costs == sorted(small_costs)
    assert medium_costs == sorted(medium_costs)
    assert branch[3].gold_cost > branch[2].gold_cost
    assert branch_total_gold("MAGE") == sum(node.gold_cost for node in branch)


def test_branch_progress_and_run_power_are_deterministic():
    branch = layer_zero_branch("ARCHER")
    assert next_branch_node("ARCHER", set()) == branch[0]
    assert next_branch_node(
        "ARCHER", {node.node_code for node in branch}
    ) is None
    assert run_power_multiplier(small_nodes=6, medium_nodes=2) == pytest.approx(1.22)


def test_rebirth_reward_starts_at_floor_100_and_grows_slowly():
    assert rebirth_star_shards(99) == 0
    assert rebirth_star_shards(100) == 1
    assert rebirth_star_shards(199) == 1
    assert rebirth_star_shards(300) == 2
