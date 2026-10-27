"""Stored quote requests. Personal data stays in this table, never in logs."""

from datetime import date, datetime, timezone

from sqlalchemy import CheckConstraint, Date, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.data.services import STATUSES
from app.db.session import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class QuoteRequest(Base):
    __tablename__ = "quote_requests"
    __table_args__ = (CheckConstraint(f"status IN {STATUSES}", name="ck_quote_status"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reference: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(120))
    telephone: Mapped[str | None] = mapped_column(String(30))
    company: Mapped[str | None] = mapped_column(String(80))
    service: Mapped[str] = mapped_column(String(40), index=True)
    property_type: Mapped[str | None] = mapped_column(String(40))
    area_sqm: Mapped[int | None] = mapped_column(Integer)
    preferred_date: Mapped[date | None] = mapped_column(Date)
    message: Mapped[str] = mapped_column(String(2000))
    privacy_version: Mapped[str] = mapped_column(String(20))
    privacy_accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(32), default="neu", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
