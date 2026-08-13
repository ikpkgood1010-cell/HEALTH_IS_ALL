"""Canonical idle-game persistence and rebirth operations."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from math import floor
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.config import utc_now
from backend.constellation_economy import (
    REBIRTH_MINIMUM_FLOOR,
    branch_total_gold,
    layer_zero_branch,
    next_branch_node,
    rebirth_star_shards,
    run_power_multiplier,
)
from backend.database import (
    GameBattleSettlementModel,
    GameConstellationNodeModel,
    GameHeroModel,
    GameProfileModel,
    GameRebirthLogModel,
)
from backend.idle_battle_engine import (
    DEFAULT_TUNING,
    advance_battle,
    calculate_party_power,
    room_required_seconds,
)

HERO_ROLES = (
    ("TANKER", "탱커"),
    ("WARRIOR", "전사"),
    ("MAGE", "마법사"),
    ("ARCHER", "궁수"),
    ("ROGUE", "도적"),
    ("HEALER", "치유사"),
)
ROOMS_PER_FLOOR = 6
RUN_NODE_SIZES = ("SMALL", "MEDIUM")


class GameStateNotFoundError(LookupError):
    pass


class InitialHeroSelectionConflictError(RuntimeError):
    pass


class RebirthRevisionConflictError(RuntimeError):
    pass


class RebirthNotReadyError(RuntimeError):
    pass


class BattleNotReadyError(RuntimeError):
    pass


class BattleSettlementConflictError(RuntimeError):
    pass


class ConstellationRevisionConflictError(RuntimeError):
    pass


class ConstellationNodeNotReadyError(RuntimeError):
    pass


class InsufficientGoldError(RuntimeError):
    pass


@dataclass(frozen=True)
class RebirthResult:
    rebirth_id: str
    already_executed: bool
    state: dict


@dataclass(frozen=True)
class BattleSettlementResult:
    settlement_id: str
    already_settled: bool
    elapsed_seconds: int
    credited_seconds: int
    capped: bool
    rooms_cleared: int
    bosses_cleared: int
    gold_earned: int
    state: dict


def _replay_battle_settlement(
    log: GameBattleSettlementModel,
) -> BattleSettlementResult:
    payload = json.loads(log.result_json)
    return BattleSettlementResult(
        settlement_id=log.settlement_id,
        already_settled=True,
        **payload,
    )


def initialize_game_state(db: Session, *, user_id: str) -> dict:
    """Create the empty six-slot roster exactly once."""
    profile = db.query(GameProfileModel).filter_by(user_id=user_id).first()
    if profile is None:
        db.add(GameProfileModel(user_id=user_id))
        db.add_all(
            GameHeroModel(
                user_id=user_id,
                hero_code=hero_code,
                role_name=role_name,
            )
            for hero_code, role_name in HERO_ROLES
        )
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
    return get_game_state(db, user_id=user_id)


def select_initial_hero(
    db: Session,
    *,
    user_id: str,
    hero_code: str,
    expected_revision: int,
) -> dict:
    """Recruit exactly one free starter without consuming a layer-0 node."""
    normalized_code = hero_code.strip().upper()
    valid_codes = {code for code, _ in HERO_ROLES}
    if normalized_code not in valid_codes:
        raise ValueError("unknown canonical hero code")

    profile = (
        db.query(GameProfileModel)
        .filter_by(user_id=user_id)
        .with_for_update()
        .first()
    )
    if profile is None:
        raise GameStateNotFoundError(user_id)

    recruited = (
        db.query(GameHeroModel)
        .filter_by(user_id=user_id, recruited=True)
        .all()
    )
    if recruited:
        if len(recruited) == 1 and recruited[0].hero_code == normalized_code:
            return get_game_state(db, user_id=user_id)
        raise InitialHeroSelectionConflictError("initial hero is already selected")
    if profile.revision != expected_revision:
        raise InitialHeroSelectionConflictError("game state revision changed")

    hero = db.query(GameHeroModel).filter_by(
        user_id=user_id,
        hero_code=normalized_code,
    ).one()
    hero.recruited = True
    hero.updated_at = utc_now()
    profile.battle_anchor_at = utc_now()
    profile.battle_progress_seconds = 0.0
    profile.revision += 1
    profile.updated_at = utc_now()
    db.commit()
    return get_game_state(db, user_id=user_id)


def get_game_state(db: Session, *, user_id: str) -> dict:
    profile = db.query(GameProfileModel).filter_by(user_id=user_id).first()
    if profile is None:
        raise GameStateNotFoundError(user_id)

    heroes = (
        db.query(GameHeroModel)
        .filter_by(user_id=user_id)
        .order_by(GameHeroModel.hero_code.asc())
        .all()
    )
    by_code = {hero.hero_code: hero for hero in heroes}
    ordered_heroes = [by_code[code] for code, _ in HERO_ROLES if code in by_code]
    node_counts = _node_counts(db, user_id=user_id)
    recruited_count = sum(1 for hero in ordered_heroes if hero.recruited)
    recruited_tiers = [
        hero.advancement_tier for hero in ordered_heroes if hero.recruited
    ]
    power_multiplier = run_power_multiplier(
        small_nodes=node_counts["SMALL"],
        medium_nodes=node_counts["MEDIUM"],
    )
    party_power = calculate_party_power(
        recruited_tiers,
        run_power_multiplier=power_multiplier,
    )
    current_room_required = (
        room_required_seconds(
            tower_floor=profile.tower_floor,
            room_position=profile.room_position,
            party_power=party_power,
        )
        if party_power > 0
        else 0
    )
    constellation_layers, starter_hero_code = _constellation_layers(
        db,
        user_id=user_id,
        heroes=ordered_heroes,
    )
    recruitment_branches = _recruitment_branches(
        db,
        user_id=user_id,
        run_number=profile.run_number,
        heroes=ordered_heroes,
        starter_hero_code=starter_hero_code,
    )
    branch_by_hero = {branch["hero_code"]: branch for branch in recruitment_branches}
    for node in constellation_layers[0]["nodes"]:
        branch = branch_by_hero.get(node["hero_code"])
        if branch is not None and branch["ready_to_recruit"] and node["state"] != "UNLOCKED":
            node["state"] = "NEXT"

    return {
        "initialized": True,
        "phase": "ONBOARDING" if recruited_count == 0 else "IDLE_BATTLE",
        "user_id": profile.user_id,
        "revision": profile.revision,
        "run_number": profile.run_number,
        "tower_floor": profile.tower_floor,
        "highest_floor": profile.highest_floor,
        "room_position": profile.room_position,
        "rooms_per_floor": ROOMS_PER_FLOOR,
        "gold": profile.gold,
        "battle": {
            "status": "RUNNING" if recruited_count > 0 else "WAITING_FOR_HERO",
            "server_anchor_at": (
                f"{profile.battle_anchor_at.isoformat()}Z"
                if profile.battle_anchor_at is not None
                else None
            ),
            "offline_cap_seconds": DEFAULT_TUNING.offline_cap_seconds,
            "party_power": party_power,
            "run_power_multiplier": round(power_multiplier, 4),
            "current_room_kind": (
                "BOSS" if profile.room_position == ROOMS_PER_FLOOR else "NORMAL"
            ),
            "room_progress_seconds": floor(profile.battle_progress_seconds or 0.0),
            "room_required_seconds": current_room_required,
        },
        "health_essence": profile.health_essence,
        "star_shards": profile.star_shards,
        "transcendence_points": profile.transcendence_points,
        "initial_hero_selected": recruited_count > 0,
        "starter_hero_code": starter_hero_code,
        "large_node_slots_by_layer": {
            "0": 5,
            **{str(layer): 6 for layer in range(1, 7)},
        },
        "constellation_layers": constellation_layers,
        "recruitment_branches": recruitment_branches,
        "heroes": [
            {
                "hero_code": hero.hero_code,
                "role_name": hero.role_name,
                "recruited": hero.recruited,
                "advancement_tier": hero.advancement_tier,
                "appearance_code": hero.appearance_code,
                "active_skill_slots": hero.active_skill_slots,
            }
            for hero in ordered_heroes
        ],
        "node_counts": node_counts,
    }


def settle_idle_battle(
    db: Session,
    *,
    user_id: str,
    settlement_id: UUID | str,
    now: datetime | None = None,
) -> BattleSettlementResult:
    """Credit elapsed server time once and atomically advance the current run."""
    stable_id = str(settlement_id)
    existing = db.query(GameBattleSettlementModel).filter_by(
        settlement_id=stable_id
    ).first()
    if existing is not None:
        if existing.user_id != user_id:
            raise BattleSettlementConflictError(
                "battle settlement id belongs to another user"
            )
        return _replay_battle_settlement(existing)

    profile = (
        db.query(GameProfileModel)
        .filter_by(user_id=user_id)
        .with_for_update()
        .first()
    )
    if profile is None:
        raise GameStateNotFoundError(user_id)
    # A concurrent retry may have committed while this transaction waited for
    # the profile lock. Recheck before calculating or granting anything.
    existing = db.query(GameBattleSettlementModel).filter_by(
        settlement_id=stable_id
    ).first()
    if existing is not None:
        if existing.user_id != user_id:
            raise BattleSettlementConflictError(
                "battle settlement id belongs to another user"
            )
        return _replay_battle_settlement(existing)
    recruited = db.query(GameHeroModel).filter_by(
        user_id=user_id,
        recruited=True,
    ).all()
    if not recruited:
        raise BattleNotReadyError("select the initial hero before settling battle")

    settled_at = now or utc_now()
    anchor = profile.battle_anchor_at or settled_at
    elapsed = max(0, floor((settled_at - anchor).total_seconds()))
    node_counts = _node_counts(db, user_id=user_id)
    result = advance_battle(
        tower_floor=profile.tower_floor,
        room_position=profile.room_position,
        carry_seconds=profile.battle_progress_seconds or 0.0,
        elapsed_seconds=elapsed,
        advancement_tiers=[hero.advancement_tier for hero in recruited],
        run_power_multiplier=run_power_multiplier(
            small_nodes=node_counts["SMALL"],
            medium_nodes=node_counts["MEDIUM"],
        ),
    )

    profile.tower_floor = result.end_floor
    profile.highest_floor = max(profile.highest_floor, result.end_floor)
    profile.room_position = result.end_room
    profile.gold += result.gold_earned
    profile.battle_progress_seconds = result.carry_seconds
    profile.battle_anchor_at = settled_at
    if result.credited_seconds > 0:
        profile.revision += 1
    profile.updated_at = settled_at
    db.flush()

    state = get_game_state(db, user_id=user_id)
    payload = {
        "elapsed_seconds": elapsed,
        "credited_seconds": result.credited_seconds,
        "capped": elapsed > result.credited_seconds,
        "rooms_cleared": result.rooms_cleared,
        "bosses_cleared": result.bosses_cleared,
        "gold_earned": result.gold_earned,
        "state": state,
    }
    db.add(
        GameBattleSettlementModel(
            settlement_id=stable_id,
            user_id=user_id,
            elapsed_seconds=elapsed,
            credited_seconds=result.credited_seconds,
            rooms_cleared=result.rooms_cleared,
            bosses_cleared=result.bosses_cleared,
            gold_earned=result.gold_earned,
            result_json=json.dumps(
                payload,
                ensure_ascii=False,
                separators=(",", ":"),
            ),
            created_at=settled_at,
        )
    )
    db.commit()
    return BattleSettlementResult(
        settlement_id=stable_id,
        already_settled=False,
        **payload,
    )


def unlock_constellation_node(
    db: Session,
    *,
    user_id: str,
    node_code: str,
    expected_revision: int,
) -> dict:
    """Unlock the next run node or recruit one completed layer-zero branch."""
    normalized_code = node_code.strip().upper()
    profile = (
        db.query(GameProfileModel)
        .filter_by(user_id=user_id)
        .with_for_update()
        .first()
    )
    if profile is None:
        raise GameStateNotFoundError(user_id)

    existing = db.query(GameConstellationNodeModel).filter_by(
        user_id=user_id,
        node_code=normalized_code,
    ).first()
    if existing is not None:
        return get_game_state(db, user_id=user_id)
    if profile.revision != expected_revision:
        raise ConstellationRevisionConflictError("game state revision changed")

    heroes = db.query(GameHeroModel).filter_by(user_id=user_id).all()
    ordered = sorted(heroes, key=lambda hero: next(
        index for index, (code, _) in enumerate(HERO_ROLES) if code == hero.hero_code
    ))
    _, starter_hero_code = _constellation_layers(db, user_id=user_id, heroes=ordered)
    if starter_hero_code is None:
        raise ConstellationNodeNotReadyError("select the initial hero first")
    branches = _recruitment_branches(
        db,
        user_id=user_id,
        run_number=profile.run_number,
        heroes=ordered,
        starter_hero_code=starter_hero_code,
    )

    for branch in branches:
        next_node = branch["next_node"]
        recruit_code = f"L0_RECRUIT_{branch['hero_code']}"
        if next_node is not None and normalized_code == next_node["node_code"]:
            cost = next_node["gold_cost"]
            if profile.gold < cost:
                raise InsufficientGoldError(f"requires {cost} gold")
            profile.gold -= cost
            db.add(
                GameConstellationNodeModel(
                    user_id=user_id,
                    node_code=normalized_code,
                    layer=0,
                    node_size=next_node["node_size"],
                    hero_code=branch["hero_code"],
                    unlocked_run_number=profile.run_number,
                    unlocked_at=utc_now(),
                )
            )
            profile.revision += 1
            profile.updated_at = utc_now()
            db.commit()
            return get_game_state(db, user_id=user_id)
        if next_node is None and normalized_code == recruit_code:
            hero = next(item for item in heroes if item.hero_code == branch["hero_code"])
            if hero.recruited:
                return get_game_state(db, user_id=user_id)
            hero.recruited = True
            hero.updated_at = utc_now()
            db.add(
                GameConstellationNodeModel(
                    user_id=user_id,
                    node_code=recruit_code,
                    layer=0,
                    node_size="LARGE",
                    hero_code=branch["hero_code"],
                    unlocked_run_number=profile.run_number,
                    unlocked_at=utc_now(),
                )
            )
            profile.revision += 1
            profile.updated_at = utc_now()
            db.commit()
            return get_game_state(db, user_id=user_id)

    raise ConstellationNodeNotReadyError("node is not the next unlockable node")


def preview_rebirth(db: Session, *, user_id: str) -> dict:
    state = get_game_state(db, user_id=user_id)
    small = state["node_counts"]["SMALL"]
    medium = state["node_counts"]["MEDIUM"]
    shard_reward = rebirth_star_shards(state["tower_floor"])
    can_rebirth = state["tower_floor"] >= REBIRTH_MINIMUM_FLOOR
    return {
        "user_id": user_id,
        "revision": state["revision"],
        "can_rebirth": can_rebirth,
        "next_run_number": state["run_number"] + 1,
        "minimum_floor": REBIRTH_MINIMUM_FLOOR,
        "star_shards_to_earn": shard_reward,
        "reset": {
            "tower_floor": state["tower_floor"],
            "room_position": state["room_position"],
            "gold": state["gold"],
            "small_nodes": small,
            "medium_nodes": medium,
        },
        "retain": {
            "heroes": len(state["heroes"]),
            "recruited_heroes": sum(hero["recruited"] for hero in state["heroes"]),
            "large_nodes": state["node_counts"]["LARGE"],
            "health_essence": state["health_essence"],
            "star_shards": state["star_shards"],
            "transcendence_points": state["transcendence_points"],
            "advancement_tiers": {
                hero["hero_code"]: hero["advancement_tier"]
                for hero in state["heroes"]
            },
            "appearances": {
                hero["hero_code"]: hero["appearance_code"]
                for hero in state["heroes"]
            },
        },
    }


def execute_rebirth(
    db: Session,
    *,
    user_id: str,
    expected_revision: int,
    rebirth_id: UUID | str,
) -> RebirthResult:
    """Reset run-only state while atomically retaining permanent progression."""
    stable_rebirth_id = str(rebirth_id)
    existing = db.query(GameRebirthLogModel).filter_by(
        rebirth_id=stable_rebirth_id
    ).first()
    if existing is not None:
        if existing.user_id != user_id:
            raise RebirthRevisionConflictError("rebirth id belongs to another user")
        return RebirthResult(
            rebirth_id=stable_rebirth_id,
            already_executed=True,
            state=get_game_state(db, user_id=user_id),
        )

    profile = (
        db.query(GameProfileModel)
        .filter_by(user_id=user_id)
        .with_for_update()
        .first()
    )
    if profile is None:
        raise GameStateNotFoundError(user_id)
    if profile.revision != expected_revision:
        raise RebirthRevisionConflictError("game state revision changed")

    preview = preview_rebirth(db, user_id=user_id)
    if not preview["can_rebirth"]:
        raise RebirthNotReadyError(
            f"reach floor {REBIRTH_MINIMUM_FLOOR} before rebirth"
        )

    previous_floor = max(profile.highest_floor, profile.tower_floor)
    snapshot = json.dumps(preview["retain"], ensure_ascii=False, separators=(",", ":"))
    db.query(GameConstellationNodeModel).filter(
        GameConstellationNodeModel.user_id == user_id,
        GameConstellationNodeModel.node_size.in_(RUN_NODE_SIZES),
    ).delete(synchronize_session=False)

    from_run = profile.run_number
    profile.highest_floor = previous_floor
    profile.tower_floor = 1
    profile.room_position = 1
    profile.gold = 0
    profile.star_shards += preview["star_shards_to_earn"]
    profile.battle_progress_seconds = 0.0
    profile.battle_anchor_at = utc_now()
    profile.run_number = from_run + 1
    profile.revision += 1
    profile.updated_at = utc_now()
    db.add(
        GameRebirthLogModel(
            rebirth_id=stable_rebirth_id,
            user_id=user_id,
            from_run_number=from_run,
            to_run_number=from_run + 1,
            previous_highest_floor=previous_floor,
            reset_small_nodes=preview["reset"]["small_nodes"],
            reset_medium_nodes=preview["reset"]["medium_nodes"],
            star_shards_earned=preview["star_shards_to_earn"],
            retained_snapshot_json=snapshot,
        )
    )
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = db.query(GameRebirthLogModel).filter_by(
            rebirth_id=stable_rebirth_id,
            user_id=user_id,
        ).first()
        if existing is None:
            raise
        return RebirthResult(
            rebirth_id=stable_rebirth_id,
            already_executed=True,
            state=get_game_state(db, user_id=user_id),
        )

    return RebirthResult(
        rebirth_id=stable_rebirth_id,
        already_executed=False,
        state=get_game_state(db, user_id=user_id),
    )


def _node_counts(db: Session, *, user_id: str) -> dict[str, int]:
    rows = (
        db.query(
            GameConstellationNodeModel.node_size,
            func.count(GameConstellationNodeModel.node_code),
        )
        .filter(GameConstellationNodeModel.user_id == user_id)
        .group_by(GameConstellationNodeModel.node_size)
        .all()
    )
    values = {size: 0 for size in ("SMALL", "MEDIUM", "LARGE")}
    values.update({str(size): int(count) for size, count in rows})
    return values


def _recruitment_branches(
    db: Session,
    *,
    user_id: str,
    run_number: int,
    heroes: list[GameHeroModel],
    starter_hero_code: str | None,
) -> list[dict]:
    if starter_hero_code is None:
        return []
    unlocked_codes = {
        code
        for (code,) in db.query(GameConstellationNodeModel.node_code)
        .filter(
            GameConstellationNodeModel.user_id == user_id,
            GameConstellationNodeModel.unlocked_run_number == run_number,
            GameConstellationNodeModel.node_size.in_(RUN_NODE_SIZES),
        )
        .all()
    }
    result = []
    for hero in heroes:
        if hero.hero_code == starter_hero_code:
            continue
        branch = layer_zero_branch(hero.hero_code)
        unlocked = [node for node in branch if node.node_code in unlocked_codes]
        next_node = next_branch_node(hero.hero_code, unlocked_codes)
        result.append(
            {
                "hero_code": hero.hero_code,
                "role_name": hero.role_name,
                "hero_recruited": hero.recruited,
                "layer": 0,
                "unlocked_nodes": len(unlocked),
                "total_nodes": len(branch),
                "small_unlocked": sum(node.node_size == "SMALL" for node in unlocked),
                "medium_unlocked": sum(node.node_size == "MEDIUM" for node in unlocked),
                "gold_spent": sum(node.gold_cost for node in unlocked),
                "total_gold_cost": branch_total_gold(hero.hero_code),
                "branch_complete": next_node is None,
                "ready_to_recruit": next_node is None and not hero.recruited,
                "next_node": (
                    {
                        "node_code": next_node.node_code,
                        "node_size": next_node.node_size,
                        "sequence": next_node.sequence,
                        "gold_cost": next_node.gold_cost,
                        "title": next_node.title,
                        "effect_label": next_node.effect_label,
                    }
                    if next_node is not None
                    else None
                ),
                "recruit_node_code": f"L0_RECRUIT_{hero.hero_code}",
            }
        )
    return result


def _constellation_layers(
    db: Session,
    *,
    user_id: str,
    heroes: list[GameHeroModel],
) -> tuple[list[dict], str | None]:
    large_nodes = (
        db.query(GameConstellationNodeModel)
        .filter_by(user_id=user_id, node_size="LARGE")
        .all()
    )
    node_by_layer_hero = {
        (node.layer, node.hero_code): node
        for node in large_nodes
        if node.hero_code is not None
    }
    layer_zero_heroes = {
        hero_code
        for layer, hero_code in node_by_layer_hero
        if layer == 0
    }
    starter_hero_code = next(
        (
            hero.hero_code
            for hero in heroes
            if hero.recruited and hero.hero_code not in layer_zero_heroes
        ),
        None,
    )

    layers: list[dict] = []
    recruit_nodes = []
    if starter_hero_code is not None:
        for hero in heroes:
            if hero.hero_code == starter_hero_code:
                continue
            saved_node = node_by_layer_hero.get((0, hero.hero_code))
            recruit_nodes.append(
                {
                    "node_code": (
                        saved_node.node_code
                        if saved_node is not None
                        else f"L0_RECRUIT_{hero.hero_code}"
                    ),
                    "layer": 0,
                    "hero_code": hero.hero_code,
                    "role_name": hero.role_name,
                    "node_kind": "RECRUIT",
                    "state": "UNLOCKED" if hero.recruited else "LOCKED",
                    "advancement_tier": hero.advancement_tier,
                }
            )
    layers.append(
        {
            "layer": 0,
            "title": "용사 영입",
            "node_count": len(recruit_nodes),
            "nodes": recruit_nodes,
        }
    )

    for layer in range(1, 7):
        advancement_nodes = []
        for hero in heroes:
            saved_node = node_by_layer_hero.get((layer, hero.hero_code))
            unlocked = saved_node is not None or hero.advancement_tier >= layer
            is_next = (
                hero.recruited
                and not unlocked
                and hero.advancement_tier == layer - 1
            )
            advancement_nodes.append(
                {
                    "node_code": (
                        saved_node.node_code
                        if saved_node is not None
                        else f"L{layer}_ADVANCE_{hero.hero_code}"
                    ),
                    "layer": layer,
                    "hero_code": hero.hero_code,
                    "role_name": hero.role_name,
                    "node_kind": "ADVANCEMENT",
                    "state": (
                        "UNLOCKED"
                        if unlocked
                        else "NEXT"
                        if is_next
                        else "LOCKED"
                    ),
                    "advancement_tier": hero.advancement_tier,
                }
            )
        layers.append(
            {
                "layer": layer,
                "title": f"{layer}차 전직",
                "node_count": len(advancement_nodes),
                "nodes": advancement_nodes,
            }
        )
    return layers, starter_hero_code
