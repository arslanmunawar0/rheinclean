"""Public and admin schemas. Public responses never include customer details."""

from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.data.services import PROPERTY_TYPES, SERVICE_IDS, STATUSES


class QuoteCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    telephone: str | None = Field(default=None, max_length=30)
    company: str | None = Field(default=None, max_length=80)
    service: str
    property_type: str | None = None
    area_sqm: int | None = Field(default=None, ge=1, le=100_000)
    preferred_date: date | None = None
    message: str = Field(min_length=10, max_length=2000)
    privacy_accepted: bool

    @field_validator("name", "telephone", "company", "message")
    @classmethod
    def strip_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = " ".join(value.split())
        return cleaned or None

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()

    @field_validator("service")
    @classmethod
    def known_service(cls, value: str) -> str:
        if value not in SERVICE_IDS:
            raise ValueError("Unbekannte Leistung")
        return value

    @field_validator("property_type")
    @classmethod
    def known_property(cls, value: str | None) -> str | None:
        if value is None or value == "":
            return None
        if value not in PROPERTY_TYPES:
            raise ValueError("Unbekannte Objektart")
        return value

    @field_validator("privacy_accepted")
    @classmethod
    def must_accept(cls, value: bool) -> bool:
        if not value:
            raise ValueError("Bitte bestätigen Sie den Hinweis zum Datenschutz")
        return value

    @field_validator("preferred_date")
    @classmethod
    def not_in_the_past(cls, value: date | None) -> date | None:
        if value is not None and value < date.today():
            raise ValueError("Das Wunschdatum liegt in der Vergangenheit")
        return value


class QuoteAccepted(BaseModel):
    reference: str
    message: str


class QuoteAdmin(BaseModel):
    reference: str
    name: str
    email: EmailStr
    telephone: str | None
    company: str | None
    service: str
    property_type: str | None
    area_sqm: int | None
    preferred_date: date | None
    message: str
    privacy_version: str
    status: str
    created_at: datetime
    updated_at: datetime


class QuotePage(BaseModel):
    items: list[QuoteAdmin]
    total: int
    page: int
    page_size: int


class QuoteStatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def known_status(cls, value: str) -> str:
        if value not in STATUSES:
            raise ValueError("Unbekannter Status")
        return value


class Stats(BaseModel):
    total: int
    neu: int
    in_progress: int
    completed: int
