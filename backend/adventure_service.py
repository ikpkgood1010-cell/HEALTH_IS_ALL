"""Idempotent automatic-adventure and training-ground event service.

The MVP reuses ``activity_logs`` as an append-only game event store.  Stable
UUID5 identifiers make settlement and claiming safe to retry without adding a
new database migration or awarding duplicate currency.
"""
from __future__ import annotations

import json
import hashlib
from datetime import datetime, timedelta
from math import floor
from uuid import NAMESPACE_URL, uuid5

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.config import utc_now
from backend.database import ActivityLogModel
from backend.game_balance_engine import dungeon_room_type


ADVENTURE_RECORD = "game_adventure"
CLAIM_RECORD = "game_adventure_claim"
FACILITY_RECORD = "game_facility_investment"
OFFLINE_EFFICIENCY = 0.70
FACILITY_INVESTMENT_RATE = 0.20
ADVENTURE_WINDOW_HOURS = 12
ADVENTURE_ROOM_COUNT = 5

ROOM_CONTENT = {
    "COMBAT": ("안개 길목", "건강 기록에서 얻은 활력으로 길을 열었어요."),
    "EVENT": ("반짝이는 샘", "작은 발견이 다음 여정을 응원해요."),
    "REST": ("회복의 모닥불", "무리하지 않고 숨을 고르며 전진했어요."),
    "SHOP": ("떠돌이 교환소", "보유 자원을 지키며 필요한 것만 살폈어요."),
    "ELITE": ("수호자의 문", "균형 잡힌 기록이 단단한 관문을 넘겼어요."),
    "BOSS": ("층의 수호자", "오늘의 건강 균형으로 안전하게 모험을 마쳤어요."),
}


class AdventureNotFoundError(LookupError):
    pass


class AdventureOwnershipError(PermissionError):
    pass


def _stable_id(kind: str, *parts: str) -> str:
    material = ":".join(("health-is-all", kind, *parts))
    return str(uuid5(NAMESPACE_URL, material))


def adventure_window(now: datetime) -> tuple[datetime, datetime]:
    """Return the most recently completed 12-hour UTC window."""
    current = now.replace(tzinfo=None)
    boundary_hour = 0 if current.hour < ADVENTURE_WINDOW_HOURS else ADVENTURE_WINDOW_HOURS
    end = current.replace(hour=boundary_hour, minute=0, second=0, microsecond=0)
    return end - timedelta(hours=ADVENTURE_WINDOW_HOURS), end


def _detail(log: ActivityLogModel) -> dict:
    try:
        value = json.loads(log.detail_json or "{}")
    except (TypeError, json.JSONDecodeError) as exc:
        raise ValueError("Stored game event is invalid") from exc
    if not isinstance(value, dict):
        raise ValueError("Stored game event is invalid")
    return value


def _is_claimed(db: Session, adventure_id: str) -> bool:
    claim_id = _stable_id("claim", adventure_id)
    return db.query(ActivityLogModel.activity_id).filter(
        ActivityLogModel.activity_id == claim_id,
        ActivityLogModel.record_type == CLAIM_RECORD,
    ).first() is not None


def build_adventure_rooms(adventure_id: str) -> list[dict]:
    """Build a deterministic five-room route from the stored adventure ID."""
    digest = hashlib.sha256(adventure_id.encode("utf-8")).digest()
    rooms = []
    for index in range(ADVENTURE_ROOM_COUNT):
        room_type = dungeon_room_type(
            digest[index],
            position=index,
            room_count=ADVENTURE_ROOM_COUNT,
        )
        title, outcome = ROOM_CONTENT[room_type]
        rooms.append(
            {
                "position": index + 1,
                "room_type": room_type,
                "title": title,
                "outcome": outcome,
            }
        )
    return rooms


def _adventure_response(db: Session, log: ActivityLogModel) -> dict:
    detail = _detail(log)
    rooms = detail.get("rooms")
    if not isinstance(rooms, list) or not rooms:
        rooms = build_adventure_rooms(log.activity_id)
    return {
        "adventure_id": log.activity_id,
        "user_id": log.user_id,
        "window_start": datetime.fromisoformat(detail["window_start"]),
        "window_end": datetime.fromisoformat(detail["window_end"]),
        "vitality": int(detail["vitality"]),
        "gross_guild_coins": int(detail["gross_guild_coins"]),
        "offline_efficiency": float(detail["offline_efficiency"]),
        "hbi_score": float(detail["hbi_score"]),
        "tower_floor": max(1, int(detail.get("tower_floor", 1))),
        "rooms": rooms,
        "claimed": _is_claimed(db, log.activity_id),
    }


def settle_adventure(
    db: Session,
    *,
    user_id: str,
    vitality: int,
    hbi_score: float,
    guild_coins: int,
    tower_floor: int = 1,
    now: datetime | None = None,
) -> dict:
    """Create or return the single adventure result for a 12-hour UTC window."""
    window_start, window_end = adventure_window(now or utc_now())
    adventure_id = _stable_id("adventure", user_id, window_start.isoformat())
    existing = db.query(ActivityLogModel).filter(
        ActivityLogModel.activity_id == adventure_id,
        ActivityLogModel.record_type == ADVENTURE_RECORD,
    ).first()
    if existing is not None:
        return _adventure_response(db, existing)

    gross_coins = max(0, floor(max(0, guild_coins) * OFFLINE_EFFICIENCY))
    detail = {
        "window_start": window_start.isoformat(),
        "window_end": window_end.isoformat(),
        "vitality": max(0, int(vitality)),
        "gross_guild_coins": gross_coins,
        "offline_efficiency": OFFLINE_EFFICIENCY,
        "hbi_score": max(0.0, float(hbi_score)),
        "tower_floor": max(1, int(tower_floor)),
        "rooms": build_adventure_rooms(adventure_id),
    }
    log = ActivityLogModel(
        activity_id=adventure_id,
        user_id=user_id,
        record_type=ADVENTURE_RECORD,
        value=float(gross_coins),
        detail_json=json.dumps(detail, ensure_ascii=False, separators=(",", ":")),
        exp_gained=0,
        logged_at=window_end,
    )
    db.add(log)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        log = db.query(ActivityLogModel).filter(ActivityLogModel.activity_id == adventure_id).one()
    return _adventure_response(db, log)


