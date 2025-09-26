from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.types.user_id import UserIdType
from core.models.base import Base
from core.models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession  # noqa
    from core.models.favorite import Favorite  # noqa


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
