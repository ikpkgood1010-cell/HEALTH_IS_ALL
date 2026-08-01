#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

checks = [
    (ROOT / "backend/config.py", r'SSOT_EXP_LABEL\s*:\s*str\s*=\s*"([^"]+)"', "Exp", "backend.config SSOT_EXP_LABEL"),
    (ROOT / "backend/config.py", r'SSOT_CHARACTER_NAME\s*:\s*str\s*=\s*"([^"]+)"', "건강이", "backend.config SSOT_CHARACTER_NAME"),
    (ROOT / "backend/config.py", r'DAILY_EXP_CAP\s*:\s*int\s*=\s*int\(os\.getenv\("DAILY_EXP_CAP",\s*"(\d+)"\)\)', "300", "backend.config DAILY_EXP_CAP"),
    (ROOT / "backend/config.py", r'ANTI_FARMING_INTERVAL_MINUTES\s*:\s*int\s*=\s*int\(os\.getenv\("ANTI_FARMING_INTERVAL_MINUTES",\s*"(\d+)"\)\)', "10", "backend.config ANTI_FARMING_INTERVAL_MINUTES"),
    (ROOT / ".env.example", r'^DAILY_EXP_CAP=(\d+)$', "300", ".env.example DAILY_EXP_CAP"),
    (ROOT / ".env.example", r'^ANTI_FARMING_INTERVAL_MINUTES=(\d+)$', "10", ".env.example ANTI_FARMING_INTERVAL_MINUTES"),
    (ROOT / "backend/models.py", r'name:\s*str\s*=\s*Field\(default="([^"]+)"\)', "건강이", "backend.models default spirit name"),
    (ROOT / "backend/models.py", r'daily_exp_cap:\s*int\s*=\s*Field\(default=(\d+)\)', "300", "backend.models daily_exp_cap default"),
    (ROOT / "lib/mock_data_provider.dart", r'_dailyExpCap\s*=\s*(\d+)', "300", "lib mock dailyExpCap"),
    (ROOT / "03_GAME_SYSTEM/EXP_RULE.md", r'Daily Cap은 `?(\d+)`?을 기준으로 한다|Daily Cap: `?(\d+)`?', "300", "EXP_RULE daily cap"),
    (ROOT / "00_PROJECT/CANONICAL_NAMING.md", r'\| Exp \| 사용자 성장 경험치 \| ([^|]+) \|', "Exp", "CANONICAL_NAMING Exp label"),
]

errors: list[str] = []

for path, pattern, expected, label in checks:
    text = path.read_text(encoding="utf-8")
    m = re.search(pattern, text, re.MULTILINE)
    if not m:
        errors.append(f"[MISSING] {label} -> pattern not found in {path.relative_to(ROOT)}")
        continue
    value = next((g for g in m.groups() if g is not None), None)
    if value != expected:
        errors.append(f"[DRIFT] {label} -> expected {expected}, found {value}")

if errors:
    print("Canonical constant check FAILED")
    for e in errors:
        print(e)
    raise SystemExit(1)

print("Canonical constant check PASSED")
