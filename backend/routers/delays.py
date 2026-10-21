from fastapi import APIRouter, Depends, HTTPException, Query, status, Header
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import Optional
from datetime import datetime, timedelta, timezone
import uuid

from backend.database import get_db
from backend.models.database import DelayRecord, Line, Station
from backend.schemas import DelaysListResponse, DelayRecordResponse, DelayCreateRequest, DelayCreateResponse
from backend.config import settings

router = APIRouter(prefix="/api/v2/delays", tags=["Delays"])

@router.get("", response_model=DelaysListResponse)
def get_delays(
    line: Optional[str] = Query(None, description="Filter by line id"),
    station: Optional[str] = Query(None, description="Substring match for station"),
    limit: int = Query(50, ge=1, le=500),
    page: int = Query(1, ge=1),
    sort: Literal["time", "delay_minutes", "station", "line"] = Query("time"),
    hours: int = Query(24, ge=1, le=720),
    db: Session = Depends(get_db)
):
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
    query = db.query(DelayRecord).filter(DelayRecord.deleted_at.is_(None), DelayRecord.created_at >= cutoff_time)

    if line:
        query = query.filter(DelayRecord.line_id == line)
    if station:
        query = query.filter(DelayRecord.station_name.ilike(f"%{station}%"))

    total_records = query.count()

    if sort == "delay_minutes":
        query = query.order_by(DelayRecord.delay_minutes.desc())
    elif sort == "station":
        query = query.order_by(DelayRecord.station_name.asc())
    elif sort == "line":
        query = query.order_by(DelayRecord.line_id.asc())
    else:
        query = query.order_by(DelayRecord.created_at.desc())

    offset = (page - 1) * limit
    records = query.offset(offset).limit(limit).all()

    formatted_records = [
        DelayRecordResponse(
            id=r.id,
            line=r.line_id,
            station=r.station_name or "Unknown",
            delay_minutes=r.delay_minutes,
            direction=r.direction,
            severity=r.severity,
            source=r.source,
            created_at=r.created_at,
            updated_at=r.updated_at
        ) for r in records
    ]

    return DelaysListResponse(
        delays=formatted_records,
        count=len(formatted_records),
        total_records=total_records,
        page=page,
        limit=limit
    )

@router.post("", response_model=DelayCreateResponse, status_code=status.HTTP_201_CREATED)
def create_delay_observation(payload: DelayCreateRequest, db: Session = Depends(get_db)):
    line_exists = db.query(Line).filter(Line.id == payload.line).first()
    if not line_exists:
        raise HTTPException(status_code=400, detail=f"Line '{payload.line}' does not exist.")
    
    station_obj = db.query(Station).filter(Station.line_id == payload.line, Station.name.ilike(payload.station)).first()
    if not station_obj:
        raise HTTPException(status_code=400, detail=f"Station '{payload.station}' does not exist on line '{payload.line}'.")

    five_mins_ago = datetime.now(timezone.utc) - timedelta(minutes=5)
    duplicate = db.query(DelayRecord).filter(
        DelayRecord.line_id == payload.line,
        DelayRecord.station_name.ilike(station_obj.name),
        DelayRecord.created_at >= five_mins_ago,
        DelayRecord.deleted_at.is_(None)
    ).first()

    if duplicate:
        raise HTTPException(status_code=409, detail="Duplicate delay observation recorded recently for this station and line.")

    if payload.delay_minutes <= 5:
        severity = "minor"
    elif payload.delay_minutes <= 14:
        severity = "moderate"
    else:
        severity = "severe"

    new_record = DelayRecord(
        line_id=payload.line,
        station_id=station_obj.id,
        station_name=station_obj.name,
        delay_minutes=payload.delay_minutes,
        direction=payload.direction,
        severity=severity,
        source="user",
        notes=payload.notes
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return DelayCreateResponse(
        id=new_record.id,
        created_at=new_record.created_at,
        status="created"
    )

@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_delay_record(
    record_id: uuid.UUID,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token structure.")
    
    token = authorization.split(" ")[1]
    if token != settings.scraper_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid admin credentials.")

    record = db.query(DelayRecord).filter(DelayRecord.id == record_id, DelayRecord.deleted_at.is_(None)).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delay record not found.")

    record.deleted_at = datetime.now(timezone.utc)
    db.commit()
    return None
