from fastapi_users.authentication import (
    BearerTransport,
    CookieTransport,
)

from core.config import settings


bearer_transport = BearerTransport(
    tokenUrl=settings.api.bearer_token_url,
)

cookie_transport = CookieTransport(
    cookie_max_age=settings.api.cookie_max_age,
    cookie_secure=settings.api.cookie_secure,
)
