from fastapi import APIRouter

from api.api_v1.routers import router as router_api_v1
from api.webhooks import webhooks_router
from core.config import settings


router = APIRouter(prefix=settings.api.prefix)
router.include_router(router_api_v1)
router.include_router(webhooks_router)
