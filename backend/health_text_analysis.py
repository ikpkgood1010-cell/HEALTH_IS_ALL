"""Deterministic Korean free-text meal/workout analysis.

The service intentionally keeps estimates transparent.  Known foods use a small
versioned average catalogue; vague household units become confirmation cards.
An optional model-backed extractor can replace the parsing layer later without
changing the API or the stored review contract.
"""
from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class FoodAverage:
    code: str
    name: str
    aliases: tuple[str, ...]
    default_g: float
    low_g: float
    high_g: float
    count_g: float | None
    kcal: float
    carbs: float
    protein: float
    fat: float
    fiber: float
    groups: tuple[str, ...]
    source: str = "국가표준식품성분표·USDA 평균값"


FOODS: tuple[FoodAverage, ...] = (
    FoodAverage("cabbage", "양배추", ("양배추",), 70, 50, 100, None, 25, 5.8, 1.3, .1, 2.5, ("vegetable",)),
    FoodAverage("boiled_egg", "삶은 계란", ("삶은 계란", "삶은계란", "계란", "달걀"), 50, 40, 60, 50, 155, 1.1, 12.6, 10.6, 0, ("protein",)),
    FoodAverage("cooked_rice", "즉석밥", ("햇반", "즉석밥", "밥"), 210, 130, 210, 210, 150, 33.3, 2.8, .7, .5, ("grain",)),
    FoodAverage("spinach", "시금치", ("시금치",), 20, 15, 30, 20, 23, 3.6, 2.9, .4, 2.2, ("vegetable",)),
    FoodAverage("garlic", "마늘", ("마늘",), 16, 12, 24, 4, 149, 33.1, 6.4, .5, 2.1, ("vegetable",)),
    FoodAverage("ginger", "생강", ("생강",), 10, 5, 20, 20, 80, 17.8, 1.8, .8, 2.0, ("vegetable",)),
    FoodAverage("shiitake", "표고버섯", ("냉동표고", "표고버섯", "표고"), 100, 60, 150, 10, 34, 6.8, 2.2, .5, 2.5, ("vegetable",)),
    FoodAverage("cornelian_cherry", "산수유", ("산수유",), 10, 5, 20, 1, 74, 17.8, 1.0, .4, 3.0, ("fruit",), "식품 형태 확인 전 일반 과실 평균 후보"),
    FoodAverage("burdock", "우엉", ("우엉",), 15, 10, 25, None, 72, 17.3, 1.5, .2, 3.3, ("vegetable",)),
    FoodAverage("chicken_breast", "닭가슴살", ("닭가슴살", "닭 가슴살"), 120, 100, 150, 120, 165, 0, 31.0, 3.6, 0, ("protein",)),
    FoodAverage("onion", "양파", ("생양파", "양파"), 200, 150, 250, 200, 40, 9.3, 1.1, .1, 1.7, ("vegetable",)),
    FoodAverage("tofu", "두부", ("두부",), 150, 100, 300, None, 76, 1.9, 8.1, 4.8, .3, ("protein",)),
    FoodAverage("sweet_potato", "고구마", ("고구마",), 150, 100, 250, 150, 86, 20.1, 1.6, .1, 3.0, ("grain",)),
    FoodAverage("banana", "바나나", ("바나나",), 120, 90, 150, 120, 89, 22.8, 1.1, .3, 2.6, ("fruit",)),
    FoodAverage("apple", "사과", ("사과",), 200, 150, 250, 200, 52, 13.8, .3, .2, 2.4, ("fruit",)),
    FoodAverage("milk", "우유", ("우유",), 200, 180, 250, None, 61, 4.8, 3.2, 3.3, 0, ("protein", "drink")),
    FoodAverage("yogurt", "요거트", ("그릭요거트", "요거트", "요구르트"), 100, 80, 150, None, 73, 3.9, 9.9, 1.9, 0, ("protein",)),
    FoodAverage("bread", "빵", ("식빵", "빵"), 70, 40, 120, None, 265, 49.0, 9.0, 3.2, 2.7, ("grain",)),
    FoodAverage("kimchi", "김치", ("김치",), 50, 30, 100, None, 21, 3.6, 1.6, .5, 2.5, ("vegetable",)),
    # Frequent quick-entry foods.  These are intentionally *not* treated as
    # product-accurate: each produces a portion confirmation card and is
    # replaced by an official candidate when the relevant API is configured.
    FoodAverage("fried_chicken", "치킨", ("후라이드치킨", "프라이드치킨", "치킨"), 180, 120, 280, 180, 269, 8.5, 19.0, 17.0, .5, ("protein",), "제품·조리법 확인 전 치킨 평균값"),
    FoodAverage("hot_dog", "핫도그", ("핫도그",), 120, 80, 180, 120, 290, 26.0, 11.0, 17.0, .8, ("grain", "protein"), "제품·조리법 확인 전 핫도그 평균값"),
    FoodAverage("instant_ramen", "라면", ("컵라면", "라면"), 120, 90, 150, 120, 460, 62.0, 9.0, 18.0, 2.5, ("grain",), "제품·조리법 확인 전 라면 평균값"),
    FoodAverage("tteok_skewer", "떡꼬치", ("떡꼬치",), 80, 50, 130, 80, 220, 43.0, 3.5, 3.0, 1.0, ("grain",), "제품·소스 확인 전 떡꼬치 평균값"),
)


