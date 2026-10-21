import logging
import httpx
from typing import List, Dict, Any, Union
from datetime import datetime, timezone
from backend.config import settings
from backend.database import SessionLocal
from backend.models.database import DelayRecord, Line, Station

logger = logging.getLogger(__name__)

class ScraperService:
    @staticmethod
    def fetch_data() -> Union[Dict[str, Any], str, None]:
        headers = {"User-Agent": "MumbaiLocalTrackerScraper/2.0"}
        for attempt in range(1, 4):
            try:
                with httpx.Client(timeout=10.0) as client:
                    response = client.get(settings.scraper_source_url, headers=headers)
                    response.raise_for_status()
                    logger.info(f"Successfully fetched scraper feed on attempt {attempt}")
                    try:
                        return response.json()
                    except Exception:
                        return response.text
            except Exception as e:
                logger.warning(f"Fetch attempt {attempt} failed: {e}")
        logger.error("All 3 fetch attempts failed for scraper feed.")
        return None

    @staticmethod
    def classify_severity(delay_minutes: int) -> str:
        if delay_minutes <= 5:
            return "minor"
        elif delay_minutes <= 14:
            return "moderate"
        else:
            return "severe"

    @classmethod
    def parse_delays(cls, raw_feed: Union[Dict[str, Any], str]) -> List[Dict[str, Any]]:
        parsed_records = []
        if isinstance(raw_feed, dict):
            items = raw_feed.get("delays", [])
            for item in items:
                line_id = item.get("line_id") or item.get("line")
                station_name = item.get("station_name") or item.get("station")
                delay_mins = item.get("delay_minutes")
                
                if not line_id or not station_name or delay_mins is None:
                    continue
                
                parsed_records.append({
                    "line_id": str(line_id).lower().strip(),
                    "station_name": str(station_name).strip(),
                    "delay_minutes": int(delay_mins),
                    "direction": item.get("direction"),
                    "source": "scraper",
                    "notes": item.get("notes")
                })
        return parsed_records

    @classmethod
    def persist_delays(cls, records: List[Dict[str, Any]]) -> int:
        if not records:
            return 0
            
        db = SessionLocal()
        persisted_count = 0
        try:
            for rec in records:
                line_id = rec["line_id"]
                station_name = rec["station_name"]
                delay_minutes = rec["delay_minutes"]
                
                line_obj = db.query(Line).filter(Line.id == line_id).first()
                if not line_obj:
                    continue
                    
                station_obj = db.query(Station).filter(Station.line_id == line_id, Station.name.ilike(station_name)).first()
                station_id = station_obj.id if station_obj else None
                
                severity = cls.classify_severity(delay_minutes)
                
                five_mins_ago = datetime.now(timezone.utc) - timedelta(minutes=5)
                existing = db.query(DelayRecord).filter(
                    DelayRecord.line_id == line_id,
                    DelayRecord.station_name.ilike(station_name),
                    DelayRecord.created_at >= five_mins_ago,
                    DelayRecord.deleted_at.is_(None)
                ).first()
                
                if existing:
                    existing.delay_minutes = delay_minutes
                    existing.severity = severity
                    existing.updated_at = datetime.now(timezone.utc)
                else:
                    new_rec = DelayRecord(
                        line_id=line_id,
                        station_id=station_id,
                        station_name=station_obj.name if station_obj else station_name,
                        delay_minutes=delay_minutes,
                        direction=rec.get("direction"),
                        severity=severity,
                        source="scraper",
                        notes=rec.get("notes")
                    )
                    db.add(new_rec)
                persisted_count += 1
            db.commit()
            logger.info(f"Successfully persisted {persisted_count} records via scraper.")
            return persisted_count
        except Exception as e:
            db.rollback()
            logger.error(f"Database error during persistence: {e}")
            raise e
        finally:
            db.close()

    @classmethod
    def run(cls):
        logger.info("Executing scheduled scraper run...")
        raw = cls.fetch_data()
        if not raw:
            return
        parsed = cls.parse_delays(raw)
        cls.persist_delays(parsed)
