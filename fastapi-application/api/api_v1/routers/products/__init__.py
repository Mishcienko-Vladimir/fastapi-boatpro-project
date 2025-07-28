from fastapi import APIRouter

from core.config import settings

from .boats import router as boats_router
from .trailers import router as trailers_router
from .motors import router as motors_router
from .product_types import router as product_types_router


router = APIRouter(prefix=settings.api.v1.products)

router.include_router(boats_router)
router.include_router(trailers_router)
router.include_router(motors_router)
router.include_router(product_types_router)
