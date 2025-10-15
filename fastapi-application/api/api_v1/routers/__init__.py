from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from core.config import settings
from .users import router as users_router
from .auth import router as auth_router
from .messages import router as messages_router
from .products import router as products_router
from .favorites import router as favorites_router
from .search import router as search_router


http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(prefix=settings.api.v1.prefix, dependencies=[Depends(http_bearer)])

router.include_router(users_router)
router.include_router(auth_router)
router.include_router(messages_router)
router.include_router(products_router)
router.include_router(favorites_router)
router.include_router(search_router)
