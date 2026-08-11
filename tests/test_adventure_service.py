from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.adventure_service import (
    ADVENTURE_RECORD,
    CLAIM_RECORD,
    FACILITY_RECORD,
    HERO_JOIN_RECORD,
    adventure_history,
    adventure_window,
    claim_adventure,
    hero_roster,
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
        assert all(room["result_code"] for room in first["rooms"])
        assert all(room["result_title"] for room in first["rooms"])

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
        assert claimed["joined_hero"]["hero_code"] == "FOREST_SCOUT_ARU"
        assert claimed["joined_hero"]["gameplay_effect"] == "NONE"
        assert claimed_again["already_claimed"] is True

        assert db.query(ActivityLogModel).filter(
            ActivityLogModel.user_id == "service_test_user",
            ActivityLogModel.record_type == ADVENTURE_RECORD,
        ).count() == 1
        assert db.query(ActivityLogModel).filter(
            ActivityLogModel.user_id == "service_test_user",
            ActivityLogModel.record_type == HERO_JOIN_RECORD,
        ).count() == 1
        assert hero_roster(db, user_id="service_test_user")[0]["name"] == "아루"
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
        assert facility["stage_code"] == "FIELD_CAMP"
        assert facility["stage_name"] == "들판 훈련터"
        assert facility["next_milestone_level"] == 3

        later = settle_adventure(
            db,
            user_id="service_test_user",
            vitality=80,
            hbi_score=70,
            guild_coins=50,
            tower_floor=9,
            now=datetime(2026, 8, 11, 3, 0),
        )
        history = adventure_history(db, user_id="service_test_user")
        assert [item["adventure_id"] for item in history] == [
            later["adventure_id"],
            first["adventure_id"],
        ]
        assert history[1]["claimed"] is True
    finally:
        db.close()
        engine.dispose()


def test_facility_visual_stage_changes_without_reward_multiplier():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    try:
        for index in range(3):
            db.add(
                ActivityLogModel(
                    activity_id=f"facility-stage-{index}",
                    user_id="facility_stage_user",
                    record_type=FACILITY_RECORD,
                    value=100,
                    detail_json="{}",
                    exp_gained=0,
                )
            )
        db.commit()

        facility = training_grounds_status(db, user_id="facility_stage_user")
        assert facility["level"] == 3
        assert facility["stage_code"] == "TIMBER_YARD"
        assert facility["stage_name"] == "나무 훈련장"
        assert facility["next_milestone_level"] == 6
        assert "reward_multiplier" not in facility
    finally:
        db.close()
        engine.dispose()


def test_legacy_stored_rooms_are_enriched_without_changing_rewards():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    try:
        adventure = settle_adventure(
            db,
            user_id="legacy_room_user",
            vitality=50,
            hbi_score=60,
            guild_coins=40,
            now=datetime(2026, 8, 10, 15, 0),
        )
        record = db.query(ActivityLogModel).filter(
            ActivityLogModel.activity_id == adventure["adventure_id"]
        ).one()
        detail = {
            "window_start": "2026-08-10T00:00:00",
            "window_end": "2026-08-10T12:00:00",
            "vitality": 50,
            "gross_guild_coins": 28,
            "offline_efficiency": 0.7,
            "hbi_score": 60,
            "tower_floor": 1,
            "rooms": [
                {
                    "position": 1,
                    "room_type": "COMBAT",
                    "title": "안개 길목",
                    "outcome": "기존 기록",
                }
            ],
        }
        import json

        record.detail_json = json.dumps(detail, ensure_ascii=False)
        db.commit()

        replay = adventure_history(db, user_id="legacy_room_user")[0]
        assert replay["gross_guild_coins"] == 28
        assert len(replay["rooms"]) == 5
        assert all(room["result_code"] for room in replay["rooms"])
    finally:
        db.close()
        engine.dispose()