def claim_adventure(db: Session, *, user_id: str, adventure_id: str) -> dict:
    """Claim once and atomically route 20% of the reward to the training ground."""
    adventure = db.query(ActivityLogModel).filter(
        ActivityLogModel.activity_id == adventure_id,
        ActivityLogModel.record_type == ADVENTURE_RECORD,
    ).first()
    if adventure is None:
        raise AdventureNotFoundError(adventure_id)
    if adventure.user_id != user_id:
        raise AdventureOwnershipError(adventure_id)

    claim_id = _stable_id("claim", adventure_id)
    existing = db.query(ActivityLogModel).filter(
        ActivityLogModel.activity_id == claim_id,
        ActivityLogModel.record_type == CLAIM_RECORD,
    ).first()
    if existing is not None:
        result = _detail(existing)
        result["already_claimed"] = True
        return result

    adventure_detail = _detail(adventure)
    gross = int(adventure_detail["gross_guild_coins"])
    invested = floor(gross * FACILITY_INVESTMENT_RATE)
    received = gross - invested
    result = {
        "adventure_id": adventure_id,
        "claim_id": claim_id,
        "already_claimed": False,
        "gross_guild_coins": gross,
        "facility_invested": invested,
        "guild_coins_received": received,
    }
    facility_id = _stable_id("facility", adventure_id)
    db.add_all([
        ActivityLogModel(
            activity_id=claim_id,
            user_id=user_id,
            record_type=CLAIM_RECORD,
            value=float(received),
            detail_json=json.dumps(result, ensure_ascii=False, separators=(",", ":")),
            exp_gained=0,
        ),
        ActivityLogModel(
            activity_id=facility_id,
            user_id=user_id,
            record_type=FACILITY_RECORD,
            value=float(invested),
            detail_json=json.dumps(
                {"adventure_id": adventure_id, "facility": "TRAINING_GROUNDS"},
                ensure_ascii=False,
                separators=(",", ":"),
            ),
            exp_gained=0,
        ),
    ])
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = db.query(ActivityLogModel).filter(ActivityLogModel.activity_id == claim_id).one()
        result = _detail(existing)
        result["already_claimed"] = True
    return result


def adventure_history(db: Session, *, user_id: str, limit: int = 5) -> list[dict]:
    """Return recent stored adventures without creating or changing game data."""
    logs = (
        db.query(ActivityLogModel)
        .filter(
            ActivityLogModel.user_id == user_id,
            ActivityLogModel.record_type == ADVENTURE_RECORD,
        )
        .order_by(ActivityLogModel.logged_at.desc())
        .limit(max(1, min(int(limit), 20)))
        .all()
    )
    return [_adventure_response(db, log) for log in logs]


def _facility_stage(level: int) -> dict:
    """Describe visible facility growth without adding an economy multiplier."""
    if level >= 10:
        return {
            "stage_code": "GUARDIAN_HALL",
            "stage_name": "수호자의 훈련관",
            "stage_message": "오래 쌓아온 건강 기록이 든든한 훈련관을 완성했어요.",
            "next_milestone_level": None,
        }
    if level >= 6:
        return {
            "stage_code": "STONE_COURT",
            "stage_name": "돌담 연무장",
            "stage_message": "꾸준한 모험 덕분에 비바람에도 든든한 연무장이 됐어요.",
            "next_milestone_level": 10,
        }
    if level >= 3:
        return {
            "stage_code": "TIMBER_YARD",
            "stage_name": "나무 훈련장",
            "stage_message": "조금씩 모은 주화로 안전한 훈련 도구를 갖췄어요.",
            "next_milestone_level": 6,
        }
    return {
        "stage_code": "FIELD_CAMP",
        "stage_name": "들판 훈련터",
        "stage_message": "작은 훈련터가 건강한 모험을 차근차근 기억하고 있어요.",
        "next_milestone_level": 3,
    }


def training_grounds_status(db: Session, *, user_id: str) -> dict:
    total = int(db.query(func.coalesce(func.sum(ActivityLogModel.value), 0)).filter(
        ActivityLogModel.user_id == user_id,
        ActivityLogModel.record_type == FACILITY_RECORD,
    ).scalar() or 0)
    balance = int(db.query(func.coalesce(func.sum(ActivityLogModel.value), 0)).filter(
        ActivityLogModel.user_id == user_id,
        ActivityLogModel.record_type == CLAIM_RECORD,
    ).scalar() or 0)

    level = 1
    remainder = total
    next_cost = 100
    while remainder >= next_cost:
        remainder -= next_cost
        level += 1
        next_cost = 100 + (level - 1) * 50

    return {
        "code": "TRAINING_GROUNDS",
        "name": "훈련장",
        "level": level,
        "total_invested": total,
        "current_level_progress": remainder,
        "next_level_cost": next_cost,
        "progress_ratio": round(remainder / next_cost, 4),
        "guild_coin_balance": balance,
        "description": "모험 보상의 20%가 자동 적립되는 길드 기초 시설",
        **_facility_stage(level),
    }
