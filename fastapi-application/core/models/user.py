from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase as SQLAlchemyUserDatabaseGeneric,
)

from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.types.user_id import UserIdType
from core.models.base import Base
from core.models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession  # noqa
    from core.models.favorite import Favorite  # noqa


class SQLAlchemyUserDatabase(SQLAlchemyUserDatabaseGeneric):
    """
    Добавление новых методов в SQLAlchemyUserDatabase, для работы с пользователями.

    :methods:
        - get_users() - возвращает список пользователей.
    """

    async def get_users(self) -> list["User"]:
        statement = select(User).order_by(User.id)
        results = await self.session.scalars(statement)
        return list(results.all())


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[UserIdType]):
    """Таблица пользователей"""

    first_name: Mapped[str] = mapped_column(
        String(50),
        comment="Имя пользователя",
    )

    # Обратная связь с избранным
    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="user",
    )

    # Получение данных из БД
    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
