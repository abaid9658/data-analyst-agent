"""
AI Data Analyst Agent — FastAPI Application Entry Point
"""
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.config import settings
from app.database.base import init_db
from app.database.redis import init_redis, close_redis
from app.middleware.logging import RequestLoggingMiddleware
from app.middleware.rate_limit import setup_rate_limiter
from app.routes import (
    auth,
    upload,
    database,
    chat,
    query,
    chart,
    report,
    dashboard,
    export,
    history,
    settings as settings_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown."""
    # Startup
    await init_db()
    await init_redis()
    yield
    # Shutdown
    await close_redis()


app = FastAPI(
    title=settings.APP_NAME,
    description="Production-ready AI Data Analyst Agent API",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# ─── Middleware ────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestLoggingMiddleware)

setup_rate_limiter(app)

# ─── Routes ───────────────────────────────────────────────────────────────────

API_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=f"{API_PREFIX}/auth", tags=["Authentication"])
app.include_router(upload.router, prefix=f"{API_PREFIX}/upload", tags=["Upload"])
app.include_router(database.router, prefix=f"{API_PREFIX}/database", tags=["Database"])
app.include_router(chat.router, prefix=f"{API_PREFIX}/chat", tags=["Chat"])
app.include_router(query.router, prefix=f"{API_PREFIX}/query", tags=["Query"])
app.include_router(chart.router, prefix=f"{API_PREFIX}/chart", tags=["Chart"])
app.include_router(report.router, prefix=f"{API_PREFIX}/report", tags=["Report"])
app.include_router(dashboard.router, prefix=f"{API_PREFIX}/dashboard", tags=["Dashboard"])
app.include_router(export.router, prefix=f"{API_PREFIX}/export", tags=["Export"])
app.include_router(history.router, prefix=f"{API_PREFIX}/history", tags=["History"])
app.include_router(settings_router.router, prefix=f"{API_PREFIX}/settings", tags=["Settings"])


# ─── Health Check ─────────────────────────────────────────────────────────────

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
