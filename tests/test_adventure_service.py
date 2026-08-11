from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.adventure_service import (
    ADVENTURE_RECORD,
    CLAIM_RECORD,
    FACILITY_RECORD,
    adventure_window,
    claim_adventure,
    settle_adventure,
    training_grounds_status,
)
from backend.database import ActivityLogModel, Base


def test_completed_window_reward_and_claim_are_idempotent():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    now = datetime(2026, 8, 10, 15, 30)

    try:
        start, end = adventure_window(now)
        assert start == datetime(2026, 8, 10, 0, 0)
        assert end == datetime(2026, 8, 10, 12, 0)

        first = settle_adventure(
            db,
            user_id="service_test_user",
            vitality=100,
            hbi_score=80,
            guild_coins=100,
            tower_floor=8,
            now=now,
        )
        retry = settle_adventure(
            db,
            user_id="service_test_user",
            vitality=999,
            hbi_score=100,
            guild_coins=999,
            tower_floor=99,
            now=now,
        )
        assert first["adventure_id"] == retry["adventure_id"]
        assert first["gross_guild_coins"] == 70
        assert retry["gross_guild_coins"] == 70
        assert first["tower_floor"] == 8
        assert retry["tower_floor"] == 8
        assert first["rooms"] == retry["rooms"]
        assert len(first["rooms"]) == 5
        assert first["rooms"][0]["room_type"] == "COMBAT"
        assert first["rooms"][-2]["room_type"] in {"REST", "SHOP"}
        assert first["rooms"][-1]["room_type"] == "BOSS"

        claimed = claim_adventure(
            db,
            user_id="service_test_user",
            adventure_id=first["adventure_id"],
        )
        claimed_again = claim_adventure(
            db,
            user_id="service_test_user",
            adventure_id=first["adventure_id"],
        )
        assert claimed["facility_invested"] == 14
        assert claimed["guild_coins_received"] == 56
        assert claimed_again["already_claimed"] is True

        assert db.query(ActivityLogModel).filter(
            ActivityLogModel.user_id == "service_test_user",
            ActivityLogModel.record_type == ADVENTURE_RECORD,
        ).count() == 1
        assert db.query(ActivityLogModel).filter(
            ActivityLogModel.user_id == "service_test_user",
            ActivityLogModel.record_type == CLAIM_RECORD,
        ).count() == 1
        assert db.query(ActivityLogModel).filter(
            ActivityLogModel.user_id == "service_test_user",
            ActivityLogModel.record_type == FACILITY_RECORD,
        ).count() == 1

        facility = training_grounds_status(db, user_id="service_test_user")
        assert facility["total_invested"] == 14
        assert facility["guild_coin_balance"] == 56
    finally:
        db.close()
        engine.dispose()
