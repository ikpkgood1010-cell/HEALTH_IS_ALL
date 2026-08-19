"""Official nutrition data adapters with bounded, failure-safe lookup.

Provider order follows the product decision: Korean national composition data,
Korean commercial product data, then USDA FoodData Central.  Missing keys or
provider outages never break the built-in deterministic analyser.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any, Iterable

import httpx


@dataclass(frozen=True)
class NutritionCandidate:
    provider: str
    food_id: str
    name: str
    brand: str | None
    basis_g: float
    serving_g: float
    kcal: float
    carbs_g: float
    protein_g: float
    fat_g: float
    fiber_g: float
    source_label: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _number(value: Any, default: float = 0.0) -> float:
    if value in (None, "", "-", "N/A"):
        return default
    match = re.search(r"-?\d+(?:\.\d+)?", str(value).replace(",", ""))
    return float(match.group(0)) if match else default


def _items_at_any_depth(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        if any(key in value for key in ("fdNm", "FOOD_NM_KR", "foodName", "fdcId")):
            yield value
        for nested in value.values():
            yield from _items_at_any_depth(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _items_at_any_depth(nested)


def extract_food_lookup_query(text: str) -> str:
    """Reduce a short Korean meal sentence to a provider search phrase."""
    cleaned = re.sub(
        r"(?:\d+(?:\.\d+)?|한|두|세|네|반)\s*(?:g|그램|kg|개|알|봉지|팩|장|인분|그릇|컵)",
        " ",
        text,
        flags=re.I,
    )
    cleaned = re.sub(r"(?:먹었어|먹었다|먹음|섭취했어|섭취|오늘|아침|점심|저녁|간식|그리고|같이|후|뒤)", " ", cleaned)
    cleaned = re.sub(r"[^0-9A-Za-z가-힣 ]+", " ", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()[:80]


def extract_compound_food_queries(
    text: str,
    *,
    known_aliases: Iterable[str] = (),
    limit: int = 4,
) -> list[str]:
    """Return plausible *unresolved* food names from a Korean meal sentence.

    This is deliberately a small, deterministic pre-parser rather than a
    pretend-NLP system.  Known catalogue aliases are removed first, then the
    remaining text is split on the conjunctions people normally use when
    listing foods.  Each result is a separate official-data lookup, so
    ``치킨, 핫도그, 라면`` never becomes one meaningless search query.
    """
    remaining = text
    for alias in sorted({alias for alias in known_aliases if alias}, key=len, reverse=True):
        remaining = remaining.replace(alias, " ")

    parts = re.split(
        r"(?:[,，/·+]|\b(?:그리고|및)\b|(?:랑|와|과|하고|먹고|먹은|먹었어|먹었다|"
        r"섭취했어|섭취했다|같이|후|뒤))",
        remaining,
    )
    noise = re.compile(
        r"(?:\d+(?:\.\d+)?|한|두|세|네|반)\s*(?:g|그램|kg|개|알|봉지|팩|장|"
        r"인분|그릇|컵|마리|조각|꼬치|큐브|줌|분|초)|"
        r"(?:오늘|아침|점심|저녁|간식|을|를|이|가|은|는|에|에서|로|으로|"
        r"하고|해서|넣고|넣어|돌렸고|전자레인지|조리|먹어|먹었|섭취|"
        r"처음|보는|외국|음식|한접시|한 접시)",
        re.I,
    )
    queries: list[str] = []
    for part in parts:
        cleaned = noise.sub(" ", part)
        cleaned = re.sub(r"[^0-9A-Za-z가-힣 ]+", " ", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        # Particles can remain attached to a word when the sentence was not
        # split at that particle.  Strip only common trailing particles.
        cleaned = re.sub(r"(?:을|를|이|가|은|는|에|의)$", "", cleaned).strip()
        if len(cleaned) < 2 or cleaned in queries:
            continue
        queries.append(cleaned[:60])
        if len(queries) == limit:
            break
    return queries


class NutritionDataService:
    RDA_URL = "https://www.nics.go.kr/food/kfi/openapi/service"
    MFDS_URL = "https://apis.data.go.kr/1471000/FoodNtrCpntDbInfo02/getFoodNtrCpntDbInq02"
    USDA_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

    def __init__(
        self,
        *,
        rda_api_key: str = "",
        mfds_api_key: str = "",
        usda_api_key: str = "",
        client: httpx.Client | None = None,
    ):
        self.rda_api_key = rda_api_key.strip()
        self.mfds_api_key = mfds_api_key.strip()
        self.usda_api_key = usda_api_key.strip()
        self._client = client or httpx.Client(timeout=4.0, follow_redirects=True)

    @property
    def enabled_providers(self) -> list[str]:
        return [
            name
            for name, key in (
                ("RDA_NATIONAL_STANDARD_10_4", self.rda_api_key),
                ("MFDS_PRODUCT_DB", self.mfds_api_key),
                ("USDA_FDC", self.usda_api_key),
            )
            if key
        ]

    def search(self, query: str, *, limit: int = 5) -> list[dict[str, Any]]:
        phrase = extract_food_lookup_query(query)
        if not phrase:
            return []
        results: list[NutritionCandidate] = []
        for lookup in (self._search_rda, self._search_mfds, self._search_usda):
            try:
                results.extend(lookup(phrase, limit=limit))
            except (httpx.HTTPError, TypeError, ValueError, KeyError):
                continue
            if len(results) >= limit:
                break
        deduped: list[dict[str, Any]] = []
        seen: set[tuple[str, str]] = set()
        for result in results:
            key = (result.provider, result.food_id)
            if key in seen:
                continue
            seen.add(key)
            deduped.append(result.to_dict())
            if len(deduped) == limit:
                break
        return deduped

    def _search_rda(self, query: str, *, limit: int) -> list[NutritionCandidate]:
        if not self.rda_api_key:
            return []
        response = self._client.get(
            self.RDA_URL,
            params={
                "apiKey": self.rda_api_key,
                "serviceType": "AA002",
                "nowPage": 1,
                "pageSize": 500,
                "fdNm": query,
            },
        )
        response.raise_for_status()
        rows = list(_items_at_any_depth(response.json()))
        grouped: dict[str, dict[str, Any]] = {}
        for row in rows:
            food_id = str(row.get("fdCode") or row.get("foodCode") or row.get("fdNm") or "")
            if not food_id:
                continue
            entry = grouped.setdefault(food_id, {"row": row, "nutrients": {}})
            nutrient_name = str(row.get("irdntNm") or row.get("nutrientName") or "").lower()
            entry["nutrients"][nutrient_name] = _number(row.get("contInfo"))
        candidates: list[NutritionCandidate] = []
        for food_id, entry in grouped.items():
            row, nutrients = entry["row"], entry["nutrients"]
            pick = lambda *words: next((value for name, value in nutrients.items() if any(word in name for word in words)), 0.0)
            candidates.append(NutritionCandidate(
                provider="RDA_NATIONAL_STANDARD_10_4",
                food_id=food_id,
                name=str(row.get("fdNm") or row.get("foodName") or query),
                brand=None,
                basis_g=100.0,
                serving_g=100.0,
                kcal=pick("에너지", "열량"),
                carbs_g=pick("탄수화물"),
                protein_g=pick("단백질"),
                fat_g=pick("지방", "지질"),
                fiber_g=pick("식이섬유"),
                source_label="국가표준식품성분 DB 10.4(2026)",
            ))
        return [item for item in candidates if item.kcal > 0][:limit]

    def _search_mfds(self, query: str, *, limit: int) -> list[NutritionCandidate]:
        if not self.mfds_api_key:
            return []
        response = self._client.get(
            self.MFDS_URL,
            params={
                "serviceKey": self.mfds_api_key,
                "type": "json",
                "pageNo": 1,
                "numOfRows": limit,
                "FOOD_NM_KR": query,
            },
        )
        response.raise_for_status()
        candidates: list[NutritionCandidate] = []
        for row in _items_at_any_depth(response.json()):
            name = str(row.get("FOOD_NM_KR") or row.get("DESC_KOR") or "")
            if not name:
                continue
            basis = _number(row.get("NUTRI_AMOUNT_SERVING") or row.get("SERVING_SIZE") or 100, 100)
            serving = _number(row.get("DISH_ONE_SERVING") or row.get("FOOD_SIZE") or basis, basis)
            candidates.append(NutritionCandidate(
                provider="MFDS_PRODUCT_DB",
                food_id=str(row.get("FOOD_CD") or row.get("ITEM_REPORT_NO") or name),
                name=name,
                brand=str(row.get("COMPANY_NM") or row.get("MAKER_NAME") or "") or None,
                basis_g=basis,
                serving_g=serving,
                kcal=_number(row.get("AMT_NUM1") or row.get("NUTR_CONT1")),
                carbs_g=_number(row.get("CARBOHYDRATE") or row.get("NUTR_CONT2")),
                protein_g=_number(row.get("PROTEIN") or row.get("NUTR_CONT3")),
                fat_g=_number(row.get("FAT") or row.get("NUTR_CONT4")),
                fiber_g=_number(row.get("DIETARY_FIBER") or row.get("NUTR_CONT9")),
                source_label="식품의약품안전처 식품영양성분DB",
            ))
        return [item for item in candidates if item.kcal > 0][:limit]

    def _search_usda(self, query: str, *, limit: int) -> list[NutritionCandidate]:
        if not self.usda_api_key:
            return []
        response = self._client.get(
            self.USDA_URL,
            params={"api_key": self.usda_api_key, "query": query, "pageSize": limit},
        )
        response.raise_for_status()
        candidates: list[NutritionCandidate] = []
        for row in response.json().get("foods", []):
            nutrients = row.get("foodNutrients", [])

            def pick(*words: str, unit: str | None = None) -> float:
                for nutrient in nutrients:
                    name = str(nutrient.get("nutrientName", "")).lower()
                    nutrient_unit = str(nutrient.get("unitName", "")).upper()
                    if any(word in name for word in words) and (
                        unit is None or nutrient_unit == unit
                    ):
                        return _number(nutrient.get("value"))
                return 0.0

            candidates.append(NutritionCandidate(
                provider="USDA_FDC",
                food_id=str(row.get("fdcId") or row.get("description") or ""),
                name=str(row.get("description") or query),
                brand=str(row.get("brandOwner") or row.get("brandName") or "") or None,
                basis_g=100.0,
                serving_g=_number(row.get("servingSize"), 100.0),
                kcal=pick("energy", unit="KCAL"),
                carbs_g=pick("carbohydrate"),
                protein_g=pick("protein"),
                fat_g=pick("total lipid", "total fat"),
                fiber_g=pick("fiber, total dietary", "dietary fiber"),
                source_label="USDA FoodData Central",
            ))
        return [item for item in candidates if item.kcal > 0][:limit]

    def close(self) -> None:
        self._client.close()
