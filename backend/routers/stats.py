from collections import Counter
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.database import DelayRecord
from ..schemas import StatsRead

router = APIRouter(prefix="/api/v2/stats", tags=["statistics"])


@router.get("/summary", response_model=StatsRead)
def summary(db: Session = Depends(get_db), hours: int = Query(24, ge=1, le=720)):
    since = datetime.now(timezone.utc) - timedelta(hours=hours)
    records = list(db.scalars(select(DelayRecord).where(DelayRecord.recorded_at >= since)).all())
    by_line = {line: round(sum(r.delay_minutes for r in records if r.line == line) / max(1, sum(r.line == line for r in records)), 2) for line in ("central", "western", "harbour")}
    hourly = Counter(r.recorded_at.hour for r in records if r.recorded_at)
    return StatsRead(window_hours=hours, total_records=len(records), average_delay_minutes=round(sum(r.delay_minutes for r in records) / max(1, len(records)), 2), peak_hour=hourly.most_common(1)[0][0] if hourly else None, by_line=by_line)


@router.get("/trends")
def trends(db: Session = Depends(get_db), days: int = Query(7, ge=1, le=90)):
    since = datetime.now(timezone.utc) - timedelta(days=days)
    records = db.scalars(select(DelayRecord).where(DelayRecord.recorded_at >= since)).all()
    buckets: dict[str, list[int]] = {}
    for record in records:
        key = record.recorded_at.date().isoformat()
        buckets.setdefault(key, []).append(record.delay_minutes)
    return [{"date": key, "average_delay_minutes": round(sum(values) / len(values), 2), "observations": len(values)} for key, values in sorted(buckets.items())]
