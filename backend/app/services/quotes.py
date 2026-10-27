"""Create and query quote requests."""

import secrets

from datetime import datetime, timezone

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.data.services import PRIVACY_VERSION
from app.models.quote import QuoteRequest, utcnow
from app.schemas.quotes import QuoteAdmin, QuoteCreate, QuotePage, Stats

_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def new_reference() -> str:
    body = "".join(secrets.choice(_ALPHABET) for _ in range(8))
    return f"RC-{body}"


def create_quote(db: Session, payload: QuoteCreate) -> str:
    now = datetime.now(timezone.utc)
    for _ in range(5):
        reference = new_reference()
        if db.scalar(select(QuoteRequest.id).where(QuoteRequest.reference == reference)):
            continue
        row = QuoteRequest(
            reference=reference,
            name=payload.name,
            email=payload.email,
            telephone=payload.telephone,
            company=payload.company,
            service=payload.service,
            property_type=payload.property_type,
            area_sqm=payload.area_sqm,
            preferred_date=payload.preferred_date,
            message=payload.message,
            privacy_version=PRIVACY_VERSION,
            privacy_accepted_at=now,
            status="neu",
            created_at=now,
            updated_at=now,
        )
        db.add(row)
        db.commit()
        return reference
    raise RuntimeError("Referenz konnte nicht erzeugt werden")


def to_admin(row: QuoteRequest) -> QuoteAdmin:
    return QuoteAdmin(
        reference=row.reference,
        name=row.name,
        email=row.email,
        telephone=row.telephone,
        company=row.company,
        service=row.service,
        property_type=row.property_type,
        area_sqm=row.area_sqm,
        preferred_date=row.preferred_date,
        message=row.message,
        privacy_version=row.privacy_version,
        status=row.status,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def list_quotes(
    db: Session, *, page: int, page_size: int, status: str | None, query: str | None
) -> QuotePage:
    filters = []
    if status:
        filters.append(QuoteRequest.status == status)
    if query:
        like = f"%{query.strip()}%"
        filters.append(or_(QuoteRequest.reference.ilike(like), QuoteRequest.name.ilike(like)))
    total = db.scalar(select(func.count()).select_from(QuoteRequest).where(*filters)) or 0
    rows = db.scalars(
        select(QuoteRequest)
        .where(*filters)
        .order_by(QuoteRequest.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    return QuotePage(items=[to_admin(row) for row in rows], total=total, page=page, page_size=page_size)


def get_quote(db: Session, reference: str) -> QuoteRequest | None:
    return db.scalar(select(QuoteRequest).where(QuoteRequest.reference == reference))


def set_status(db: Session, row: QuoteRequest, status: str) -> QuoteRequest:
    row.status = status
    row.updated_at = utcnow()
    db.commit()
    db.refresh(row)
    return row


def delete_quote(db: Session, row: QuoteRequest) -> None:
    db.delete(row)
    db.commit()


def stats(db: Session) -> Stats:
    rows = db.execute(select(QuoteRequest.status, func.count()).group_by(QuoteRequest.status)).all()
    counts = {status: count for status, count in rows}
    return Stats(
        total=sum(counts.values()),
        neu=counts.get("neu", 0),
        in_progress=counts.get("kontaktiert", 0) + counts.get("angebot_erstellt", 0),
        completed=counts.get("abgeschlossen", 0),
    )


def purge_older_than(db: Session, days: int) -> int:
    cutoff = datetime.now(timezone.utc).timestamp() - days * 86400
    cutoff_dt = datetime.fromtimestamp(cutoff, tz=timezone.utc)
    rows = db.scalars(select(QuoteRequest).where(QuoteRequest.created_at < cutoff_dt)).all()
    for row in rows:
        db.delete(row)
    db.commit()
    return len(rows)
