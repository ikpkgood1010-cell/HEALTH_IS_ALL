import json

from backend.health_text_analysis import analyze_meal_text, analyze_workout_text


BREAKFAST = "양배추 한줌을 먹고 10분 후 삶은 계란 3개를 먹었어"
LUNCH = (
    "양배추 한줌을 먹고 10분 후 햇반에 시금치1큐브, 마늘 4개 편썰고, "
    "생강 반개 편썰고, 냉동표고 10개, 산수유 10알, 우엉 손가락 한마디 "
    "편썰어서 넣고 전자레인지에 6분돌렸고, 닭가슴살 1개랑, 생양파 1개 같이 먹었어."
)
WORKOUT = (
    "20분간 크로스핏 CINDY 수행했고 총 18회 성공했어. 그 다음 20초 쉬고 "
    "계단 3~9층을 왕복 3번 왔다갔다했고 쉬는시간없이 바로했어. 내려올때는 "
    "엘리베이터를 탔어. 끝나고 휴식없이 케틀벨플로우 1종씩+웨이트 1종씩"
    "(이두, 어깨측면, 어깨후면) 진행했고 총 5세트를 세트 간 휴식시간 1분으로 진행했어."
)


def test_detailed_meal_estimates_and_cards():
    breakfast = analyze_meal_text(BREAKFAST, meal_type="아침")
    assert breakfast["estimated"]["meal_score"] == 75
    assert {item["name"] for item in breakfast["items"]} == {"양배추", "삶은 계란"}
    assert breakfast["estimated"]["totals"]["protein_g"] > 19
    egg_card = next(card for card in breakfast["confirmation_cards"] if card["id"] == "grams_boiled_egg")
    assert [option["value"] for option in egg_card["options"]] == [120.0, 150.0, 180.0]
    assert breakfast["estimated"]["totals_low"]["kcal"] > 190

    lunch = analyze_meal_text(LUNCH, meal_type="점심")
    assert lunch["estimated"]["meal_score"] == 90
    assert len(lunch["items"]) == 10
    assert lunch["estimated"]["food_variety_count"] == 10
    assert lunch["estimated"]["interval_minutes"] == [10]
    assert 650 < lunch["estimated"]["totals"]["kcal"] < 720
    assert {card["id"] for card in lunch["confirmation_cards"]} >= {
        "grams_cooked_rice", "grams_spinach", "grams_chicken_breast"
    }
    assert len(json.dumps(lunch["storage_detail"], ensure_ascii=False).encode("utf-8")) < 2000


def test_unknown_meal_stays_blocked_instead_of_saving_fake_calories():
    result = analyze_meal_text("처음 보는 외국 음식 한 접시", meal_type="저녁")

    assert result["status"] == "NEEDS_CONFIRMATION"
    assert result["confirmation_cards"][0]["id"] == "food_not_found"
    assert result["estimated"]["totals"]["kcal"] == 0


def test_official_candidate_requires_food_then_portion_confirmation():
    candidates = [{
        "provider": "MFDS_PRODUCT_DB",
        "food_id": "P1",
        "name": "예시 볶음면",
        "brand": "예시식품",
        "basis_g": 100,
        "serving_g": 140,
        "kcal": 400,
        "carbs_g": 65,
        "protein_g": 8,
        "fat_g": 12,
        "fiber_g": 3,
        "source_label": "식품의약품안전처 식품영양성분DB",
    }]
    choose_food = analyze_meal_text(
        "예시 볶음면 1봉지", meal_type="저녁", external_candidates=candidates
    )
    assert choose_food["confirmation_cards"][0]["id"] == "external_candidate_index"

    choose_portion = analyze_meal_text(
        "예시 볶음면 1봉지",
        meal_type="저녁",
        answers={"external_candidate_index": 0},
        external_candidates=candidates,
    )
    assert choose_portion["confirmation_cards"][0]["id"] == "external_grams"
    assert choose_portion["estimated"]["totals"]["kcal"] == 560

    ready = analyze_meal_text(
        "예시 볶음면 1봉지",
        meal_type="저녁",
        answers={"external_candidate_index": 0, "external_grams": 140},
        external_candidates=candidates,
    )
    assert ready["status"] == "READY"
    assert ready["items"][0]["source"] == "식품의약품안전처 식품영양성분DB"


