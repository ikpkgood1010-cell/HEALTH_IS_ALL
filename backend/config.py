"""Application settings for HEALTH IS ALL."""
import os
from datetime import datetime, timezone


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "HEALTH IS ALL")
    APP_VERSION: str = os.getenv("APP_VERSION", "2.1.0-repair")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    SSOT_EXP_LABEL: str = "Exp"
    SSOT_CHARACTER_NAME: str = "건강이"
    DAILY_EXP_CAP: int = int(os.getenv("DAILY_EXP_CAP", "300"))
    ANTI_FARMING_INTERVAL_MINUTES: int = int(os.getenv("ANTI_FARMING_INTERVAL_MINUTES", "10"))

    DATABASE_URL: str = os.getenv("DATABASE_URL", "").strip()

    @property
    def database_url(self) -> str:
        return self.DATABASE_URL


def utc_now() -> datetime:
    """Return a naive UTC datetime for legacy DB compatibility."""
    return datetime.now(timezone.utc).replace(tzinfo=None)

settings = Settings()
