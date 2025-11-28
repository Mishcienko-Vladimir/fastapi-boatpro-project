from fastapi import APIRouter

from core.config import settings
from .home import router as home_router
from .boats import router as boats_router
from .outboard_motors import router as outboard_motors_router
from .trailers import router as trailers_router
from .users import router as users_router
from .categories import router as categories_router
from .orders import router as orders_router
from .pickup_points import router as pickup_points_router


router = APIRouter(prefix=settings.view.admin)

router.include_router(home_router)
router.include_router(boats_router)
router.include_router(outboard_motors_router)
router.include_router(trailers_router)
router.include_router(users_router)
router.include_router(categories_router)
router.include_router(orders_router)
router.include_router(pickup_points_router)
