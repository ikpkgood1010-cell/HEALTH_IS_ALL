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
HERO_JOIN_RECORD = "game_hero_join"
OFFLINE_EFFICIENCY = 0.70
FACILITY_INVESTMENT_RATE = 0.20
ADVENTURE_WINDOW_HOURS = 12
ADVENTURE_ROOM_COUNT = 5

ROOM_CONTENT = {
    "COMBAT": ("안개 길목", (
        ("SWIFT_CLEAR", "경쾌한 돌파", "건강 기록에서 얻은 활력으로 안개 짐승을 가볍게 지나쳤어요."),
        ("STEADY_GUARD", "든든한 방어", "서두르지 않고 대열을 지켜 안전하게 길을 열었어요."),
        ("TEAM_COMBO", "호흡이 맞은 한 걸음", "서로의 빈틈을 채우며 작은 몬스터 무리를 정리했어요."),
    )),
    "EVENT": ("반짝이는 샘", (
        ("SPRING_ECHO", "샘의 메아리", "맑은 물결에서 다음 여정을 응원하는 목소리를 들었어요."),
        ("FOREST_CLUE", "숲의 작은 단서", "나뭇잎 표식이 안전한 지름길을 알려주었어요."),
        ("KIND_ENCOUNTER", "다정한 만남", "길을 잃은 여행자와 간식을 나누며 잠시 웃었어요."),
    )),
    "REST": ("회복의 모닥불", (
        ("WARM_REST", "따뜻한 휴식", "모닥불 곁에서 무리하지 않고 충분히 숨을 골랐어요."),
        ("QUIET_STRETCH", "가벼운 몸풀기", "긴장을 풀고 다음 방을 위한 편안한 리듬을 찾았어요."),
        ("SHARED_MEAL", "함께한 한 끼", "작은 식사를 나누며 모험대의 기운을 채웠어요."),
    )),
    "SHOP": ("떠돌이 교환소", (
        ("WISE_CHOICE", "현명한 선택", "보유 자원을 지키며 여정에 필요한 물품만 살폈어요."),
        ("LOCAL_RUMOR", "상인의 소문", "주화 대신 탑 위쪽의 안전한 길에 대한 이야기를 들었어요."),
        ("WINDOW_SHOP", "즐거운 구경", "꼭 필요한 물건은 없어 가볍게 구경만 하고 떠났어요."),
    )),
    "ELITE": ("수호자의 문", (
        ("PATIENT_WIN", "침착한 승리", "균형 잡힌 기록의 힘으로 단단한 관문을 차분히 넘겼어요."),
        ("GUARD_BREAK", "빈틈 발견", "수호자의 움직임을 살피고 안전한 순간에 문을 열었어요."),
        ("RESOLUTE_STEP", "흔들림 없는 전진", "빠르지 않아도 포기하지 않는 걸음으로 시련을 통과했어요."),
    )),
    "BOSS": ("층의 수호자", (
        ("BALANCED_FINISH", "균형의 마무리", "오늘의 건강 균형으로 수호자와의 대결을 안전하게 마쳤어요."),
        ("LASTING_COURAGE", "끝까지 이어진 용기", "작은 실천이 모인 힘으로 마지막까지 자리를 지켰어요."),
        ("GENTLE_VICTORY", "무리 없는 승리", "회복할 때와 나아갈 때를 구분하며 이번 층을 완주했어요."),
    )),
}

STARTER_HERO = {
    "hero_code": "FOREST_SCOUT_ARU",
    "name": "아루",
    "title": "새싹 길잡이",
    "role": "탐험 용사",
    "element": "FOREST",
    "rarity": "STORY",
    "join_source": "FIRST_ADVENTURE_CLAIM",
    "join_message": "첫 모험을 안전하게 마친 길드에 숲의 길잡이 아루가 합류했어요.",
    "gameplay_effect": "NONE",
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
        title, variants = ROOM_CONTENT[room_type]
        result_code, result_title, outcome = variants[digest[index + 8] % len(variants)]
        rooms.append(
            {
                "position": index + 1,
                "room_type": room_type,
                "title": title,
                "result_code": result_code,
                "result_title": result_title,
                "outcome": outcome,
            }
        )
    return rooms


def _response_rooms(adventure_id: str, stored_rooms: object) -> list[dict]:
    """Return enriched deterministic rooms, including for pre-expansion records."""
    generated = build_adventure_rooms(adventure_id)
    if not isinstance(stored_rooms, list):
        return generated
    by_position = {
        room.get("position"): room
        for room in stored_rooms
        if isinstance(room, dict) and isinstance(room.get("position"), int)
    }
    result = []
    for room in generated:
        stored = by_position.get(room["position"])
        if isinstance(stored, dict) and stored.get("result_code"):
            result.append({**room, **stored})
        else:
            result.append(room)
    return result


def _adventure_response(db: Session, log: ActivityLogModel) -> dict:
    detail = _detail(log)
    rooms = _response_rooms(log.activity_id, detail.get("rooms"))
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
    joined_hero = _joined_starter_hero(db, user_id=user_id)
    has_health_vitality = int(adventure_detail.get("vitality", 0)) > 0
    is_first_join = joined_hero is None and has_health_vitality
    if is_first_join:
        joined_hero = {
            **STARTER_HERO,
            "joined_at": utc_now().isoformat(),
            "source_adventure_id": adventure_id,
        }
    result = {
        "adventure_id": adventure_id,
        "claim_id": claim_id,
        "already_claimed": False,
        "gross_guild_coins": gross,
        "facility_invested": invested,
        "guild_coins_received": received,
        "joined_hero": joined_hero if is_first_join else None,
    }
    facility_id = _stable_id("facility", adventure_id)
    records = [
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
    ]
    if is_first_join:
        records.append(
            ActivityLogModel(
                activity_id=_stable_id("hero", user_id, STARTER_HERO["hero_code"]),
                user_id=user_id,
                record_type=HERO_JOIN_RECORD,
                value=0,
                detail_json=json.dumps(
                    joined_hero,
                    ensure_ascii=False,
                    separators=(",", ":"),
                ),
                exp_gained=0,
            )
        )
    db.add_all(records)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = db.query(ActivityLogModel).filter(
            ActivityLogModel.activity_id == claim_id
        ).first()
        if existing is None and is_first_join and _joined_starter_hero(
            db, user_id=user_id
        ) is not None:
            # Another adventure for the same user may have won the single hero
            # join race. Retry this distinct claim without trying to add the
            # already joined hero again.
            return claim_adventure(
                db,
                user_id=user_id,
                adventure_id=adventure_id,
            )
        if existing is None:
            raise
        result = _detail(existing)
        result["already_claimed"] = True
    return result


def _joined_starter_hero(db: Session, *, user_id: str) -> dict | None:
    hero_id = _stable_id("hero", user_id, STARTER_HERO["hero_code"])
    record = db.query(ActivityLogModel).filter(
        ActivityLogModel.activity_id == hero_id,
        ActivityLogModel.user_id == user_id,
        ActivityLogModel.record_type == HERO_JOIN_RECORD,
    ).first()
    return _detail(record) if record is not None else None


def hero_roster(db: Session, *, user_id: str) -> list[dict]:
    """Return story-earned heroes without changing game state."""
    records = (
        db.query(ActivityLogModel)
        .filter(
            ActivityLogModel.user_id == user_id,
            ActivityLogModel.record_type == HERO_JOIN_RECORD,
        )
        .order_by(ActivityLogModel.logged_at.asc())
        .all()
    )
    return [_detail(record) for record in records]


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
