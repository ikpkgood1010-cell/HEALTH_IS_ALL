import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend import migration_runner


def test_plan_contains_only_baseline_migration():
    assert migration_runner.plan() == ["202608090001_orm_baseline.sql"]


def test_checksum_is_stable_hex_digest():
    digest = migration_runner.checksum()
    assert len(digest) == 64
    assert int(digest, 16) >= 0


def test_apply_path_remains_blocked_without_dedicated_registration():
    try:
        migration_runner.run(dry_run=False, approve=True, backup_reference="backup.dump")
    except RuntimeError as error:
        assert "register_baseline" in str(error)
    else:
        raise AssertionError("generic apply must remain blocked")
