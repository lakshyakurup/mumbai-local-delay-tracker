from datetime import datetime, timedelta, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database import get_db
from backend.models.database import DelayRecord, Line, Station
from backend.schemas import (
    LinesStatusResponse,
    LineStatusItem,
    LineStationsResponse,
    StationMetricItem,
)

router = APIRouter(prefix="/api/v2/lines", tags=["Lines"])

KNOWN_LINES = {
    "central": "Central Line",
    "western": "Western Line",
    "harbour": "Harbour Line",
}


@router.get("/status", response_model=LinesStatusResponse)
def get_lines_status(
    hours: int = Query(6, ge=1, le=72),
    db: Session = Depends(get_db),
):
    since = datetime.now(timezone.utc) - timedelta(hours=hours)
    items: List[LineStatusItem] = []

    for line_id, line_name in KNOWN_LINES.items():
        records = (
            db.query(DelayRecord)
            .filter(
                DelayRecord.line_id == line_id,
                DelayRecord.deleted_at.is_(None),
                DelayRecord.created_at >= since,
            )
            .all()
        )

        total = len(records)
        avg = int(round(sum(r.delay_minutes for r in records) / max(1, total))) if total else 0
        delayed = sum(1 for r in records if r.delay_minutes > 5)
        delayed_pct = int(round(100 * delayed / max(1, total))) if total else 0

        if avg == 0 and total == 0:
            status = "UNKNOWN"
        elif avg <= 5:
            status = "ON_TIME"
        elif avg <= 14:
            status = "DELAYED"
        else:
            status = "CRITICAL"

        last_updated = max((r.created_at for r in records), default=datetime.now(timezone.utc))

        station_count = (
            db.query(func.count(Station.id))
            .filter(Station.line_id == line_id)
            .scalar()
            or 0
        )

        items.append(
            LineStatusItem(
                line_id=line_id,
                line_name=line_name,
                status=status,
                avg_delay_minutes=avg,
                delay_percentage=delayed_pct,
                last_updated=last_updated,
                station_count=station_count,
                delayed_stations=delayed,
            )
        )

    return LinesStatusResponse(lines=items, timestamp=datetime.now(timezone.utc))


@router.get("/{line}/stations", response_model=LineStationsResponse)
def get_line_stations(
    line: str,
    db: Session = Depends(get_db),
):
    line_id = line.lower().strip()
    if line_id not in KNOWN_LINES:
        raise HTTPException(status_code=404, detail=f"Unknown line '{line}'")

    stations = (
        db.query(Station)
        .filter(Station.line_id == line_id)
        .order_by(Station.display_order.asc().nullslast(), Station.name.asc())
        .all()
    )

    since = datetime.now(timezone.utc) - timedelta(days=7)
    metrics: List[StationMetricItem] = []

    for st in stations:
        records = (
            db.query(DelayRecord)
            .filter(
                DelayRecord.line_id == line_id,
                DelayRecord.station_name.ilike(st.name),
                DelayRecord.deleted_at.is_(None),
                DelayRecord.created_at >= since,
            )
            .all()
        )
        total = len(records)
        avg = round(sum(r.delay_minutes for r in records) / max(1, total), 1) if total else 0.0
        on_time = sum(1 for r in records if r.delay_minutes <= 5)
        on_time_pct = round(100 * on_time / max(1, total), 1) if total else 100.0
        last = max((r.created_at for r in records), default=None)

        metrics.append(
            StationMetricItem(
                station_id=st.id,
                name=st.name,
                order=st.display_order or 0,
                avg_delay_minutes=avg,
                incidents_7d=total,
                on_time_percentage=on_time_pct,
                last_delay=last,
                passenger_volume_estimate=None,
            )
        )

    return LineStationsResponse(line=line_id, stations=metrics)
