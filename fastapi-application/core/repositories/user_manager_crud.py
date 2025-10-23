from typing import Sequence, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User


class UserManagerCrud:
    """
    Помощник для работы с пользователями.

    :session: - сессия для работы с БД.

    :methods:
        - get_all_users - получает всех пользователей.
        - get_user_by_id - получает пользователя по id.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_users(self) -> Sequence[User]:
        """
        Получает всех пользователей.

        :return: - список всех пользователей.
        """

        stmt = select(User).order_by(User.id)
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        Получает пользователя по id.

        :param user_id: - id пользователя.
        :return: - пользователь или None.
        """
        return await self.session.get(User, user_id)

    async def delete_user(self, user_id: int) -> Optional[User]:
        """
        Удаляет пользователя по ID.

        :param user_id: ID пользователя.
        :return: Удалённый объект User или None, если пользователь не найден.
        """
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        await self.session.delete(user)
        await self.session.commit()
        return user
