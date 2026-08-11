from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.adventure_service import (
    claim_adventure,
    settle_adventure,
    training_grounds_status,
)
from backend.database import Base
from backend.guild_workshop_service import (
    HeroNotJoinedError,
    InsufficientGuildCoinsError,
    WorkshopLockedError,
    assign_party_member,
    craft_item,
    inventory,
    party_status,
    workshop_status,
)


def _session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return engine, sessionmaker(bind=engine)()


def test_crafting_inventory_and_party_assignment_are_persistent_and_idempotent():
    engine, db = _session()
    try:
        locked = workshop_status(db, user_id="workshop_user")
        assert locked["guild_coin_balance"] == 0
        assert all(recipe["unlocked"] is False for recipe in locked["recipes"])
        with pytest.raises(WorkshopLockedError):
            craft_item(db, user_id="workshop_user", recipe_code="FOREST_COMPASS")

        adventure = settle_adventure(
            db,
            user_id="workshop_user",
            vitality=100,
            hbi_score=80,
            guild_coins=200,
            now=datetime(2026, 8, 11, 15, 0),
        )
        claim = claim_adventure(
            db,
            user_id="workshop_user",
            adventure_id=adventure["adventure_id"],
        )
        assert claim["joined_hero"]["hero_code"] == "FOREST_SCOUT_ARU"
        assert training_grounds_status(db, user_id="workshop_user")[
            "guild_coin_balance"
        ] == 112

        compass = craft_item(
            db,
            user_id="workshop_user",
            recipe_code="FOREST_COMPASS",
        )
        compass_retry = craft_item(
            db,
            user_id="workshop_user",
            recipe_code="FOREST_COMPASS",
        )
        cloak = craft_item(
            db,
            user_id="workshop_user",
            recipe_code="WARM_TRAIL_CLOAK",
        )

        assert compass["already_crafted"] is False
        assert compass_retry["already_crafted"] is True
        assert compass["item"]["gameplay_effect"] == "NONE"
        assert cloak["guild_coin_balance"] == 52
        assert len(inventory(db, user_id="workshop_user")) == 2
        assert training_grounds_status(db, user_id="workshop_user")[
            "guild_coin_balance"
        ] == 52

        before_party = party_status(db, user_id="workshop_user")
        assert before_party["slots"][0]["member"] is None
        assigned = assign_party_member(
            db,
            user_id="workshop_user",
            hero_code="FOREST_SCOUT_ARU",
        )
        assigned_retry = assign_party_member(
            db,
            user_id="workshop_user",
            hero_code="FOREST_SCOUT_ARU",
        )
        assert assigned["already_assigned"] is False
        assert assigned_retry["already_assigned"] is True
        assert party_status(db, user_id="workshop_user")["slots"][0]["member"][
            "name"
        ] == "아루"
    finally:
        db.close()
        engine.dispose()


def test_locked_party_and_insufficient_balance_are_rejected():
    engine, db = _session()
    try:
        with pytest.raises(HeroNotJoinedError):
            assign_party_member(
                db,
                user_id="no_hero_user",
                hero_code="FOREST_SCOUT_ARU",
            )

        adventure = settle_adventure(
            db,
            user_id="poor_user",
            vitality=10,
            hbi_score=10,
            guild_coins=10,
            now=datetime(2026, 8, 11, 15, 0),
        )
        claim_adventure(
            db,
            user_id="poor_user",
            adventure_id=adventure["adventure_id"],
        )
        with pytest.raises(InsufficientGuildCoinsError):
            craft_item(db, user_id="poor_user", recipe_code="FOREST_COMPASS")
    finally:
        db.close()
        engine.dispose()
