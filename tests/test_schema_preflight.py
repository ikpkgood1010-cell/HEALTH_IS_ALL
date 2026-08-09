import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import schema_preflight


def _schema(*, nullable=False):
    return {
        "health_i_profiles": {
            "columns": {"health_i_id": {"type": "character varying", "nullable": nullable}},
            "pk": ["health_i_id"],
            "fk": [],
            "indexes": ["ix_health_i_profiles_health_i_id"],
        }
    }


def test_compare_matches_equivalent_schema():
    status, differences = schema_preflight.compare(_schema(), _schema())
    assert status == "MATCH"
    assert differences == []


def test_compare_reports_drift_for_nullable_and_extra_column():
    actual = _schema(nullable=True)
    actual["health_i_profiles"]["columns"]["unexpected"] = {
        "type": "integer",
        "nullable": True,
    }
    status, differences = schema_preflight.compare(_schema(), actual)
    assert status == "DRIFT"
    assert {item["kind"] for item in differences} == {"nullable", "extra_column"}


def test_catalog_queries_are_select_only():
    assert all(query.lstrip().lower().startswith("select") for query in schema_preflight.SCHEMA_QUERIES)
