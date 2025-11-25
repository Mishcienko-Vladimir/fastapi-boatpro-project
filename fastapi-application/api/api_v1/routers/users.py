from typing import Annotated, TYPE_CHECKING
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from api.api_v1.dependencies.authentication import get_users_db

from core.dependencies.fastapi_users import fastapi_users
from core.config import settings
from core.schemas.user import UserRead, UserUpdate

from utils.key_builder import users_list_key_builder

if TYPE_CHECKING:
    from core.models.user import SQLAlchemyUserDatabase  # noqa


router = APIRouter(prefix=settings.api.v1.users, tags=["Users 👥"])


@router.get(
    "",
    response_model=list[UserRead],
)
@cache(
    expire=60,
    key_builder=users_list_key_builder,
    namespace=settings.cache.namespace.users_list,
)
async def get_users_list(
    users_db: Annotated[
        "SQLAlchemyUserDatabase",
        Depends(get_users_db),
    ],
) -> list[UserRead]:
    users = await users_db.get_users()
    return [UserRead.model_validate(user) for user in users]


# /me
# /{id}
router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)
