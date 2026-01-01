import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import get_jsonl_logger, log_event

logger = get_jsonl_logger("app")


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        start = time.time()

    
        request.state.request_id = request_id

        try:
            response: Response = await call_next(request)
            return response
        finally:
            latency_ms = int((time.time() - start) * 1000)

            # log request-level
            log_event(
                logger,
                {
                    "event": "http_request",
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": getattr(response, "status_code", None),
                    "latency_ms": latency_ms,
                },
            )
