from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class DelayIncident(Base):
    __tablename__ = "delay_incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    line: Mapped[str] = mapped_column(String(20), index=True)
    direction: Mapped[str] = mapped_column(String(2), index=True)
    station: Mapped[str] = mapped_column(String(100), index=True)
    delay_minutes: Mapped[int] = mapped_column(Integer)
    announcement_text: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )
