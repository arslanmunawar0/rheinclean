"""Protected enquiry management."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import current_admin, ensure_csrf, require_csrf
from app.core.limiter import enforce_limit
from app.core.security import clear_auth_cookies, set_csrf_cookie, set_session_cookie, verify_password
from app.data.services import STATUSES
from app.db.session import get_db
from app.models.admin import AdminUser
from app.schemas.auth import LoginRequest, SessionState
from app.schemas.quotes import QuoteAdmin, QuotePage, QuoteStatusUpdate, Stats
from app.services.quotes import delete_quote, get_quote, list_quotes, set_status, stats, to_admin
from app.core.security import new_csrf_token

router = APIRouter(prefix="/admin")


@router.get("/session", response_model=SessionState)
def session(request: Request, response: Response, db: Session = Depends(get_db)) -> SessionState:
    token = ensure_csrf(request, response)
    try:
        current_admin(request, db)
        authenticated = True
    except HTTPException:
        authenticated = False
    return SessionState(authenticated=authenticated, csrf_token=token)


@router.post("/login", response_model=SessionState)
def login(payload: LoginRequest, request: Request, response: Response, db: Session = Depends(get_db)) -> SessionState:
    enforce_limit(request, "login", limit=5, window_seconds=900)
    require_csrf(request)
    admin = db.scalar(select(AdminUser).where(AdminUser.email == payload.normalized_email()))
    if admin is None or not verify_password(payload.password, admin.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Anmeldung fehlgeschlagen")
    set_session_cookie(response, admin.id)
    token = new_csrf_token()
    set_csrf_cookie(response, token)
    return SessionState(authenticated=True, csrf_token=token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request, response: Response, _: AdminUser = Depends(current_admin)) -> Response:
    require_csrf(request)
    clear_auth_cookies(response)
    return response


@router.get("/stats", response_model=Stats)
def admin_stats(db: Session = Depends(get_db), _: AdminUser = Depends(current_admin)) -> Stats:
    return stats(db)


@router.get("/quote-requests", response_model=QuotePage)
def admin_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    status_filter: str | None = Query(None, alias="status"),
    q: str | None = Query(None, max_length=80),
    db: Session = Depends(get_db),
    _: AdminUser = Depends(current_admin),
) -> QuotePage:
    if status_filter is not None and status_filter not in STATUSES:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unbekannter Status")
    return list_quotes(db, page=page, page_size=page_size, status=status_filter, query=q)


@router.get("/quote-requests/{reference}", response_model=QuoteAdmin)
def admin_detail(
    reference: str, db: Session = Depends(get_db), _: AdminUser = Depends(current_admin)
) -> QuoteAdmin:
    row = get_quote(db, reference)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Anfrage nicht gefunden")
    return to_admin(row)


@router.patch("/quote-requests/{reference}", response_model=QuoteAdmin)
def admin_update(
    reference: str,
    payload: QuoteStatusUpdate,
    request: Request,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(current_admin),
) -> QuoteAdmin:
    require_csrf(request)
    row = get_quote(db, reference)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Anfrage nicht gefunden")
    return to_admin(set_status(db, row, payload.status))


@router.delete("/quote-requests/{reference}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete(
    reference: str,
    request: Request,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(current_admin),
) -> Response:
    require_csrf(request)
    row = get_quote(db, reference)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Anfrage nicht gefunden")
    delete_quote(db, row)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
