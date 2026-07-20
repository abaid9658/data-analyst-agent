"""
Audit Logging Middleware — writes AuditLog records for all state-changing requests
"""
import logging
import time
import uuid

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.database.base import async_session_maker
from app.models.audit_log import AuditLog

logger = logging.getLogger(__name__)

# Only audit state-changing HTTP methods
AUDITED_METHODS = {"POST", "PUT", "PATCH", "DELETE"}

# Skip noisy paths
SKIP_PATHS = {"/health", "/docs", "/redoc", "/openapi.json"}


class AuditMiddleware(BaseHTTPMiddleware):
    """Middleware that persists an AuditLog record for every non-read API call."""

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.method not in AUDITED_METHODS:
            return await call_next(request)

        path = request.url.path
        if any(path.startswith(s) for s in SKIP_PATHS):
            return await call_next(request)

        start_time = time.time()
        response = await call_next(request)
        duration_ms = int((time.time() - start_time) * 1000)

        # Extract user_id from request state (set by auth middleware)
        user_id: uuid.UUID | None = getattr(request.state, "user_id", None)
        status = "success" if response.status_code < 400 else "failure"

        # Non-blocking background audit write
        try:
            async with async_session_maker() as db:
                log = AuditLog(
                    user_id=user_id,
                    action=f"{request.method} {path}",
                    ip_address=request.client.host if request.client else None,
                    user_agent=request.headers.get("user-agent"),
                    request_id=request.headers.get("x-request-id"),
                    status=status,
                    details={"duration_ms": duration_ms, "status_code": response.status_code},
                )
                db.add(log)
                await db.commit()
        except Exception as e:
            logger.warning("Audit log write failed (non-fatal): %s", e)

        return response
