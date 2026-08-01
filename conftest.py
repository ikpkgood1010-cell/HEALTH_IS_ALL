from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXTRA_PATHS = [ROOT, ROOT / "03_BACKEND", ROOT / "04_FRONTEND"]

for path in EXTRA_PATHS:
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

os.environ.setdefault("SQLALCHEMY_DATABASE_URL", "sqlite:///./health_is_all_test.db")
os.environ.setdefault("APP_NAME", "HEALTH IS ALL")
os.environ.setdefault("APP_VERSION", "2.1.0-repair")
