"""Explicit migration planner; application startup never invokes it."""
from pathlib import Path

MIGRATIONS = tuple(sorted(Path("02_DATABASE").glob("*_schema_migration*.sql")))

def plan() -> list[str]:
    return [path.name for path in MIGRATIONS]

def run(*, dry_run: bool = True) -> list[str]:
    if dry_run:
        return plan()
    from backend.database import engine
    if engine is None:
        raise RuntimeError("DATABASE_URL is required before applying migrations")
    raise RuntimeError("Migration application requires an approved ordering review")
