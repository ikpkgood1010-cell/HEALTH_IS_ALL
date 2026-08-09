"""Explicit migration planner; application startup never invokes it."""
from pathlib import Path

MIGRATIONS = tuple(sorted(Path("migrations").glob("*.sql")))

def plan() -> list[str]:
    return [path.name for path in MIGRATIONS]

def run(*, dry_run: bool = True, approve: bool = False, backup_reference: str = "") -> list[str]:
    if dry_run:
        return plan()
    if not approve or not backup_reference:
        raise RuntimeError("apply requires explicit approval and backup reference")
    raise RuntimeError("apply requires approved baseline tracking and is not automatic")