def test_meal_answers_recalculate_nutrition():
    baseline = analyze_meal_text(LUNCH, meal_type="점심")
    changed = analyze_meal_text(
        LUNCH,
        meal_type="점심",
        answers={"grams_cooked_rice": 130, "grams_chicken_breast": 100},
    )
    assert changed["estimated"]["totals"]["kcal"] < baseline["estimated"]["totals"]["kcal"]
    assert "grams_cooked_rice" not in {card["id"] for card in changed["confirmation_cards"]}


def test_common_quick_foods_are_split_and_confirmed_individually():
    result = analyze_meal_text(
        "치킨 2조각, 핫도그 1개, 라면 1봉지, 떡꼬치 2꼬치 먹었어",
        meal_type="간식",
    )

    assert {item["name"] for item in result["items"]} == {"치킨", "핫도그", "라면", "떡꼬치"}
    assert {card["id"] for card in result["confirmation_cards"]} == {
        "grams_fried_chicken", "grams_hot_dog", "grams_instant_ramen", "grams_tteok_skewer",
    }
    assert result["estimated"]["totals"]["kcal"] > 1000


def test_compound_official_candidates_merge_with_catalogue_foods():
    candidates = {
        "불닭볶음면": [{
            "provider": "MFDS_PRODUCT_DB", "food_id": "N1", "name": "불닭볶음면",
            "brand": "예시사", "basis_g": 100, "serving_g": 140,
            "kcal": 420, "carbs_g": 70, "protein_g": 9, "fat_g": 13,
            "fiber_g": 2, "source_label": "식품의약품안전처 식품영양성분DB",
        }],
        "제육볶음": [{
            "provider": "RDA_NATIONAL_STANDARD_10_4", "food_id": "N2", "name": "제육볶음",
            "brand": None, "basis_g": 100, "serving_g": 180,
            "kcal": 210, "carbs_g": 12, "protein_g": 18, "fat_g": 10,
            "fiber_g": 1, "source_label": "국가표준식품성분 DB 10.4(2026)",
        }],
    }
    text = "양배추 한 줌과 불닭볶음면 1봉지, 제육볶음 1인분 먹었어"
    choosing = analyze_meal_text(text, meal_type="저녁", external_candidates_by_query=candidates)
    assert {item["name"] for item in choosing["items"]} == {"양배추"}
    assert {card["id"] for card in choosing["confirmation_cards"]} >= {
        "grams_cabbage", "external_candidate_index_0", "external_candidate_index_1",
    }

    portions = analyze_meal_text(
        text,
        meal_type="저녁",
        answers={"external_candidate_index_0": 0, "external_candidate_index_1": 0},
        external_candidates_by_query=candidates,
    )
    assert {card["id"] for card in portions["confirmation_cards"]} >= {
        "external_grams_0", "external_grams_1",
    }

    ready = analyze_meal_text(
        text,
        meal_type="저녁",
        answers={
            "grams_cabbage": 70,
            "external_candidate_index_0": 0,
            "external_candidate_index_1": 0,
            "external_grams_0": 140,
            "external_grams_1": 180,
        },
        external_candidates_by_query=candidates,
    )
    assert ready["status"] == "READY"
    assert {item["name"] for item in ready["items"]} == {"양배추", "불닭볶음면", "제육볶음"}
    assert "식품의약품안전처 식품영양성분DB" in ready["sources"]


def test_workout_text_is_split_into_structured_blocks():
    result = analyze_workout_text(WORKOUT)
    assert result["estimated"] == {
        "duration_min": 45,
        "rpe": 8,
        "activity_score": 75.3,
        "rest_seconds": [20, 60],
        "no_rest_transitions": 2,
        "block_count": 3,
    }
    assert result["storage_detail"]["rest_seconds"] == [20, 60]
    assert result["storage_detail"]["no_rest_transitions"] == 2
    cindy = result["blocks"][0]
    assert cindy["rounds"] == 18
    assert cindy["reps"] == 540
    stairs = result["blocks"][1]
    assert stairs["floor_gain"] == 18
    assert stairs["descent"] == "ELEVATOR"
    assert result["reward_preview"] == {"base_exp": 50, "health_essence": 2}
