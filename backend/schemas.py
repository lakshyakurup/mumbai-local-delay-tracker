from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

LineName = Literal["central", "western", "harbour"]
Severity = Literal["normal", "minor", "major", "severe"]


class DelayCreate(BaseModel):
    line: LineName
    station: str = Field(min_length=2, max_length=100)
    direction: str = Field(default="both", max_length=20)
    delay_minutes: int = Field(ge=0, le=240)
    announcement: str | None = Field(default=None, max_length=500)
    source: str = Field(default="api", max_length=120)


class DelayRead(DelayCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    severity: Severity
    recorded_at: datetime


class LineStatusRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    line: LineName
    status: Severity
    average_delay_minutes: float
    active_incidents: int
    updated_at: datetime


class StationMetricRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    line: LineName
    station: str
    average_delay_minutes: float
    trains_observed: int
    reliability_percent: float
    measured_at: datetime


class StatsRead(BaseModel):
    window_hours: int
    total_records: int
    average_delay_minutes: float
    peak_hour: int | None
    by_line: dict[str, float]
