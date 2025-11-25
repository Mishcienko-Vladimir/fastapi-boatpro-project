from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from fastapi_users.authentication.strategy.db import DatabaseStrategy

from .access_tokens import get_access_token_db
from core.config import settings

if TYPE_CHECKING:
    from core.models import AccessToken  # noqa
    from fastapi_users.authentication.strategy.db import AccessTokenDatabase  # noqa


def get_database_strategy(
    access_token_db: Annotated[
        "AccessTokenDatabase[AccessToken]",
        Depends(get_access_token_db),
    ],
) -> DatabaseStrategy:
    """
    Зависимость для получения стратегии аутентификации.

    Использует хранение токенов в базе данных. Время жизни токена
    берётся из настроек. Подходит для веб-приложений с куками.

    Args:
        access_token_db (AccessTokenDatabase): База данных токенов

    Returns:
        DatabaseStrategy: Стратегия аутентификации
    """
    return DatabaseStrategy(
        database=access_token_db,
        lifetime_seconds=settings.access_token.lifetime_seconds,
    )
