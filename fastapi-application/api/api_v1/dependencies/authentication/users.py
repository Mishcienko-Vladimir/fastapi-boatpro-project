from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from core.dependencies import get_db_session
from core.models import User

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession  # noqa


async def get_users_db(
    session: Annotated[
        "AsyncSession",
        Depends(get_db_session),
    ],
):
    """
    Зависимость для получения базы данных пользователей.

    Возвращает адаптер для работы с моделью User через SQLAlchemy.
    Используется UserManager для выполнения CRUD операций.

    Args:
        session (AsyncSession): Асинхронная сессия

    Yields:
        SQLAlchemyUserDatabase: Адаптер для User
    """
    yield User.get_db(session=session)
