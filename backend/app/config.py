import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str
    cors_origins: tuple[str, ...]
    api_title: str = "Mumbai Local Delay Tracker API"
    api_version: str = "1.0.0"


def _origins(value: str | None) -> tuple[str, ...]:
    if not value:
        return (
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        )
    return tuple(origin.strip() for origin in value.split(",") if origin.strip())


def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv("DATABASE_URL", "sqlite:///./delay_tracker.db"),
        cors_origins=_origins(os.getenv("CORS_ORIGINS")),
    )
