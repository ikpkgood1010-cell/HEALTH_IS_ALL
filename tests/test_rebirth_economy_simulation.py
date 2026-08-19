from scripts.simulate_rebirth_economy import simulate


def test_thirty_rebirth_candidate_has_no_gold_or_shard_explosion():
    result = simulate()
    assert result["rebirths"] == 30
    assert result["all_six_recruited_on_run"] == 2
    assert 16 <= result["average_hours_per_rebirth"] <= 24
    assert result["star_shards_total"] == 30
    assert all(run["floor"] >= 100 for run in result["runs"])
    assert max(run["unspent_gold_reset"] for run in result["runs"]) < 10_000
