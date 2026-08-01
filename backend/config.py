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

    DB_HOST: str = os.getenv("DB_HOST", "")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "health_is_all")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
    SQLALCHEMY_DATABASE_URL: str = os.getenv("SQLALCHEMY_DATABASE_URL", os.getenv("DATABASE_URL", "")).strip()

    @property
    def database_url(self) -> str:
        if self.SQLALCHEMY_DATABASE_URL:
            return self.SQLALCHEMY_DATABASE_URL
        if self.DB_HOST:
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return "sqlite:///./health_is_all.db"


def utc_now() -> datetime:
    """Return a naive UTC datetime for legacy DB compatibility."""
    return datetime.now(timezone.utc).replace(tzinfo=None)

settings = Settings()
