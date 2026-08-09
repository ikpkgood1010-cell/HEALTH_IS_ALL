"""Read-only PostgreSQL schema fingerprint; never prints DATABASE_URL."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


def normalize_type(value: object) -> str:
    """Map SQLAlchemy/PostgreSQL spellings to stable comparison names."""
    text = str(value).lower().strip()
    if text.startswith(("varchar", "character varying", "string")):
        return "character varying"
    if text in {"datetime", "timestamp", "timestamp without time zone"}:
        return "timestamp without time zone"
    if text in {"float", "double precision", "double"}:
        return "double precision"
    return text


def baseline() -> dict[str, dict[str, object]]:
    """Build the expected schema from the canonical ORM metadata."""
    from backend.database import Base

    result: dict[str, dict[str, object]] = {}
    for table in Base.metadata.sorted_tables:
        result[table.name] = {
            "columns": {
                column.name: {
                    "type": normalize_type(column.type),
                    "nullable": column.nullable,
                }
                for column in table.columns
            },
            "pk": sorted(column.name for column in table.primary_key.columns),
            "fk": sorted(
                f"{foreign_key.parent.name}->{foreign_key.target_fullname}"
                for foreign_key in table.foreign_keys
            ),
            "indexes": sorted(index.name for index in table.indexes),
        }
    return result


def compare(
    expected: dict[str, dict[str, object]], actual: dict[str, dict[str, object]]
) -> tuple[str, list[dict[str, str]]]:
    """Return MATCH only when the live schema equals the ORM baseline."""
    differences: list[dict[str, str]] = []
    ignored_tables = {"schema_migrations"}

    for name in sorted(set(actual) - set(expected) - ignored_tables):
        differences.append({"table": name, "kind": "extra_table"})

    for name, spec in expected.items():
        found = actual.get(name)
        if not found:
            differences.append({"table": name, "kind": "missing_table"})
            continue

        expected_columns = spec["columns"]
        actual_columns = found["columns"]
        for column, detail in expected_columns.items():
            if column not in actual_columns:
                differences.append({"table": name, "column": column, "kind": "missing_column"})
                continue
            if actual_columns[column]["type"] != detail["type"]:
                differences.append({"table": name, "column": column, "kind": "type"})
            if actual_columns[column]["nullable"] != detail["nullable"]:
                differences.append({"table": name, "column": column, "kind": "nullable"})
        for column in sorted(set(actual_columns) - set(expected_columns)):
            differences.append({"table": name, "column": column, "kind": "extra_column"})

        for field, kind in (("pk", "primary_key"), ("fk", "foreign_key"), ("indexes", "index")):
            if sorted(found[field]) != sorted(spec[field]):
                differences.append({"table": name, "kind": kind})

    return ("DRIFT" if differences else "MATCH"), differences


SCHEMA_QUERIES = (
    "SELECT table_name FROM information_schema.tables "
    "WHERE table_schema = 'public' AND table_type = 'BASE TABLE'",
    "SELECT table_name, column_name, data_type, is_nullable "
    "FROM information_schema.columns WHERE table_schema = 'public'",
    "SELECT tc.table_name, kcu.column_name "
    "FROM information_schema.table_constraints tc "
    "JOIN information_schema.key_column_usage kcu "
    "USING (constraint_name, table_schema) "
    "WHERE tc.constraint_type = 'PRIMARY KEY' AND tc.table_schema = 'public'",
    "SELECT t.relname, index_rel.relname "
    "FROM pg_class t "
    "JOIN pg_namespace ns ON ns.oid = t.relnamespace "
    "JOIN pg_index index_map ON index_map.indrelid = t.oid "
    "JOIN pg_class index_rel ON index_rel.oid = index_map.indexrelid "
    "LEFT JOIN pg_constraint constraint_map ON constraint_map.conindid = index_map.indexrelid "
    "WHERE ns.nspname = 'public' AND constraint_map.oid IS NULL",
    "SELECT tc.table_name, kcu.column_name, ccu.table_name, ccu.column_name "
    "FROM information_schema.table_constraints tc "
    "JOIN information_schema.key_column_usage kcu "
    "USING (constraint_name, table_schema) "
    "JOIN information_schema.constraint_column_usage ccu "
    "USING (constraint_name, table_schema) "
    "WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_schema = 'public'",
)


def collect_actual_schema(database_url: str) -> dict[str, dict[str, object]]:
    """Collect PostgreSQL catalog metadata with SELECT-only queries."""
    import psycopg2

    with psycopg2.connect(database_url) as connection:
        connection.set_session(readonly=True, autocommit=True)
        with connection.cursor() as cursor:
            cursor.execute(SCHEMA_QUERIES[0])
            actual: dict[str, dict[str, object]] = {
                name: {"columns": {}, "pk": [], "fk": [], "indexes": []}
                for (name,) in cursor.fetchall()
            }
            cursor.execute(SCHEMA_QUERIES[1])
            for table, column, data_type, nullable in cursor.fetchall():
                if table in actual:
                    actual[table]["columns"][column] = {
                        "type": normalize_type(data_type),
                        "nullable": nullable == "YES",
                    }
            cursor.execute(SCHEMA_QUERIES[2])
            for table, column in cursor.fetchall():
                if table in actual:
                    actual[table]["pk"].append(column)
            cursor.execute(SCHEMA_QUERIES[3])
            for table, index in cursor.fetchall():
                if table in actual:
                    actual[table]["indexes"].append(index)
            cursor.execute(SCHEMA_QUERIES[4])
            for table, column, target, target_column in cursor.fetchall():
                if table in actual:
                    actual[table]["fk"].append(f"{column}->{target}.{target_column}")
    return actual


def write_report(path: Path, report: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output_path = Path(args.output)
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        write_report(output_path, {"status": "UNKNOWN", "reason": "DATABASE_URL is required"})
        print("DATABASE_URL is required.", file=sys.stderr)
        return 1

    try:
        expected = baseline()
        actual = collect_actual_schema(database_url)
        status, differences = compare(expected, actual)
        write_report(output_path, {"status": status, "differences": differences})
        return 0 if status == "MATCH" else 1
    except Exception:
        write_report(output_path, {"status": "UNKNOWN", "reason": "schema preflight failed"})
        print("schema preflight failed", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
