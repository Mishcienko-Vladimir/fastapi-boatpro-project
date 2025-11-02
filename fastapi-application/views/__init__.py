from fastapi import APIRouter

from .admin import router as admin_router
from .home import router as home_router
from .page_missing import router as page_missing_router
from .limit_exceeded import router as limit_exceeded_router
from .favorites import router as favorites_router
from .search import router as search_router
from .products import router as catalog_router

from views.auth.verification import router as verification_router
from views.auth.reset_password import router as reset_password_router
from views.auth.change_password import router as change_password_router


router = APIRouter()

router.include_router(admin_router)
router.include_router(home_router)
router.include_router(page_missing_router)
router.include_router(limit_exceeded_router)
router.include_router(favorites_router)
router.include_router(search_router)
router.include_router(catalog_router)
router.include_router(verification_router)
router.include_router(reset_password_router)
router.include_router(change_password_router)
