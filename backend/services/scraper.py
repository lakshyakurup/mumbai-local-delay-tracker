from dataclasses import dataclass
from datetime import datetime, timezone
import logging
import re
from typing import Any
import requests
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..config import get_settings
from ..models.database import DelayRecord, LineStatus

logger = logging.getLogger(__name__)
LINES = ("central", "western", "harbour")


@dataclass(frozen=True)
class ParsedUpdate:
    line: str
    station: str
    delay_minutes: int
    direction: str = "both"
    announcement: str | None = None


def severity_for_delay(delay_minutes: int) -> str:
    if delay_minutes <= 3:
        return "normal"
    if delay_minutes <= 10:
        return "minor"
    if delay_minutes <= 20:
        return "major"
    return "severe"


def parse_status_payload(payload: dict[str, Any]) -> list[ParsedUpdate]:
    updates: list[ParsedUpdate] = []
    for item in payload.get("updates", []):
        line = str(item.get("line", "")).strip().lower()
        station = str(item.get("station", "")).strip()
        if line not in LINES or not station:
            continue
        try:
            delay = max(0, int(item.get("delay_minutes", 0)))
        except (TypeError, ValueError):
            continue
        updates.append(ParsedUpdate(line, station, delay, str(item.get("direction", "both")), item.get("announcement")))
    return updates


def parse_status_text(text: str) -> list[ParsedUpdate]:
    pattern = re.compile(r"(?P<line>central|western|harbour)\s*[:|-]\s*(?P<station>[A-Za-z ]+)\s+(?P<delay>\d+)\s*min", re.I)
    return [ParsedUpdate(m.group("line").lower(), m.group("station").strip(), int(m.group("delay"))) for m in pattern.finditer(text)]


class ScraperService:
    def __init__(self, session: Session, source_url: str | None = None) -> None:
        self.session = session
        self.source_url = source_url or get_settings().scraper_source_url

    def fetch(self) -> list[ParsedUpdate]:
        response = requests.get(self.source_url, timeout=get_settings().scraper_timeout_seconds, headers={"User-Agent": "MumbaiDelayTracker/2.0"})
        response.raise_for_status()
        try:
            return parse_status_payload(response.json())
        except ValueError:
            return parse_status_text(response.text)

    def persist(self, updates: list[ParsedUpdate], source: str = "live-scraper") -> int:
        now = datetime.now(timezone.utc)
        for update in updates:
            self.session.add(DelayRecord(line=update.line, station=update.station, direction=update.direction, delay_minutes=update.delay_minutes, severity=severity_for_delay(update.delay_minutes), source=source, announcement=update.announcement, recorded_at=now))
        self.session.commit()
        self.refresh_line_statuses()
        return len(updates)

    def refresh_line_statuses(self) -> None:
        for line in LINES:
            records = self.session.scalars(select(DelayRecord).where(DelayRecord.line == line).order_by(DelayRecord.recorded_at.desc()).limit(50)).all()
            average = round(sum(item.delay_minutes for item in records) / len(records), 2) if records else 0
            status = severity_for_delay(round(average))
            current = self.session.scalar(select(LineStatus).where(LineStatus.line == line))
            if current is None:
                current = LineStatus(line=line)
                self.session.add(current)
            current.average_delay_minutes = average
            current.active_incidents = sum(item.delay_minutes > 0 for item in records)
            current.status = status
        self.session.commit()

    def run_once(self) -> int:
        try:
            return self.persist(self.fetch())
        except requests.RequestException:
            logger.exception("Live status fetch failed")
            return 0
