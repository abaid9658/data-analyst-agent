"""
Request logging middleware for API metrics and request tracking
"""
import logging
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log duration, path, and status of every incoming HTTP request."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        logger.info(
            "Method: %s Path: %s Status: %d Duration: %.4fs",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )
        return response
