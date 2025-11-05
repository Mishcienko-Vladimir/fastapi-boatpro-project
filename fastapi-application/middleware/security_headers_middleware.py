from fastapi import Request
from starlette.datastructures import MutableHeaders
from starlette.middleware.base import BaseHTTPMiddleware

from core.config import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware для установки безопасности HTTP-заголовков.
    """

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "no-referrer",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
        }

        # Добавляем HSTS только в продакшене (HTTPS)
        if (
            not settings.run.host == "127.0.0.1"
            and not settings.run.host == "localhost"
        ):
            headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        response_headers = MutableHeaders(headers=response.headers)
        for key, value in headers.items():
            if key not in response_headers:
                response_headers[key] = value

        return response
