"""Persistent idempotency helpers for health-record writes.

The original candidate implementation kept keys in process memory.  That could
not survive a Render restart or coordinate multiple workers.  The canonical
runtime instead stores the client UUID directly in ``activity_logs.activity_id``
and lets the database primary key provide the final concurrency guard.
"""
from __future__ import annotations

import json
from typing import Any

from backend.database import ActivityLogModel


DUPLICATE_RECORD_MESSAGE = "이미 건강이가 소중하게 챙겨둔 기록입니다 ✨"


def canonical_detail_json(detail_data: dict[str, Any] | None) -> str | None:
    if not detail_data:
        return None
    return json.dumps(
        detail_data,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def matches_health_record(
    existing: ActivityLogModel,
    *,
    user_id: str,
    record_type: str,
    value: float,
    detail_json: str | None,
) -> bool:
    """Return true only when a reused UUID describes the exact same record."""
    return (
        existing.user_id == user_id
        and existing.record_type == record_type
        and abs(float(existing.value) - float(value)) < 1e-9
        and canonical_detail_json(_parse_detail(existing.detail_json)) == detail_json
    )


def _parse_detail(value: str | None) -> dict[str, Any] | None:
    if not value:
        return None
    parsed = json.loads(value)
    return parsed if isinstance(parsed, dict) else None
