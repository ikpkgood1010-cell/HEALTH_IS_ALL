from uuid import UUID

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.database import (
    Base,
    GameConstellationNodeModel,
    GameHeroModel,
    GameProfileModel,
    GameRebirthLogModel,
)
from backend.idle_game_service import (
    InitialHeroSelectionConflictError,
    RebirthNotReadyError,
    RebirthRevisionConflictError,
    execute_rebirth,
    get_game_state,
    initialize_game_state,
    preview_rebirth,
    select_initial_hero,
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


def test_rebirth_resets_only_run_state_and_is_idempotent(db_session):
    initialize_game_state(db_session, user_id="rebirth_user")
    profile = db_session.query(GameProfileModel).filter_by(user_id="rebirth_user").one()
    profile.tower_floor = 18
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
    assert result.state["highest_floor"] == 18
    assert result.state["room_position"] == 1
    assert result.state["gold"] == 0
    assert result.state["run_number"] == 2
    assert result.state["health_essence"] == 41
    assert result.state["star_shards"] == 7
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
