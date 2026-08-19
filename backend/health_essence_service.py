"""Bounded, auditable health-record rewards for the permanent game currency."""
from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.config import utc_now
from backend.database import ActivityLogModel, GameHealthRewardModel, GameProfileModel


DAILY_HEALTH_ESSENCE_CAP = 8


def health_essence_candidate(record_type: str, value: float) -> int:
    """Return a small deterministic candidate without rewarding extreme values."""
    if record_type == "workout_log":
        if value < 10:
            return 0
        if value < 30:
            return 1
        if value < 60:
            return 2
        return 3
    if record_type == "meal_log":
        return 1 if value > 0 else 0
    if record_type == "water_log":
        return 1 if value >= 0.25 else 0
    if record_type == "habit_complete":
        return 1 if value >= 1 else 0
    return 0


def award_health_essence(
    db: Session,
    *,
    user_id: str,
    activity_id: str,
    record_type: str,
    value: float,
) -> int:
    """Award once per activity when the anonymous game's profile already exists."""
    existing = db.query(GameHealthRewardModel).filter_by(activity_id=activity_id).first()
    if existing is not None:
        return existing.health_essence_earned
    profile = (
        db.query(GameProfileModel)
        .filter_by(user_id=user_id)
        .with_for_update()
        .first()
    )
    if profile is None:
        return 0

    now = utc_now()
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    earned_today = int(
        db.query(func.coalesce(func.sum(GameHealthRewardModel.health_essence_earned), 0))
        .filter(
            GameHealthRewardModel.user_id == user_id,
            GameHealthRewardModel.created_at >= day_start,
        )
        .scalar()
        or 0
    )
    earned = min(
        health_essence_candidate(record_type, value),
        max(0, DAILY_HEALTH_ESSENCE_CAP - earned_today),
    )
    db.add(
        GameHealthRewardModel(
            activity_id=activity_id,
            user_id=user_id,
            record_type=record_type,
            health_essence_earned=earned,
            created_at=now,
        )
    )
    if earned:
        profile.health_essence += earned
        profile.revision += 1
        profile.updated_at = now
    return earned


def sync_unrewarded_health_records(db: Session, *, user_id: str) -> int:
    """Backfill valid records made before the user first opened the game."""
    profile = db.query(GameProfileModel).filter_by(user_id=user_id).first()
    if profile is None:
        return 0
    existing_rewards = db.query(GameHealthRewardModel).filter_by(user_id=user_id).all()
    rewarded_ids = {reward.activity_id for reward in existing_rewards}
    earned_by_day: dict[object, int] = {}
    for reward in existing_rewards:
        day = reward.created_at.date()
        earned_by_day[day] = earned_by_day.get(day, 0) + reward.health_essence_earned

    total = 0
    records = (
        db.query(ActivityLogModel)
        .filter_by(user_id=user_id)
        .order_by(ActivityLogModel.logged_at.asc(), ActivityLogModel.activity_id.asc())
        .all()
    )
    for record in records:
        if record.activity_id in rewarded_ids:
            continue
        day = record.logged_at.date()
        already = earned_by_day.get(day, 0)
        earned = min(
            health_essence_candidate(record.record_type, record.value),
            max(0, DAILY_HEALTH_ESSENCE_CAP - already),
        )
        db.add(
            GameHealthRewardModel(
                activity_id=record.activity_id,
                user_id=user_id,
                record_type=record.record_type,
                health_essence_earned=earned,
                created_at=record.logged_at,
            )
        )
        earned_by_day[day] = already + earned
        total += earned
    if total:
        profile.health_essence += total
        profile.revision += 1
        profile.updated_at = utc_now()
    return total
