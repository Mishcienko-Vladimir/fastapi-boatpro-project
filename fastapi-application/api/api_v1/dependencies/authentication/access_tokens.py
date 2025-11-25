from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from core.dependencies import get_db_session
from core.models import AccessToken

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession  # noqa


async def get_access_token_db(
    session: Annotated["AsyncSession", Depends(get_db_session)],
):
    """
    Зависимость для получения базы данных токенов доступа.

    Возвращает адаптер для работы с моделью AccessToken через SQLAlchemy.
    Используется стратегией аутентификации для хранения и проверки
    токенов в базе данных (вместо JWT).

    Подходит для сценариев, где нужно:
    - Управлять сроком жизни токенов
    - Принудительно удалять сессии
    - Хранить метаданные токена

    Args:
        session (AsyncSession): Асинхронная сессия для работы с БД

    Yields:
        AccessTokenDatabase: Адаптер для модели AccessToken
    """
    yield AccessToken.get_db(
        session=session,
    )
