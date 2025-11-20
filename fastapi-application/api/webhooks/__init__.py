# Схема, что отправляет этот сайт на сторонний
from fastapi import APIRouter

from core.config import settings
from .user import router as user_router
from .yookassa import router as yookassa_router


webhooks_router = APIRouter(prefix=settings.api.v1.webhooks)
webhooks_router.include_router(user_router)
webhooks_router.include_router(yookassa_router)
