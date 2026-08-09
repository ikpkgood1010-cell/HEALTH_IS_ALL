import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.migration_runner import run

parser = argparse.ArgumentParser(description="WP-0009 migration planner")
parser.add_argument("--dry-run", action="store_true", required=True)
args = parser.parse_args()
for name in run(dry_run=args.dry_run):
    print(name)
