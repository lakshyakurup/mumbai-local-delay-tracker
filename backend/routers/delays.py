from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.database import DelayRecord, LineStatus, StationMetric
from ..schemas import DelayCreate, DelayRead, LineName, LineStatusRead, StationMetricRead
from ..services.scraper import severity_for_delay
from ..services.scraper import ScraperService
from ..config import get_settings

router = APIRouter(prefix="/api/v2", tags=["delays"])


@router.post("/scraper/run")
def run_scraper(authorization: str | None = Header(default=None), db: Session = Depends(get_db)):
    expected = get_settings().scraper_token
    if expected and authorization != f"Bearer {expected}":
        raise HTTPException(status_code=401, detail="Invalid scraper credentials")
    return {"persisted": ScraperService(db).run_once()}


@router.get("/delays", response_model=list[DelayRead])
def list_delays(db: Session = Depends(get_db), line: LineName | None = None, hours: int = Query(24, ge=1, le=168), limit: int = Query(100, ge=1, le=500)):
    query = select(DelayRecord).where(DelayRecord.recorded_at >= datetime.now(timezone.utc) - timedelta(hours=hours))
    if line:
        query = query.where(DelayRecord.line == line)
    return list(db.scalars(query.order_by(desc(DelayRecord.recorded_at)).limit(limit)).all())


@router.post("/delays", response_model=DelayRead, status_code=201)
def create_delay(payload: DelayCreate, db: Session = Depends(get_db)):
    record = DelayRecord(**payload.model_dump(), severity=severity_for_delay(payload.delay_minutes))
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/lines/status", response_model=list[LineStatusRead])
def line_status(db: Session = Depends(get_db)):
    return list(db.scalars(select(LineStatus).order_by(LineStatus.line)).all())


@router.get("/lines/{line}/stations", response_model=list[StationMetricRead])
def station_metrics(line: LineName, db: Session = Depends(get_db)):
    return list(db.scalars(select(StationMetric).where(StationMetric.line == line).order_by(StationMetric.average_delay_minutes.desc())).all())


@router.delete("/delays/{record_id}", status_code=204)
def delete_delay(record_id: int, db: Session = Depends(get_db)):
    record = db.get(DelayRecord, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Delay record not found")
    db.delete(record)
    db.commit()
