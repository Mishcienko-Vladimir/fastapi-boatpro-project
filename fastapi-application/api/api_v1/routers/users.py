import hashlib

from typing import (
    Annotated,
    Any,
    Callable,
    Dict,
    Optional,
    Tuple,
)

from fastapi import APIRouter, Depends, Response, Request
from fastapi_cache.decorator import cache

from api.api_v1.dependencies.authentication import get_users_db
from core.repositories.authentication.fastapi_users import fastapi_users

from core.config import settings
from core.models.user import SQLAlchemyUserDatabase
from core.schemas.user import UserRead, UserUpdate


router = APIRouter(prefix=settings.api.v1.users, tags=["Users"])


def users_list_key_builder(
    func: Callable[..., Any],
    namespace: str,
    *,
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    """
    Функция для построения ключа кэша для списка пользователей.
    """
    exclude_types = (SQLAlchemyUserDatabase,)
    cache_kw = {}
    for name, value in kwargs.items():
        if isinstance(value, exclude_types):
            continue
        cache_kw[name] = value

    cache_key = hashlib.md5(  # noqa: S324
        f"{func.__module__}:{func.__name__}:{args}:{cache_kw}".encode()
    ).hexdigest()
    return f"{namespace}:{cache_key}"


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