KOREAN_NUMBERS = {"반": .5, "한": 1.0, "두": 2.0, "세": 3.0, "네": 4.0}


def _round(value: float) -> float:
    return round(value, 1)


def _nutrients(food: FoodAverage, grams: float) -> dict[str, float]:
    factor = grams / 100.0
    return {
        "kcal": _round(food.kcal * factor),
        "carbs_g": _round(food.carbs * factor),
        "protein_g": _round(food.protein * factor),
        "fat_g": _round(food.fat * factor),
        "fiber_g": _round(food.fiber * factor),
    }


def _quantity_near(text: str, alias: str, food: FoodAverage) -> tuple[float, str, bool]:
    position = text.find(alias)
    nearby = text[position: position + len(alias) + 16]
    direct_g = re.search(r"(\d+(?:\.\d+)?)\s*(?:g|그램)", nearby, re.I)
    if direct_g:
        return float(direct_g.group(1)), f"직접 입력 {direct_g.group(1)}g", False
    if "한줌" in nearby or "한 줌" in nearby:
        return food.default_g, "한 줌 평균값", True
    if "손가락 한마디" in nearby or "손가락 한 마디" in nearby:
        return food.default_g, "손가락 한 마디 평균값", True
    half = re.search(r"(?:반|0\.5)\s*(개|쪽|봉지|마리|조각|꼬치|인분)", nearby)
    if half and food.count_g:
        return food.count_g * .5, "반 개 평균값", True
    count = re.search(r"(\d+(?:\.\d+)?)\s*(개|알|쪽|큐브|장|팩|봉지|마리|조각|꼬치|인분|그릇|컵)", nearby)
    if count and food.count_g:
        number = float(count.group(1))
        return number * food.count_g, f"{count.group(1)}{count.group(2)} 평균값", True
    korean_count = re.search(r"(한|두|세|네)\s*(개|알|쪽|큐브|장|팩|봉지|마리|조각|꼬치|인분|그릇|컵)", nearby)
    if korean_count and food.count_g:
        number = KOREAN_NUMBERS[korean_count.group(1)]
        return number * food.count_g, f"{korean_count.group(1)} {korean_count.group(2)} 평균값", True
    return food.default_g, "일반 1회 제공량 평균값", True


