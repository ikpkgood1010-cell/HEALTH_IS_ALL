from uuid import UUID
from datetime import datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.database import (
    Base,
    GameConstellationNodeModel,
    GameBattleSettlementModel,
    GameHeroModel,
    GameProfileModel,
    GameRebirthLogModel,
)
from backend.idle_game_service import (
    InitialHeroSelectionConflictError,
    InsufficientPermanentCurrencyError,
    RebirthNotReadyError,
    RebirthRevisionConflictError,
    execute_rebirth,
    get_game_state,
    initialize_game_state,
    preview_rebirth,
    select_initial_hero,
    settle_idle_battle,
    unlock_constellation_node,
)


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


def test_initialization_creates_exactly_six_locked_roles_once(db_session):
    first = initialize_game_state(db_session, user_id="idle_user")
    second = initialize_game_state(db_session, user_id="idle_user")

    assert first == second
    assert first["phase"] == "ONBOARDING"
    assert [hero["role_name"] for hero in first["heroes"]] == [
        "탱커",
        "전사",
        "마법사",
        "궁수",
        "도적",
        "치유사",
    ]
    assert all(hero["recruited"] is False for hero in first["heroes"])
    assert db_session.query(GameProfileModel).count() == 1
    assert db_session.query(GameHeroModel).count() == 6
    assert first["initial_hero_selected"] is False
    assert first["large_node_slots_by_layer"] == {
        "0": 5,
        "1": 6,
        "2": 6,
        "3": 6,
        "4": 6,
        "5": 6,
        "6": 6,
    }


def test_initial_hero_is_free_exactly_once_and_uses_no_large_node(db_session):
    initialize_game_state(db_session, user_id="starter_user")

    selected = select_initial_hero(
        db_session,
        user_id="starter_user",
        hero_code="mage",
        expected_revision=0,
    )
    assert selected["phase"] == "IDLE_BATTLE"
    assert selected["revision"] == 1
    assert selected["initial_hero_selected"] is True
    assert selected["starter_hero_code"] == "MAGE"
    assert selected["node_counts"]["LARGE"] == 0
    assert [
        hero["hero_code"] for hero in selected["heroes"] if hero["recruited"]
    ] == ["MAGE"]
    layer_zero = selected["constellation_layers"][0]
    assert layer_zero["node_count"] == 5
    assert {node["hero_code"] for node in layer_zero["nodes"]} == {
        "TANKER",
        "WARRIOR",
        "ARCHER",
        "ROGUE",
        "HEALER",
    }
    assert {node["state"] for node in layer_zero["nodes"]} == {"LOCKED"}
    first_advancement = selected["constellation_layers"][1]
    assert first_advancement["node_count"] == 6
    assert next(
        node for node in first_advancement["nodes"] if node["hero_code"] == "MAGE"
    )["state"] == "NEXT"

    retry = select_initial_hero(
        db_session,
        user_id="starter_user",
        hero_code="MAGE",
        expected_revision=0,
    )
    assert retry == selected

    with pytest.raises(InitialHeroSelectionConflictError):
        select_initial_hero(
            db_session,
            user_id="starter_user",
            hero_code="HEALER",
            expected_revision=1,
        )


def test_automatic_battle_uses_server_time_and_settles_once(db_session):
    initialize_game_state(db_session, user_id="battle_user")
    select_initial_hero(
        db_session,
        user_id="battle_user",
        hero_code="TANKER",
        expected_revision=0,
    )
    anchor = datetime(2026, 8, 14, 0, 0, 0)
    profile = db_session.query(GameProfileModel).filter_by(user_id="battle_user").one()
    profile.battle_anchor_at = anchor
    db_session.commit()

    settlement_id = UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
    first = settle_idle_battle(
        db_session,
        user_id="battle_user",
        settlement_id=settlement_id,
        now=anchor + timedelta(minutes=10),
    )
    assert first.already_settled is False
    assert first.elapsed_seconds == 600
    assert first.credited_seconds == 600
    assert first.rooms_cleared > 0
    assert first.bosses_cleared > 0
    assert first.gold_earned > 0
    assert first.state["tower_floor"] > 1
    assert first.state["battle"]["party_power"] == 100

    retry = settle_idle_battle(
        db_session,
        user_id="battle_user",
        settlement_id=settlement_id,
        now=anchor + timedelta(days=1),
    )
    assert retry.already_settled is True
    assert retry.gold_earned == first.gold_earned
    assert retry.state == first.state
    assert db_session.query(GameBattleSettlementModel).count() == 1


