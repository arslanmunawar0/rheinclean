"""Public health, services and quote submission."""

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.core.limiter import enforce_limit
from app.data.services import SERVICES
from app.db.session import get_db
from app.schemas.quotes import QuoteAccepted, QuoteCreate
from app.services.quotes import create_quote

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/services")
def services() -> dict:
    return {"items": list(SERVICES)}


@router.post("/quote-requests", response_model=QuoteAccepted, status_code=status.HTTP_201_CREATED)
def submit_quote(payload: QuoteCreate, request: Request, db: Session = Depends(get_db)) -> QuoteAccepted:
    enforce_limit(request, "quote", limit=5, window_seconds=600)
    reference = create_quote(db, payload)
    return QuoteAccepted(
        reference=reference,
        message="Ihre Anfrage ist eingegangen. Das ist noch kein verbindlicher Auftrag.",
    )