def _card(food: FoodAverage, grams: float, reason: str) -> dict[str, Any]:
    options = sorted({
        _round(grams * food.low_g / food.default_g),
        _round(grams),
        _round(grams * food.high_g / food.default_g),
    })
    return {
        "id": f"grams_{food.code}",
        "question": f"{food.name} 양을 {grams:g}g으로 계산할까요?",
        "help": f"{reason}을 사용했습니다. 실제 양과 가까운 값을 선택해 주세요.",
        "recommended_value": grams,
        "options": [{"label": f"{value:g}g", "value": value} for value in options],
    }


def _totals(items: Iterable[dict[str, Any]], key: str = "nutrients") -> dict[str, float]:
    fields = ("kcal", "carbs_g", "protein_g", "fat_g", "fiber_g")
    return {field: _round(sum(float(item[key][field]) for item in items)) for field in fields}


def _append_external_food(
    *,
    items: list[dict[str, Any]],
    cards: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    answers: dict[str, float],
    query: str,
    candidate_id: str,
    grams_id: str,
    not_found_id: str,
) -> None:
    """Add one unresolved food's official candidate/portion confirmation flow."""
    if not candidates:
        cards.append({
            "id": not_found_id,
            "question": f"‘{query}’의 영양 정보를 찾지 못했어요.",
            "help": "제품명·브랜드·중량을 더 구체적으로 적어 주세요. 추정값을 임의로 저장하지 않습니다.",
            "recommended_value": 0,
            "options": [],
        })
        return

    selected_index = answers.get(candidate_id)
    if selected_index is None or not 0 <= int(selected_index) < len(candidates):
        cards.append({
            "id": candidate_id,
            "question": f"공식 데이터에서 ‘{query}’와 가장 가까운 음식을 선택해 주세요.",
            "help": "이름·제조사·영양값을 비교한 뒤 실제로 먹은 항목을 선택합니다.",
            "recommended_value": 0,
            "options": [
                {
                    "label": " · ".join(filter(None, (
                        str(candidate.get("name") or "음식"),
                        str(candidate.get("brand") or ""),
                        str(candidate.get("source_label") or ""),
                    ))),
                    "value": index,
                }
                for index, candidate in enumerate(candidates)
            ],
        })
        return

    candidate = candidates[int(selected_index)]
    basis_g = max(float(candidate.get("basis_g") or 100), 1)
    suggested_g = max(float(candidate.get("serving_g") or basis_g), 1)
    grams = float(answers.get(grams_id, suggested_g))
    confirmed = grams_id in answers
    low_g = grams if confirmed else grams * .75
    high_g = grams if confirmed else grams * 1.25

    def external_nutrients(weight: float) -> dict[str, float]:
        factor = weight / basis_g
        return {
            key: _round(float(candidate.get(key) or 0) * factor)
            for key in ("kcal", "carbs_g", "protein_g", "fat_g", "fiber_g")
        }

    nutrients = external_nutrients(grams)
    groups = ["product"]
    if nutrients["protein_g"] >= 10:
        groups.append("protein")
    if nutrients["carbs_g"] >= 15:
        groups.append("grain")
    items.append({
        "code": f"{candidate.get('provider')}:{candidate.get('food_id')}",
        "name": candidate.get("name") or query,
        "grams": _round(grams),
        "range_g": [_round(low_g), _round(high_g)],
        "basis": f"공식 DB {basis_g:g}g 기준",
        "source": candidate.get("source_label") or candidate.get("provider") or "공식 영양 DB",
        "groups": groups,
        "nutrients": nutrients,
        "nutrients_low": external_nutrients(low_g),
        "nutrients_high": external_nutrients(high_g),
    })
    if not confirmed:
        cards.append({
            "id": grams_id,
            "question": f"{candidate.get('name') or query}을 {suggested_g:g}g 먹었나요?",
            "help": "공식 DB의 1회 제공량 후보입니다. 실제 섭취량과 가까운 값을 골라 주세요.",
            "recommended_value": suggested_g,
            "options": [
                {"label": f"{value:g}g", "value": value}
                for value in sorted({_round(suggested_g * .5), _round(suggested_g), _round(suggested_g * 1.5)})
            ],
        })


