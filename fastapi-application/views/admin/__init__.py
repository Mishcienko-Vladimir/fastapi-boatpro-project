from fastapi import APIRouter

from core.config import settings
from .home import router as home_router
from .boats import router as boats_router


router = APIRouter(prefix=settings.view.admin)

router.include_router(home_router)
router.include_router(boats_router)
