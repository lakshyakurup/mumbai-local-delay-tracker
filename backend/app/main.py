import os
from collections import Counter
from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .models import DelayIncident
from .schemas import (
    DelayIncidentCreate,
    DelayIncidentRead,
    DelayStatsResponse,
    LineBreakdownResponse,
    LineStatus,
    RailwayLine,
    StatusResponse,
)

app = FastAPI(
    title="Mumbai Local Delay Tracker API",
    version="1.0.0",
    description="API for ingesting and querying Mumbai local train delay incidents.",
)


def get_cors_origins() -> list[str]:
    configured = os.getenv("CORS_ORIGINS")
    if configured:
        return [origin.strip() for origin in configured.split(",") if origin.strip()]
    return [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def classify_line_status(avg_delay: float, incidents: int) -> str:
    if incidents == 0 or avg_delay <= 3:
        return "Normal"
    if avg_delay <= 10:
        return "Minor Delays"
    return "Major Disruptions"


def normalize_line_name(line_name: str) -> RailwayLine:
    normalized = line_name.strip().lower()
    mapping = {
        "central": RailwayLine.CENTRAL,
        "western": RailwayLine.WESTERN,
        "harbour": RailwayLine.HARBOUR,
    }
    line = mapping.get(normalized)
    if line is None:
        raise HTTPException(
            status_code=404,
            detail="line_name must be one of: central, western, harbour",
        )
    return line


@app.get("/api/delays", response_model=list[DelayIncidentRead])
def get_delays(
    db: Annotated[Session, Depends(get_db)],
    line: RailwayLine | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
) -> list[DelayIncident]:
    query = select(DelayIncident)
    if line:
        query = query.where(DelayIncident.line == line.value)

    incidents = db.scalars(query.order_by(desc(DelayIncident.created_at)).limit(limit)).all()
    return list(incidents)


@app.get("/api/status", response_model=StatusResponse)
def get_status(db: Annotated[Session, Depends(get_db)]) -> StatusResponse:
    lines: list[LineStatus] = []

    for line in RailwayLine:
        incidents = db.scalars(
            select(DelayIncident).where(DelayIncident.line == line.value)
        ).all()

        incident_count = len(incidents)
        avg_delay = (
            round(sum(item.delay_minutes for item in incidents) / incident_count, 2)
            if incident_count > 0
            else 0.0
        )
        lines.append(
            LineStatus(
                line=line,
                status=classify_line_status(avg_delay, incident_count),
                avg_delay_minutes=avg_delay,
                incident_count=incident_count,
            )
        )

    return StatusResponse(updated_at=datetime.now(tz=timezone.utc), lines=lines)


@app.post("/api/delays", response_model=DelayIncidentRead, status_code=201)
def create_delay(
    payload: DelayIncidentCreate,
    db: Annotated[Session, Depends(get_db)],
) -> DelayIncident:
    incident_data = {
        "line": payload.line.value,
        "direction": payload.direction.value,
        "station": payload.station,
        "affected_stretch": payload.affected_stretch,
        "delay_minutes": payload.delay_minutes,
        "priority": payload.priority.value,
        "announcement_text": payload.announcement_text,
    }
    if payload.created_at is not None:
        incident_data["created_at"] = payload.created_at

    incident = DelayIncident(
        **incident_data,
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


@app.get("/api/delays/stats", response_model=DelayStatsResponse)
def get_delay_stats(db: Annotated[Session, Depends(get_db)]) -> DelayStatsResponse:
    incidents = db.scalars(select(DelayIncident)).all()
    total = len(incidents)
    avg_delay = round(sum(item.delay_minutes for item in incidents) / total, 2) if total else 0.0

    line_counter = Counter(item.line for item in incidents)
    worst_line = line_counter.most_common(1)[0][0] if line_counter else None

    stretch_counter = Counter(item.affected_stretch for item in incidents)
    worst_stretch = stretch_counter.most_common(1)[0][0] if stretch_counter else None

    return DelayStatsResponse(
        total_active_delays=total,
        average_delay_minutes=avg_delay,
        worst_affected_line=RailwayLine(worst_line) if worst_line else None,
        most_affected_stretch=worst_stretch,
    )


@app.get("/api/lines/{line_name}", response_model=LineBreakdownResponse)
def get_line_breakdown(
    line_name: str,
    db: Annotated[Session, Depends(get_db)],
) -> LineBreakdownResponse:
    line = normalize_line_name(line_name)
    incidents = db.scalars(
        select(DelayIncident)
        .where(DelayIncident.line == line.value)
        .order_by(desc(DelayIncident.created_at))
    ).all()

    total = len(incidents)
    avg_delay = round(sum(item.delay_minutes for item in incidents) / total, 2) if total else 0.0
    priorities = Counter(item.priority for item in incidents)
    directions = Counter(item.direction for item in incidents)
    stretches = Counter(item.affected_stretch for item in incidents)

    return LineBreakdownResponse(
        line=line,
        total_incidents=total,
        average_delay_minutes=avg_delay,
        worst_stretch=stretches.most_common(1)[0][0] if stretches else None,
        priorities={"Minor": priorities.get("Minor", 0), "Major": priorities.get("Major", 0), "Severe": priorities.get("Severe", 0)},
        directions={"UP": directions.get("UP", 0), "DN": directions.get("DN", 0)},
        recent_incidents=incidents[:25],
    )