def test_layer_zero_branch_spends_gold_in_order_then_recruits_permanently(db_session):
    initialize_game_state(db_session, user_id="node_user")
    state = select_initial_hero(
        db_session,
        user_id="node_user",
        hero_code="TANKER",
        expected_revision=0,
    )
    profile = db_session.query(GameProfileModel).filter_by(user_id="node_user").one()
    profile.gold = 100_000
    db_session.commit()
    state = get_game_state(db_session, user_id="node_user")
    warrior_branch = next(
        branch for branch in state["recruitment_branches"]
        if branch["hero_code"] == "WARRIOR"
    )
    spent = 0
    for _ in range(warrior_branch["total_nodes"]):
        next_node = next(
            branch for branch in state["recruitment_branches"]
            if branch["hero_code"] == "WARRIOR"
        )["next_node"]
        spent += next_node["gold_cost"]
        state = unlock_constellation_node(
            db_session,
            user_id="node_user",
            node_code=next_node["node_code"],
            expected_revision=state["revision"],
        )
    ready = next(
        branch for branch in state["recruitment_branches"]
        if branch["hero_code"] == "WARRIOR"
    )
    assert ready["ready_to_recruit"] is True
    assert state["gold"] == 100_000 - spent
    assert state["node_counts"] == {"SMALL": 6, "MEDIUM": 2, "LARGE": 0}
    assert state["battle"]["run_power_multiplier"] == 1.22

    recruited = unlock_constellation_node(
        db_session,
        user_id="node_user",
        node_code=ready["recruit_node_code"],
        expected_revision=state["revision"],
    )
    warrior = next(
        hero for hero in recruited["heroes"] if hero["hero_code"] == "WARRIOR"
    )
    assert warrior["recruited"] is True
    assert recruited["node_counts"]["LARGE"] == 1
    recruited_branch = next(
        branch for branch in recruited["recruitment_branches"]
        if branch["hero_code"] == "WARRIOR"
    )
    assert recruited_branch["hero_recruited"] is True
    assert recruited_branch["branch_complete"] is True


def test_advancement_spends_permanent_currency_and_preserves_class_identity(db_session):
    initialize_game_state(db_session, user_id="advance_user")
    state = select_initial_hero(
        db_session,
        user_id="advance_user",
        hero_code="TANKER",
        expected_revision=0,
    )
    tier_one = next(
        node
        for node in state["constellation_layers"][1]["nodes"]
        if node["hero_code"] == "TANKER"
    )
    assert tier_one["advancement_name"] == "수호자"
    assert tier_one["health_essence_cost"] == 12
    assert tier_one["star_shard_cost"] == 0
    assert tier_one["can_afford"] is False

    profile = db_session.query(GameProfileModel).filter_by(user_id="advance_user").one()
    profile.health_essence = 12
    db_session.commit()
    state = get_game_state(db_session, user_id="advance_user")
    assert next(
        node
        for node in state["constellation_layers"][1]["nodes"]
        if node["hero_code"] == "TANKER"
    )["can_afford"] is True

    advanced = unlock_constellation_node(
        db_session,
        user_id="advance_user",
        node_code="L1_ADVANCE_TANKER",
        expected_revision=state["revision"],
    )
    tanker = next(hero for hero in advanced["heroes"] if hero["hero_code"] == "TANKER")
    assert tanker["advancement_tier"] == 1
    assert tanker["appearance_code"] == "TANKER_TIER_1"
    assert tanker["active_skill_slots"] == 1
    assert advanced["health_essence"] == 0
    assert advanced["node_counts"]["LARGE"] == 1

    assert unlock_constellation_node(
        db_session,
        user_id="advance_user",
        node_code="L1_ADVANCE_TANKER",
        expected_revision=0,
    ) == advanced
    with pytest.raises(InsufficientPermanentCurrencyError):
        unlock_constellation_node(
            db_session,
            user_id="advance_user",
            node_code="L2_ADVANCE_TANKER",
            expected_revision=advanced["revision"],
        )


