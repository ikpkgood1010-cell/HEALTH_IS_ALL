"""Manual PostgreSQL migration operations; never called by application startup."""
from __future__ import annotations

import hashlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = tuple(sorted((PROJECT_ROOT / "migrations").glob("*.sql")))
BASELINE = MIGRATIONS[0]


def plan() -> list[str]:
    return [path.name for path in MIGRATIONS]


def checksum(path: Path = BASELINE) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _require_schema_match(database_url: str) -> None:
    from scripts.schema_preflight import baseline, collect_actual_schema, compare

    status, _ = compare(baseline(), collect_actual_schema(database_url))
    if status != "MATCH":
        raise RuntimeError("baseline registration blocked: live schema is not MATCH")


def register_baseline(
    *, database_url: str, backup_reference: str, approved_by: str
) -> str:
    """Record the already-existing ORM tables as one immutable migration baseline.

    No application table is created, altered, or deleted.  The live schema is
    compared read-only before this function creates the tracking record.
    """
    if not backup_reference or not approved_by:
        raise RuntimeError("baseline registration requires backup reference and approver")
    _require_schema_match(database_url)

    import psycopg2

    version = BASELINE.stem.split("_", 1)[0]
    digest = checksum()
    with psycopg2.connect(database_url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS schema_migrations ("
                "version VARCHAR(64) PRIMARY KEY, checksum VARCHAR(64) NOT NULL, "
                "migration_name VARCHAR(255) NOT NULL, backup_reference TEXT NOT NULL, "
                "approved_by VARCHAR(255) NOT NULL, "
                "applied_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP)"
            )
            cursor.execute(
                "INSERT INTO schema_migrations "
                "(version, checksum, migration_name, backup_reference, approved_by) "
                "VALUES (%s, %s, %s, %s, %s) "
                "ON CONFLICT (version) DO NOTHING RETURNING version",
                (version, digest, BASELINE.name, backup_reference, approved_by),
            )
            if cursor.fetchone():
                return "registered"
            cursor.execute("SELECT checksum FROM schema_migrations WHERE version = %s", (version,))
            row = cursor.fetchone()
            if not row or row[0] != digest:
                raise RuntimeError("baseline registration blocked: tracking checksum conflict")
            return "already_registered"


def run(*, dry_run: bool = True, approve: bool = False, backup_reference: str = "") -> list[str]:
    if dry_run:
        return plan()
    if not approve or not backup_reference:
        raise RuntimeError("apply requires explicit approval and backup reference")
    raise RuntimeError(
        "generic apply remains blocked; baseline and pending migrations require "
        "their dedicated approved operations"
    )
