from fastapi import APIRouter

from core.config import settings

from .catalog import router as catalog_router
from .boats import router as boats_router
from .outboard_motors import router as outboard_motors_router
from .trailers import router as trailers_router


router = APIRouter(prefix=settings.view.catalog)

router.include_router(catalog_router)
router.include_router(boats_router)
router.include_router(outboard_motors_router)
router.include_router(trailers_router)
