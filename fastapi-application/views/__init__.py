from fastapi import APIRouter

from .home import router as home_router
from .verification import router as verification_router
from .reset_password import router as reset_password_router
from .change_password import router as change_password_router
from .page_missing import router as page_missing_router


router = APIRouter()

router.include_router(home_router)
router.include_router(verification_router)
router.include_router(reset_password_router)
router.include_router(change_password_router)
router.include_router(page_missing_router)
