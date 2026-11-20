"""FastAPI application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.db import Base, engine
from app.schemas import HealthResponse


def create_app() -> FastAPI:
    """Create and configure the SiteCheck application."""

    app = FastAPI(title="SiteCheck", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[],
        allow_credentials=False,
        allow_methods=["GET", "POST", "PATCH", "DELETE"],
        allow_headers=["X-API-Key"],
    )

    @app.middleware("http")
    async def security_headers(request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Frame-Options"] = "DENY"
        return response

    @app.on_event("startup")
    async def startup() -> None:
        Base.metadata.create_all(bind=engine)

    @app.get("/healthz", response_model=HealthResponse)
    async def healthz() -> JSONResponse:
        return JSONResponse({"status": "ok"})

    return app


app = create_app()
