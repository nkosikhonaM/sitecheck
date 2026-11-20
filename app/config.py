"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for SiteCheck."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./sitecheck.db"
    api_key: str | None = None
    dev_mode: bool = False
    retention_days: int = 90


settings = Settings()
