"""One-time cosmetic crafting, inventory, and party assignment services."""
from __future__ import annotations

import json
from uuid import NAMESPACE_URL, uuid5

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.adventure_service import (
    CRAFT_RECORD,
    HERO_JOIN_RECORD,
    guild_coin_balance,
)
from backend.config import utc_now
from backend.database import ActivityLogModel, HealthIProfileModel


PARTY_ASSIGN_RECORD = "game_party_assignment"
VANGUARD_SLOT = "VANGUARD"

WORKSHOP_RECIPES = {
    "FOREST_COMPASS": {
        "recipe_code": "FOREST_COMPASS",
        "item_code": "FOREST_COMPASS",
        "name": "숲길 나침반",
        "category": "KEEPSAKE",
        "rarity": "COMMON",
        "cost": 20,
        "description": "첫 원정의 방향을 기억하는 작은 나침반",
        "gameplay_effect": "NONE",
    },
    "WARM_TRAIL_CLOAK": {
        "recipe_code": "WARM_TRAIL_CLOAK",
        "item_code": "WARM_TRAIL_CLOAK",
        "name": "포근한 길잡이 망토",
        "category": "COSTUME",
        "rarity": "COMMON",
        "cost": 40,
        "description": "천천히 걸어도 따뜻한 원정대의 기념 망토",
        "gameplay_effect": "NONE",
    },
}


class RecipeNotFoundError(LookupError):
    pass


class WorkshopLockedError(PermissionError):
    pass


class InsufficientGuildCoinsError(ValueError):
    pass


class HeroNotJoinedError(LookupError):
    pass


def _stable_id(kind: str, *parts: str) -> str:
    material = ":".join(("health-is-all", kind, *parts))
    return str(uuid5(NAMESPACE_URL, material))


def _detail(record: ActivityLogModel) -> dict:
    value = json.loads(record.detail_json or "{}")
    if not isinstance(value, dict):
        raise ValueError("Stored guild event is invalid")
    return value


def _hero(db: Session, *, user_id: str, hero_code: str) -> dict | None:
    records = db.query(ActivityLogModel).filter(
        ActivityLogModel.user_id == user_id,
        ActivityLogModel.record_type == HERO_JOIN_RECORD,
    ).all()
    for record in records:
        hero = _detail(record)
        if hero.get("hero_code") == hero_code:
            return hero
    return None


def inventory(db: Session, *, user_id: str) -> list[dict]:
    records = (
        db.query(ActivityLogModel)
        .filter(
            ActivityLogModel.user_id == user_id,
            ActivityLogModel.record_type == CRAFT_RECORD,
        )
        .order_by(ActivityLogModel.logged_at.asc())
        .all()
    )
    return [_detail(record) for record in records]


def workshop_status(db: Session, *, user_id: str) -> dict:
    owned_items = inventory(db, user_id=user_id)
    owned_codes = {item["item_code"] for item in owned_items}
    has_hero = db.query(ActivityLogModel.activity_id).filter(
        ActivityLogModel.user_id == user_id,
        ActivityLogModel.record_type == HERO_JOIN_RECORD,
    ).first() is not None
    recipes = [
        {
            **recipe,
            "unlocked": has_hero,
            "unlock_message": (
                "모험 용사가 합류해 제작법을 알려줬어요."
                if has_hero
                else "건강 기록으로 첫 모험을 마치고 용사를 맞이하면 열려요."
            ),
            "crafted": recipe["item_code"] in owned_codes,
        }
        for recipe in WORKSHOP_RECIPES.values()
    ]
    return {
        "guild_coin_balance": guild_coin_balance(db, user_id=user_id),
        "recipes": recipes,
        "inventory": owned_items,
    }


