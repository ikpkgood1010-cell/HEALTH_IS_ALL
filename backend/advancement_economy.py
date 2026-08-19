"""Permanent per-hero advancement economy for constellation layers 1-6."""
from __future__ import annotations

from dataclasses import dataclass


ADVANCEMENT_NAMES: dict[str, tuple[str, ...]] = {
    "TANKER": ("수호자", "성기사", "철갑 기사", "절대 수호자", "불사의 선봉장", "우주의 거신"),
    "WARRIOR": ("광전사", "전장 투사", "전쟁 군주", "절대 검왕", "파멸의 검성", "초신성 검신"),
    "MAGE": ("원소 마도사", "원소술사", "대마도사", "혼돈의 마도사", "성좌의 현자", "천체 대마도사"),
    "ARCHER": ("명사수", "추적자", "신궁", "질풍의 사수", "차원 사냥꾼", "은하의 신궁"),
    "ROGUE": ("암살자", "그림자 추적자", "악몽의 암살자", "그림자 군주", "환영 검사", "허무의 집행자"),
    "HEALER": ("사제", "고위 사제", "성자", "대신관", "천상의 예언자", "은하의 구원자"),
}

HEALTH_ESSENCE_BASE_COST = 6
STAR_SHARD_STEP_COST = 2
MAX_ADVANCEMENT_TIER = 6


@dataclass(frozen=True)
class AdvancementSpec:
    hero_code: str
    tier: int
    name: str
    health_essence_cost: int
    star_shard_cost: int
    appearance_code: str
    active_skill_slots: int
    effect_label: str


def advancement_spec(hero_code: str, tier: int) -> AdvancementSpec:
    normalized = hero_code.strip().upper()
    if normalized not in ADVANCEMENT_NAMES:
        raise ValueError(f"unknown hero code: {hero_code}")
    if not 1 <= tier <= MAX_ADVANCEMENT_TIER:
        raise ValueError(f"advancement tier must be 1-{MAX_ADVANCEMENT_TIER}")
    return AdvancementSpec(
        hero_code=normalized,
        tier=tier,
        name=ADVANCEMENT_NAMES[normalized][tier - 1],
        health_essence_cost=HEALTH_ESSENCE_BASE_COST * (2**tier),
        star_shard_cost=STAR_SHARD_STEP_COST * max(0, tier - 1),
        appearance_code=f"{normalized}_TIER_{tier}",
        active_skill_slots=tier,
        effect_label=f"{tier}차 전직 외형·패시브 영구 보존, 액티브 스킬 청사진 해금",
    )


def advancement_node_code(hero_code: str, tier: int) -> str:
    return f"L{tier}_ADVANCE_{hero_code.strip().upper()}"
