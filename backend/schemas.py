from pydantic import BaseModel, Field, conint
from typing import Optional, List, Literal, Dict
from datetime import datetime
import uuid

class LineStatusItem(BaseModel):
    line_id: str
    line_name: str
    status: Literal["ON_TIME", "DELAYED", "CRITICAL", "UNKNOWN"]
    avg_delay_minutes: int
    delay_percentage: int
    last_updated: datetime
    station_count: int
    delayed_stations: int

class LinesStatusResponse(BaseModel):
    lines: List[LineStatusItem]
    timestamp: datetime

class DelayRecordResponse(BaseModel):
    id: uuid.UUID
    line: str
    station: str
    delay_minutes: int
    direction: Optional[Literal["up", "down"]] = None
    severity: Literal["minor", "moderate", "severe"]
    source: Literal["scraper", "user", "api"]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DelaysListResponse(BaseModel):
    delays: List[DelayRecordResponse]
    count: int
    total_records: int
    page: int
    limit: int

class DelayCreateRequest(BaseModel):
    line: str = Field(..., example="central")
    station: str = Field(..., example="Dadar")
    delay_minutes: conint(ge=0, le=360) = Field(..., example=15)
    direction: Optional[Literal["up", "down"]] = None
    notes: Optional[str] = Field(None, max_length=200, example="Stuck at signal")

class DelayCreateResponse(BaseModel):
    id: uuid.UUID
    created_at: datetime
    status: str = "created"

class StationMetricItem(BaseModel):
    station_id: uuid.UUID
    name: str
    order: int
    avg_delay_minutes: float
    incidents_7d: int
    on_time_percentage: float
    last_delay: Optional[datetime] = None
    passenger_volume_estimate: Optional[int] = None

class LineStationsResponse(BaseModel):
    line: str
    stations: List[StationMetricItem]

class MostDelayedStation(BaseModel):
    name: str
    line: str
    avg_delay: float

class StatsSummary(BaseModel):
    avg_delay_minutes_all_lines: float
    peak_hour: str
    peak_hour_avg_delay: float
    total_delays_24h: int
    most_delayed_station: MostDelayedStation
    on_time_percentage: int
    measurement_period_hours: int

class StatsSummaryResponse(BaseModel):
    summary: StatsSummary
    timestamp: datetime

class LineBreakdownDetail(BaseModel):
    avg_delay: float
    count: int

class TrendItem(BaseModel):
    period: datetime
    avg_delay_minutes: float
    delay_count: int
    line_breakdown: Dict[str, LineBreakdownDetail]

class StatsTrendsResponse(BaseModel):
    trends: List[TrendItem]
    granularity: Literal["hourly", "daily", "weekly"]

class HealthResponse(BaseModel):
    status: str
    database: str
    timestamp: datetime

class ScraperRunRequest(BaseModel):
    token: str

class ScraperRunResponse(BaseModel):
    job_id: uuid.UUID
    status: str
    message: str
