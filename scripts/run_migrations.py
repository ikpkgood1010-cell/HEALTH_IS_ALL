"""Run the manual migration planner or the explicitly approved baseline registration."""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.migration_runner import plan, register_baseline


parser = argparse.ArgumentParser(description="Manual PostgreSQL migration operations")
operation = parser.add_mutually_exclusive_group(required=True)
operation.add_argument("--dry-run", action="store_true")
operation.add_argument("--apply-baseline", action="store_true")
parser.add_argument("--approve", action="store_true")
parser.add_argument("--backup-reference")
parser.add_argument("--approved-by")
args = parser.parse_args()

if args.dry_run:
    for name in plan():
        print(name)
    raise SystemExit(0)

if not args.approve or not args.backup_reference or not args.approved_by:
    parser.error("--apply-baseline requires --approve, --backup-reference, and --approved-by")
if not Path(args.backup_reference).is_file():
    parser.error("backup reference file was not found")
database_url = os.getenv("DATABASE_URL")
if not database_url:
    parser.error("DATABASE_URL is required")

try:
    result = register_baseline(
        database_url=database_url,
        backup_reference=args.backup_reference,
        approved_by=args.approved_by,
    )
except Exception:
    print("baseline registration failed", file=sys.stderr)
    raise SystemExit(1)
print(f"baseline registration: {result}")
