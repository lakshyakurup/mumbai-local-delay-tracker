from datetime import datetime
from sqlalchemy import DateTime, Float, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base


class DelayRecord(Base):
    __tablename__ = "delay_records"
    __table_args__ = (Index("ix_delay_records_line_recorded", "line", "recorded_at"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    line: Mapped[str] = mapped_column(String(20), index=True)
    station: Mapped[str] = mapped_column(String(100), index=True)
    direction: Mapped[str] = mapped_column(String(20), default="both")
    delay_minutes: Mapped[int] = mapped_column(Integer, default=0)
    severity: Mapped[str] = mapped_column(String(20), default="normal")
    source: Mapped[str] = mapped_column(String(120), default="manual")
    announcement: Mapped[str | None] = mapped_column(Text, nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)


class LineStatus(Base):
    __tablename__ = "line_statuses"

    id: Mapped[int] = mapped_column(primary_key=True)
    line: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(20), default="normal")
    average_delay_minutes: Mapped[float] = mapped_column(Float, default=0)
    active_incidents: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class StationMetric(Base):
    __tablename__ = "station_metrics"

    id: Mapped[int] = mapped_column(primary_key=True)
    line: Mapped[str] = mapped_column(String(20), index=True)
    station: Mapped[str] = mapped_column(String(100), index=True)
    average_delay_minutes: Mapped[float] = mapped_column(Float, default=0)
    trains_observed: Mapped[int] = mapped_column(Integer, default=0)
    reliability_percent: Mapped[float] = mapped_column(Float, default=100)
    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
