from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db_helper import db_helper


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Зависимость для получения асинхронной сессии SQLAlchemy.
    Используется в routers через Depends(get_db_session).
    """
    async for session in db_helper.session_getter():
        yield session
