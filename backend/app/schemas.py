from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class RailwayLine(str, Enum):
    CENTRAL = "Central"
    WESTERN = "Western"
    HARBOUR = "Harbour"


class Direction(str, Enum):
    UP = "UP"
    DN = "DN"


class Priority(str, Enum):
    MINOR = "Minor"
    MAJOR = "Major"
    SEVERE = "Severe"


class DelayIncidentBase(BaseModel):
    line: RailwayLine
    direction: Direction
    station: str = Field(min_length=2, max_length=100)
    affected_stretch: str = Field(min_length=5, max_length=120)
    delay_minutes: int = Field(ge=0, le=180)
    priority: Priority
    announcement_text: str = Field(min_length=10, max_length=500)


class DelayIncidentCreate(DelayIncidentBase):
    created_at: datetime | None = None


class DelayIncidentRead(DelayIncidentBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class LineStatus(BaseModel):
    line: RailwayLine
    status: str
    avg_delay_minutes: float
    incident_count: int


class StatusResponse(BaseModel):
    updated_at: datetime
    lines: list[LineStatus]


class DelayStatsResponse(BaseModel):
    total_active_delays: int
    average_delay_minutes: float
    worst_affected_line: RailwayLine | None
    most_affected_stretch: str | None


class LineBreakdownResponse(BaseModel):
    line: RailwayLine
    total_incidents: int
    average_delay_minutes: float
    worst_stretch: str | None
    priorities: dict[str, int]
    directions: dict[str, int]
    recent_incidents: list[DelayIncidentRead]
