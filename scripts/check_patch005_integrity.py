from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

checks = [
    (ROOT / "backend/config.py", r'SSOT_EXP_LABEL\s*:\s*str\s*=\s*"([^"]+)"', "Exp", "backend.config SSOT_EXP_LABEL"),
    (ROOT / "backend/config.py", r'DAILY_EXP_CAP\s*:\s*int\s*=\s*int\(os\.getenv\("DAILY_EXP_CAP",\s*"(\d+)"\)\)', "300", "backend.config DAILY_EXP_CAP"),
    (ROOT / "backend/config.py", r'ANTI_FARMING_INTERVAL_MINUTES\s*:\s*int\s*=\s*int\(os\.getenv\("ANTI_FARMING_INTERVAL_MINUTES",\s*"(\d+)"\)\)', "10", "backend.config ANTI_FARMING_INTERVAL_MINUTES"),
    (ROOT / "backend/models.py", r'name:\s*str\s*=\s*Field\(default="([^"]+)"\)', "건강이", "backend.models default spirit name"),
    (ROOT / "03_GAME_SYSTEM/EXP_RULE.md", r'Daily Cap은 `?(\d+)`?을 기준으로 한다|Daily Cap: `?(\d+)`?', "300", "EXP_RULE daily cap"),
]

errors: list[str] = []
for path, pattern, expected, label in checks:
    text = path.read_text(encoding="utf-8")
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        errors.append(f"[MISSING] {label} -> pattern not found in {path.relative_to(ROOT)}")
        continue
    value = next((group for group in match.groups() if group is not None), None)
    if value != expected:
        errors.append(f"[DRIFT] {label} -> expected {expected}, found {value}")

if errors:
    print("PATCH-005 integrity check FAILED")
    for error in errors:
        print(error)
    sys.exit(1)

print("PATCH-005 integrity check PASSED")
