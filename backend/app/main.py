"""FastAPI application for the RheinClean demo."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import api_router
from app.core.config import settings
from app.db.session import create_tables

MAX_BODY = 32 * 1024


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.database_url.startswith("sqlite:///./"):
        from pathlib import Path

        Path("data").mkdir(exist_ok=True)
    create_tables()
    yield


app = FastAPI(
    title="RheinClean API",
    version="0.1.0",
    description="Demo-API für die fiktive Website RheinClean Gebäudeservice.",
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url=None,
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "X-CSRF-Token"],
)
app.include_router(api_router, prefix="/api/v1")


@app.middleware("http")
async def limit_body(request: Request, call_next):
    length = request.headers.get("content-length")
    if length and length.isdigit() and int(length) > MAX_BODY:
        return JSONResponse(status_code=413, content={"detail": "Die Anfrage ist zu groß."})
    return await call_next(request)


@app.exception_handler(RequestValidationError)
async def validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    errors = [{"field": ".".join(str(part) for part in err["loc"] if part != "body"), "message": err["msg"]} for err in exc.errors()]
    return JSONResponse(status_code=422, content={"detail": "Die Eingaben sind ungültig.", "errors": errors})


