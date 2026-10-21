import uuid
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Text, ForeignKey, Index, func
from sqlalchemy.dialects.postgresql import UUID
from backend.database import Base

class Line(Base):
    __tablename__ = "lines"

    id = Column(String, primary_key=True) # 'central', 'western', 'harbour'
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Station(Base):
    __tablename__ = "stations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    line_id = Column(String, ForeignKey("lines.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(150), nullable=False)
    display_order = Column(Integer)
    lat = Column(Numeric(10, 6))
    lng = Column(Numeric(10, 6))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("uq_line_station", "line_id", "name", unique=True),
    )

class DelayRecord(Base):
    __tablename__ = "delay_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    line_id = Column(String, ForeignKey("lines.id", ondelete="CASCADE"), nullable=False)
    station_id = Column(UUID(as_uuid=True), ForeignKey("stations.id", ondelete="SET NULL"))
    station_name = Column(String(150))
    delay_minutes = Column(Integer, nullable=False)
    direction = Column(String(10)) # 'up', 'down', NULL
    severity = Column(String(20)) # 'minor', 'moderate', 'severe'
    source = Column(String(20)) # 'scraper', 'user', 'api'
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("idx_delay_records_line_created", "line_id", "created_at", postgresql_using="btree"),
        Index("idx_delay_records_station_created", "station_name", "created_at", postgresql_using="btree"),
        Index("idx_delay_records_created", "created_at", postgresql_using="btree"),
    )

class LineStatusSnapshot(Base):
    __tablename__ = "line_status_snapshots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    line_id = Column(String, ForeignKey("lines.id"), nullable=False)
    avg_delay_minutes = Column(Integer)
    delayed_count = Column(Integer)
    total_incidents = Column(Integer)
    status = Column(String(50))
    snapshot_at = Column(DateTime(timezone=True), server_default=func.now())
