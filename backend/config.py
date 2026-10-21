from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    database_url: str
    cors_origins: str = "http://localhost:3000"
    scraper_token: str
    scraper_source_url: str
    rate_limit: str = "120/minute"
    environment: str = "production"
    log_level: str = "INFO"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
