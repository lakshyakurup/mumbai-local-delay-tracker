from datetime import datetime, timezone
from fastapi import APIRouter
from ..database import check_database

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, object]:
    database_ok = check_database()
    return {"status": "ok" if database_ok else "degraded", "database": "ok" if database_ok else "unavailable", "timestamp": datetime.now(timezone.utc).isoformat()}
