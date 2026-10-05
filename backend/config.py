from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "Mumbai Local Delay Tracker API"
    environment: str = "development"
    database_url: str = "sqlite:///./delay_tracker.db"
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    scraper_source_url: str = "https://m-indicator.com/"
    scraper_timeout_seconds: float = Field(default=10, gt=0, le=60)
    scraper_token: str | None = None
    rate_limit: str = "120/minute"

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
