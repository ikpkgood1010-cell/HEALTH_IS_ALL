import httpx

from backend.nutrition_data_service import (
    NutritionDataService,
    extract_compound_food_queries,
    extract_food_lookup_query,
)


def test_extract_food_lookup_query_removes_sentence_noise():
    assert extract_food_lookup_query("불닭볶음면 1봉지 먹었어") == "불닭볶음면"


def test_compound_lookup_queries_keep_unresolved_foods_separate():
    assert extract_compound_food_queries(
        "양배추 한 줌과 불닭볶음면 1봉지, 제육볶음 1인분 먹었어",
        known_aliases=("양배추",),
    ) == ["불닭볶음면", "제육볶음"]


def test_usda_search_normalizes_official_food_data():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["api_key"] == "test-key"
        return httpx.Response(200, json={
            "foods": [{
                "fdcId": 123,
                "description": "Greek yogurt, plain",
                "brandOwner": "Example",
                "servingSize": 170,
                "foodNutrients": [
                    {"nutrientName": "Energy", "unitName": "KJ", "value": 305},
                    {"nutrientName": "Energy", "unitName": "KCAL", "value": 73},
                    {"nutrientName": "Protein", "unitName": "G", "value": 9.95},
                    {"nutrientName": "Carbohydrate, by difference", "unitName": "G", "value": 3.94},
                    {"nutrientName": "Total lipid (fat)", "unitName": "G", "value": 1.92},
                    {"nutrientName": "Fiber, total dietary", "unitName": "G", "value": 0},
                ],
            }]
        })

    service = NutritionDataService(
        usda_api_key="test-key",
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    result = service.search("Greek yogurt", limit=3)

    assert result[0]["provider"] == "USDA_FDC"
    assert result[0]["serving_g"] == 170
    assert result[0]["protein_g"] == 9.95


def test_rda_rows_are_grouped_into_one_food_candidate():
    def handler(_: httpx.Request) -> httpx.Response:
        rows = [
            {"fdCode": "R1", "fdNm": "현미밥", "irdntNm": name, "contInfo": value}
            for name, value in (
                ("에너지", "165"),
                ("탄수화물", "34.5"),
                ("단백질", "3.2"),
                ("지방", "1.1"),
                ("총 식이섬유", "1.8"),
            )
        ]
        return httpx.Response(200, json={"body": {"items": rows}})

    service = NutritionDataService(
        rda_api_key="rda-key",
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    result = service.search("현미밥")

    assert len(result) == 1
    assert result[0]["name"] == "현미밥"
    assert result[0]["kcal"] == 165
    assert result[0]["fiber_g"] == 1.8