def test_rebirth_resets_only_run_state_and_is_idempotent(db_session):
    initialize_game_state(db_session, user_id="rebirth_user")
    profile = db_session.query(GameProfileModel).filter_by(user_id="rebirth_user").one()
    profile.tower_floor = 118
    profile.highest_floor = 16
    profile.room_position = 4
    profile.gold = 3200
    profile.health_essence = 41
    profile.star_shards = 7
    profile.transcendence_points = 2
    warrior = db_session.query(GameHeroModel).filter_by(
        user_id="rebirth_user", hero_code="WARRIOR"
    ).one()
    warrior.recruited = True
    warrior.advancement_tier = 3
    warrior.appearance_code = "WARRIOR_TIER_3"
    db_session.add_all(
        [
            GameConstellationNodeModel(
                user_id="rebirth_user",
                node_code="RUN_SMALL_1",
                layer=1,
                node_size="SMALL",
                unlocked_run_number=1,
            ),
            GameConstellationNodeModel(
                user_id="rebirth_user",
                node_code="RUN_MEDIUM_1",
                layer=1,
                node_size="MEDIUM",
                unlocked_run_number=1,
            ),
            GameConstellationNodeModel(
                user_id="rebirth_user",
                node_code="L3_WARRIOR",
                layer=3,
                node_size="LARGE",
                hero_code="WARRIOR",
                unlocked_run_number=1,
            ),
        ]
    )
    db_session.commit()

    preview = preview_rebirth(db_session, user_id="rebirth_user")
    assert preview["can_rebirth"] is True
    assert preview["minimum_floor"] == 100
    assert preview["star_shards_to_earn"] == 1
    assert preview["reset"]["small_nodes"] == 1
    assert preview["reset"]["medium_nodes"] == 1
    assert preview["retain"]["large_nodes"] == 1
    assert preview["retain"]["advancement_tiers"]["WARRIOR"] == 3

    rebirth_id = UUID("11111111-1111-4111-8111-111111111111")
    result = execute_rebirth(
        db_session,
        user_id="rebirth_user",
        expected_revision=0,
        rebirth_id=rebirth_id,
    )
    assert result.already_executed is False
    assert result.state["tower_floor"] == 1
    assert result.state["highest_floor"] == 118
    assert result.state["room_position"] == 1
    assert result.state["gold"] == 0
    assert result.state["run_number"] == 2
    assert result.state["health_essence"] == 41
    assert result.state["star_shards"] == 8
    assert result.state["transcendence_points"] == 2
    assert result.state["node_counts"] == {"SMALL": 0, "MEDIUM": 0, "LARGE": 1}
    retained_warrior = next(
        hero for hero in result.state["heroes"] if hero["hero_code"] == "WARRIOR"
    )
    assert retained_warrior["recruited"] is True
    assert retained_warrior["advancement_tier"] == 3
    assert retained_warrior["appearance_code"] == "WARRIOR_TIER_3"

    retry = execute_rebirth(
        db_session,
        user_id="rebirth_user",
        expected_revision=0,
        rebirth_id=rebirth_id,
    )
    assert retry.already_executed is True
    assert db_session.query(GameRebirthLogModel).count() == 1

    with pytest.raises(RebirthRevisionConflictError):
        execute_rebirth(
            db_session,
            user_id="rebirth_user",
            expected_revision=0,
            rebirth_id=UUID("22222222-2222-4222-8222-222222222222"),
        )


def test_rebirth_blocks_an_empty_run(db_session):
    initialize_game_state(db_session, user_id="empty_run")
    assert preview_rebirth(db_session, user_id="empty_run")["can_rebirth"] is False
    with pytest.raises(RebirthNotReadyError):
        execute_rebirth(
            db_session,
            user_id="empty_run",
            expected_revision=0,
            rebirth_id=UUID("33333333-3333-4333-8333-333333333333"),
        )
    assert get_game_state(db_session, user_id="empty_run")["revision"] == 0
