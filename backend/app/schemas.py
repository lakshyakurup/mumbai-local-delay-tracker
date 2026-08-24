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


class DelayIncidentBase(BaseModel):
    line: RailwayLine
    direction: Direction
    station: str = Field(min_length=2, max_length=100)
    delay_minutes: int = Field(ge=0, le=180)
    announcement_text: str = Field(min_length=10, max_length=500)


class DelayIncidentCreate(DelayIncidentBase):
    pass


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
