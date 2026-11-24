from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database import get_db
from backend.models.database import DelayRecord, Line, Station
from backend.schemas import (
    StatsSummaryResponse,
    StatsSummary,
    MostDelayedStation,
    StatsTrendsResponse,
    TrendItem,
    LineBreakdownDetail,
)

router = APIRouter(prefix="/api/v2/stats", tags=["Stats"])


@router.get("/summary", response_model=StatsSummaryResponse)
def get_summary(
    hours: int = Query(24, ge=1, le=720),
    db: Session = Depends(get_db),
):
    since = datetime.now(timezone.utc) - timedelta(hours=hours)
    records = (
        db.query(DelayRecord)
        .filter(DelayRecord.deleted_at.is_(None), DelayRecord.created_at >= since)
        .all()
    )

    total = len(records)
    avg_delay = round(sum(r.delay_minutes for r in records) / max(1, total), 2)

    hourly = Counter()
    station_delays = defaultdict(list)
    for r in records:
        if r.created_at:
            hourly[r.created_at.hour] += 1
        key = (r.station_name or "Unknown", r.line_id or "unknown")
        station_delays[key].append(r.delay_minutes)

    peak_hour = None
    peak_avg = 0.0
    if hourly:
        peak_hour_num = hourly.most_common(1)[0][0]
        peak_hour = f"{peak_hour_num:02d}:00"
        peak_records = [r for r in records if r.created_at and r.created_at.hour == peak_hour_num]
        peak_avg = round(sum(r.delay_minutes for r in peak_records) / max(1, len(peak_records)), 2)

    most_delayed = MostDelayedStation(name="N/A", line="N/A", avg_delay=0.0)
    if station_delays:
        best = max(
            station_delays.items(),
            key=lambda kv: sum(kv[1]) / len(kv[1]),
        )
        (name, line), vals = best
        most_delayed = MostDelayedStation(
            name=name,
            line=line,
            avg_delay=round(sum(vals) / len(vals), 2),
        )

    on_time_pct = 0
    if total:
        on_time = sum(1 for r in records if r.delay_minutes <= 5)
        on_time_pct = int(round(100 * on_time / total))

    summary = StatsSummary(
        avg_delay_minutes_all_lines=avg_delay,
        peak_hour=peak_hour or "00:00",
        peak_hour_avg_delay=peak_avg,
        total_delays_24h=total,
        most_delayed_station=most_delayed,
        on_time_percentage=on_time_pct,
        measurement_period_hours=hours,
    )
    return StatsSummaryResponse(summary=summary, timestamp=datetime.now(timezone.utc))


@router.get("/trends", response_model=StatsTrendsResponse)
def get_trends(
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db),
):
    since = datetime.now(timezone.utc) - timedelta(days=days)
    records = (
        db.query(DelayRecord)
        .filter(DelayRecord.deleted_at.is_(None), DelayRecord.created_at >= since)
        .all()
    )

    buckets: dict[str, list[DelayRecord]] = defaultdict(list)
    for r in records:
        if r.created_at:
            key = r.created_at.date().isoformat()
            buckets[key].append(r)

    trends = []
    for day, day_records in sorted(buckets.items()):
        line_map: dict[str, list[int]] = defaultdict(list)
        for r in day_records:
            line_map[r.line_id or "unknown"].append(r.delay_minutes)

        breakdown = {
            line: LineBreakdownDetail(
                avg_delay=round(sum(vals) / len(vals), 2),
                count=len(vals),
            )
            for line, vals in line_map.items()
        }

        trends.append(
            TrendItem(
                period=datetime.fromisoformat(day),
                avg_delay_minutes=round(
                    sum(r.delay_minutes for r in day_records) / max(1, len(day_records)), 2
                ),
                delay_count=len(day_records),
                line_breakdown=breakdown,
            )
        )

    return StatsTrendsResponse(trends=trends, granularity="daily")