def analyze_meal_text(
    text: str,
    *,
    meal_type: str,
    answers: dict[str, float] | None = None,
    reference_detail: dict[str, Any] | None = None,
    external_candidates: list[dict[str, Any]] | None = None,
    external_candidates_by_query: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    answers = answers or {}
    external_candidates = external_candidates or []
    external_candidates_by_query = external_candidates_by_query or {}
    normalized = re.sub(r"\s+", " ", text.strip())
    if re.search(r"(점심|아침|저녁).{0,8}(똑같|동일)", normalized) and reference_detail:
        copied = dict(reference_detail)
        copied["meal_type"] = meal_type
        copied["original_text"] = normalized
        copied["copied_from_meal"] = True
        copied["confirmation_cards"] = []
        copied["summary"] = f"오늘 {reference_detail.get('meal_type', '이전 식사')} 기록과 같은 구성"
        return _meal_response(copied)

    found: list[tuple[int, FoodAverage, str]] = []
    occupied: list[tuple[int, int]] = []
    for food in FOODS:
        best: tuple[int, str] | None = None
        for alias in sorted(food.aliases, key=len, reverse=True):
            pos = normalized.find(alias)
            if pos >= 0 and (best is None or pos < best[0]):
                best = (pos, alias)
        if best is None:
            continue
        start, alias = best
        end = start + len(alias)
        if any(start < used_end and end > used_start for used_start, used_end in occupied):
            continue
        occupied.append((start, end))
        found.append((start, food, alias))

    items: list[dict[str, Any]] = []
    cards: list[dict[str, Any]] = []
    for _, food, alias in sorted(found):
        inferred_g, reason, vague = _quantity_near(normalized, alias, food)
        grams = float(answers.get(f"grams_{food.code}", inferred_g))
        low_g = (
            grams
            if not vague or f"grams_{food.code}" in answers
            else grams * food.low_g / food.default_g
        )
        high_g = (
            grams
            if not vague or f"grams_{food.code}" in answers
            else grams * food.high_g / food.default_g
        )
        item = {
            "code": food.code,
            "name": food.name,
            "grams": _round(grams),
            "range_g": [_round(low_g), _round(high_g)],
            "basis": reason,
            "source": food.source,
            "groups": list(food.groups),
            "nutrients": _nutrients(food, grams),
            "nutrients_low": _nutrients(food, low_g),
            "nutrients_high": _nutrients(food, high_g),
        }
        items.append(item)
        if vague and f"grams_{food.code}" not in answers:
            cards.append(_card(food, grams, reason))

    # Legacy single-query argument is retained for API compatibility.  The
    # query map is the compound-meal path: local and official items coexist,
    # and every unresolved food receives its own candidate/portion answer.
    has_local_items = bool(items)
    if not items and external_candidates:
        _append_external_food(
            items=items,
            cards=cards,
            candidates=external_candidates,
            answers=answers,
            query="입력한 음식",
            candidate_id="external_candidate_index",
            grams_id="external_grams",
            not_found_id="food_not_found",
        )
    for index, (query, candidates) in enumerate(external_candidates_by_query.items()):
        # Preserve the original one-food answer IDs for already deployed
        # clients. Compound (or local+external) input uses independent IDs.
        legacy_single_query = not has_local_items and len(external_candidates_by_query) == 1
        suffix = str(index)
        _append_external_food(
            items=items,
            cards=cards,
            candidates=candidates,
            answers=answers,
            query=query,
            candidate_id="external_candidate_index" if legacy_single_query else f"external_candidate_index_{suffix}",
            grams_id="external_grams" if legacy_single_query else f"external_grams_{suffix}",
            not_found_id="food_not_found" if legacy_single_query else f"food_not_found_{suffix}",
        )

    if not items and not cards:
        cards.append({
            "id": "food_not_found",
            "question": "계산할 수 있는 음식명을 찾지 못했어요.",
            "help": "제품명·음식명·수량을 더 구체적으로 적어 주세요. 외부 공식 DB 키가 설정되면 제품 후보도 자동 검색합니다.",
            "recommended_value": 0,
            "options": [],
        })

    groups = {group for item in items for group in item["groups"]}
    score = round(100 * (
        .25
        + (.20 if "protein" in groups else 0)
        + (.20 if groups.intersection({"vegetable", "fruit"}) else 0)
        + (.15 if "grain" in groups else 0)
        + (.10 if "drink" in groups or re.search(r"물|무가당", normalized) else 0)
        + .10
    )) if items else 0
    detail = {
        "analysis_version": "meal_text_v1",
        "meal_type": meal_type,
        "original_text": normalized,
        "items": items,
        "totals": _totals(items) if items else _empty_nutrients(),
        "totals_low": _totals(items, "nutrients_low") if items else _empty_nutrients(),
        "totals_high": _totals(items, "nutrients_high") if items else _empty_nutrients(),
        "meal_score": score,
        "food_variety_count": len(items),
        "interval_minutes": [int(value) for value in re.findall(r"(\d+)\s*분\s*(?:후|뒤)", normalized)],
        "preparation_methods": [
            label for token, label in (("삶", "삶기"), ("전자레인지", "전자레인지"), ("생", "생식"), ("냉동", "냉동 식품"))
            if token in normalized
        ],
        "confirmation_cards": cards,
        "summary": f"{len(items)}개 식품 · 식단점수 {score}점",
        "sources": sorted({item["source"] for item in items}),
    }
    return _meal_response(detail)


def _empty_nutrients() -> dict[str, float]:
    return {field: 0.0 for field in ("kcal", "carbs_g", "protein_g", "fat_g", "fiber_g")}


def _compact_meal_detail(detail: dict[str, Any]) -> dict[str, Any]:
    return {
        "analysis_version": detail["analysis_version"],
        "meal_type": detail["meal_type"],
        "original_text": detail["original_text"],
        "meal_score": detail["meal_score"],
        "food_variety_count": detail.get("food_variety_count", len(detail["items"])),
        "interval_minutes": detail.get("interval_minutes", []),
        "preparation_methods": detail.get("preparation_methods", []),
        "totals": detail["totals"],
        "totals_low": detail["totals_low"],
        "totals_high": detail["totals_high"],
        "sources": detail.get("sources", []),
        "items": [
            {"name": item["name"], "grams": item["grams"]}
            for item in detail["items"]
        ],
        "copied_from_meal": bool(detail.get("copied_from_meal")),
    }


def _meal_response(detail: dict[str, Any]) -> dict[str, Any]:
    totals = detail.get("totals", _empty_nutrients())
    return {
        "record_type": "meal_log",
        "status": "NEEDS_CONFIRMATION" if detail.get("confirmation_cards") else "READY",
        "summary": detail.get("summary", "식단 분석 완료"),
        "estimated": {
            "totals": totals,
            "totals_low": detail.get("totals_low", totals),
            "totals_high": detail.get("totals_high", totals),
            "meal_score": detail.get("meal_score", 0),
            "food_variety_count": detail.get("food_variety_count", len(detail.get("items", []))),
            "interval_minutes": detail.get("interval_minutes", []),
            "preparation_methods": detail.get("preparation_methods", []),
        },
        "confirmation_cards": detail.get("confirmation_cards", []),
        "reward_preview": {"base_exp": 30, "health_essence": 1},
        "storage_detail": _compact_meal_detail(detail),
        "value": max(float(totals.get("kcal", 0)), .1),
        "items": detail.get("items", []),
        "sources": detail.get("sources", []),
    }


def analyze_workout_text(text: str, *, answers: dict[str, float] | None = None) -> dict[str, Any]:
    answers = answers or {}
    normalized = re.sub(r"\s+", " ", text.strip())
    blocks: list[dict[str, Any]] = []
    cards: list[dict[str, Any]] = []

    cindy = re.search(r"(?i)cindy|신디", normalized)
    if cindy:
        minutes_match = re.search(r"(\d+)\s*분(?:간)?[^.]{0,20}(?:크로스핏\s*)?(?:CINDY|신디)", normalized, re.I)
        minutes = int(minutes_match.group(1)) if minutes_match else 20
        rounds_match = re.search(r"총\s*(\d+)\s*(?:회|라운드)", normalized)
        rounds = int(rounds_match.group(1)) if rounds_match else None
        blocks.append({
            "type": "CROSSFIT_CINDY", "label": "CrossFit Cindy", "duration_min": minutes,
            "rounds": rounds, "reps": rounds * 30 if rounds else None,
            "details": {"pull_ups": rounds * 5, "push_ups": rounds * 10, "air_squats": rounds * 15} if rounds else {},
        })

    stairs = re.search(r"계단\s*(\d+)\s*[~～\-]\s*(\d+)층[^.]{0,30}?(\d+)번", normalized)
    if stairs:
        start, end, repeats = map(int, stairs.groups())
        blocks.append({
            "type": "STAIRS", "label": "계단 오르기", "floor_gain": max(0, end - start) * repeats,
            "start_floor": start, "end_floor": end, "repeats": repeats,
            "descent": "ELEVATOR" if "엘리베이터" in normalized else "UNKNOWN",
        })

    set_match = re.search(r"총\s*(\d+)세트", normalized)
    if "케틀벨" in normalized or "웨이트" in normalized:
        blocks.append({
            "type": "STRENGTH_COMPLEX", "label": "케틀벨·웨이트 복합 세트",
            "sets": int(set_match.group(1)) if set_match else None,
            "muscles": [name for token, name in (("이두", "이두"), ("어깨측면", "어깨 측면"), ("어깨후면", "어깨 후면")) if token in normalized],
        })

    explicit_total = re.search(r"(?:전체|총 운동시간|총시간)\s*(?:은|이)?\s*(\d+)\s*분", normalized)
    known_active = sum(int(block.get("duration_min") or 0) for block in blocks)
    suggested_total = max(known_active, 45 if len(blocks) > 1 else known_active)
    inferred_total = int(answers.get("total_duration_min", explicit_total.group(1) if explicit_total else suggested_total))
    if not explicit_total and "total_duration_min" not in answers:
        cards.append({
            "id": "total_duration_min", "question": "전체 운동시간은 몇 분인가요?",
            "help": f"문장에서 확정된 시간은 {known_active}분입니다. 계단과 웨이트 시간을 포함해 선택해 주세요.",
            "recommended_value": suggested_total,
            "options": [{"label": f"{value}분", "value": value} for value in sorted({max(known_active, 30), max(known_active, 45), max(known_active, 60)})],
        })
    rpe = int(answers.get("rpe", 8))
    if not re.search(r"RPE\s*\d+", normalized, re.I) and "rpe" not in answers:
        cards.append({
            "id": "rpe", "question": "전체 체감강도(RPE)는 어느 정도였나요?",
            "help": "강도 추정보다 사용자의 체감강도를 우선합니다.", "recommended_value": 8,
            "options": [{"label": "6 · 적당함", "value": 6}, {"label": "8 · 힘듦", "value": 8}, {"label": "9 · 매우 힘듦", "value": 9}],
        })
    rest_matches = re.findall(r"(?:휴식(?:시간)?\s*|)(\d+)\s*(초|분)\s*(?:쉬|휴식)", normalized)
    rest_matches += re.findall(r"휴식(?:시간)?\s*(\d+)\s*(초|분)", normalized)
    rest_seconds = sorted({int(value) * (60 if unit == "분" else 1) for value, unit in rest_matches})
    no_rest_transitions = len(re.findall(r"(?:쉬는\s*시간|휴식)\s*없이", normalized))
    activity_score = _round(100 * (1 - math.exp(-(inferred_total * (.6 + rpe / 10)) / 45)))
    detail = {
        "analysis_version": "workout_text_v1", "original_text": normalized, "blocks": blocks,
        "duration_min": inferred_total, "known_duration_min": known_active, "rpe": rpe,
        "rest_seconds": rest_seconds, "no_rest_transitions": no_rest_transitions,
        "activity_score": activity_score,
    }
    return {
        "record_type": "workout_log",
        "status": "NEEDS_CONFIRMATION" if cards else "READY",
        "summary": f"운동 블록 {len(blocks)}개 · {inferred_total}분 · RPE {rpe}",
        "estimated": {
            "duration_min": inferred_total,
            "rpe": rpe,
            "activity_score": activity_score,
            "rest_seconds": rest_seconds,
            "no_rest_transitions": no_rest_transitions,
            "block_count": len(blocks),
        },
        "confirmation_cards": cards,
        "reward_preview": {"base_exp": 50, "health_essence": 1 if inferred_total < 30 else 2 if inferred_total < 60 else 3},
        "storage_detail": detail,
        "value": float(inferred_total),
        "blocks": blocks,
        "sources": ["사용자 확정 시간·RPE", "운동별 구조화 기록"],
    }


def daily_review(records: Iterable[Any], rewards: dict[str, int]) -> dict[str, Any]:
    meals: list[dict[str, Any]] = []
    workouts: list[dict[str, Any]] = []
    nutrition = _empty_nutrients()
    nutrition_low = _empty_nutrients()
    nutrition_high = _empty_nutrients()
    total_exp = 0
    total_essence = 0
    for record in records:
        try:
            detail = json.loads(record.detail_json) if record.detail_json else {}
        except (TypeError, ValueError):
            detail = {}
        total_exp += int(record.exp_gained or 0)
        total_essence += int(rewards.get(record.activity_id, 0))
        if record.record_type == "meal_log":
            totals = detail.get("totals", {"kcal": record.value})
            for field in nutrition:
                nutrition[field] += float(totals.get(field, 0))
                nutrition_low[field] += float(detail.get("totals_low", totals).get(field, 0))
                nutrition_high[field] += float(detail.get("totals_high", totals).get(field, 0))
            meals.append({
                "record_id": record.activity_id, "meal_type": detail.get("meal_type", "식사"),
                "text": detail.get("original_text"), "score": detail.get("meal_score"),
                "totals": totals, "items": detail.get("items", []), "exp": record.exp_gained,
                "sources": detail.get("sources", []),
                "food_variety_count": detail.get("food_variety_count", len(detail.get("items", []))),
                "interval_minutes": detail.get("interval_minutes", []),
                "preparation_methods": detail.get("preparation_methods", []),
                "health_essence": rewards.get(record.activity_id, 0),
            })
        elif record.record_type == "workout_log":
            workouts.append({
                "record_id": record.activity_id, "text": detail.get("original_text"),
                "duration_min": detail.get("duration_min", record.value), "rpe": detail.get("rpe"),
                "activity_score": detail.get("activity_score"), "blocks": detail.get("blocks", []),
                "exp": record.exp_gained, "health_essence": rewards.get(record.activity_id, 0),
            })
    scores = [float(meal["score"]) for meal in meals if meal.get("score") is not None]
    return {
        "meal_count": len(meals), "workout_count": len(workouts),
        "nutrition": {key: _round(value) for key, value in nutrition.items()},
        "nutrition_low": {key: _round(value) for key, value in nutrition_low.items()},
        "nutrition_high": {key: _round(value) for key, value in nutrition_high.items()},
        "meal_score": _round(sum(scores) / len(scores)) if scores else None,
        "workout_minutes": _round(sum(float(item["duration_min"]) for item in workouts)),
        "exp_earned": total_exp, "health_essence_earned": total_essence,
        "meals": meals, "workouts": workouts,
        "disclaimer": "추정값은 기록 보조용이며 의료 진단이나 치료 기준이 아닙니다.",
    }