def craft_item(db: Session, *, user_id: str, recipe_code: str) -> dict:
    recipe = WORKSHOP_RECIPES.get(recipe_code)
    if recipe is None:
        raise RecipeNotFoundError(recipe_code)
    if db.query(ActivityLogModel.activity_id).filter(
        ActivityLogModel.user_id == user_id,
        ActivityLogModel.record_type == HERO_JOIN_RECORD,
    ).first() is None:
        raise WorkshopLockedError(user_id)

    craft_id = _stable_id("craft", user_id, recipe["item_code"])
    existing = db.query(ActivityLogModel).filter(
        ActivityLogModel.activity_id == craft_id,
        ActivityLogModel.record_type == CRAFT_RECORD,
    ).first()
    if existing is not None:
        return {
            "item": _detail(existing),
            "already_crafted": True,
            "guild_coin_balance": guild_coin_balance(db, user_id=user_id),
        }

    db.query(HealthIProfileModel).filter(
        HealthIProfileModel.user_id == user_id
    ).with_for_update().first()
    balance = guild_coin_balance(db, user_id=user_id)
    if balance < recipe["cost"]:
        raise InsufficientGuildCoinsError(recipe_code)

    item = {
        "item_code": recipe["item_code"],
        "name": recipe["name"],
        "category": recipe["category"],
        "rarity": recipe["rarity"],
        "description": recipe["description"],
        "gameplay_effect": recipe["gameplay_effect"],
        "cost_paid": recipe["cost"],
        "crafted_at": utc_now().isoformat(),
    }
    record = ActivityLogModel(
        activity_id=craft_id,
        user_id=user_id,
        record_type=CRAFT_RECORD,
        value=float(recipe["cost"]),
        detail_json=json.dumps(item, ensure_ascii=False, separators=(",", ":")),
        exp_gained=0,
    )
    db.add(record)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = db.query(ActivityLogModel).filter(
            ActivityLogModel.activity_id == craft_id
        ).one()
        item = _detail(existing)
        already_crafted = True
    else:
        already_crafted = False
    return {
        "item": item,
        "already_crafted": already_crafted,
        "guild_coin_balance": guild_coin_balance(db, user_id=user_id),
    }


def party_status(db: Session, *, user_id: str) -> dict:
    assignment = (
        db.query(ActivityLogModel)
        .filter(
            ActivityLogModel.user_id == user_id,
            ActivityLogModel.record_type == PARTY_ASSIGN_RECORD,
        )
        .order_by(ActivityLogModel.logged_at.desc())
        .first()
    )
    member = _detail(assignment).get("member") if assignment is not None else None
    return {
        "slots": [
            {
                "slot_code": VANGUARD_SLOT,
                "slot_name": "선봉",
                "member": member,
            }
        ]
    }


def assign_party_member(db: Session, *, user_id: str, hero_code: str) -> dict:
    hero = _hero(db, user_id=user_id, hero_code=hero_code)
    if hero is None:
        raise HeroNotJoinedError(hero_code)
    assignment_id = _stable_id("party", user_id, VANGUARD_SLOT, hero_code)
    existing = db.query(ActivityLogModel).filter(
        ActivityLogModel.activity_id == assignment_id,
        ActivityLogModel.record_type == PARTY_ASSIGN_RECORD,
    ).first()
    if existing is not None:
        detail = _detail(existing)
        return {**detail, "already_assigned": True}

    result = {
        "slot_code": VANGUARD_SLOT,
        "slot_name": "선봉",
        "member": hero,
        "already_assigned": False,
        "assigned_at": utc_now().isoformat(),
    }
    db.add(
        ActivityLogModel(
            activity_id=assignment_id,
            user_id=user_id,
            record_type=PARTY_ASSIGN_RECORD,
            value=0,
            detail_json=json.dumps(result, ensure_ascii=False, separators=(",", ":")),
            exp_gained=0,
        )
    )
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = db.query(ActivityLogModel).filter(
            ActivityLogModel.activity_id == assignment_id
        ).one()
        result = _detail(existing)
        result["already_assigned"] = True
    return result
