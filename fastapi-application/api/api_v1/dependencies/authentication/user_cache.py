from typing import Optional
from fastapi import Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models.db_helper import db_helper
from core.schemas.user import UserRead

from core.repositories.user_manager_crud import UserManagerCrud
from core.repositories.authentication.fastapi_users import optional_user_id

from utils.key_builder import user_key_builder


@cache(
    expire=60,
    key_builder=user_key_builder,
    namespace=settings.cache.namespace.user,
)
async def get_cached_user(
    user_id: Optional[int] = Depends(optional_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Optional[UserRead]:
    """
    Кэшированная версия optional_user, позволяет уменьшить количество запросов к БД.
    """
    if user_id is None:
        return None

    user = await UserManagerCrud(session=session).get_user_by_id(user_id=user_id)

    if user is None:
        return None

    return UserRead.model_validate(user)
