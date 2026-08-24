from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .models import DelayIncident
from .schemas import DelayIncidentCreate, DelayIncidentRead, RailwayLine, LineStatus, StatusResponse

app = FastAPI(
    title="Mumbai Local Delay Tracker API",
    version="1.0.0",
    description="API for ingesting and querying Mumbai local train delay incidents.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    if payload.direction not in {"UP", "DN"}:
        raise HTTPException(status_code=400, detail="direction must be UP or DN")

    incident = DelayIncident(
        line=payload.line.value,
        direction=payload.direction.value,
        station=payload.station,
        delay_minutes=payload.delay_minutes,
        announcement_text=payload.announcement_text,
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident
