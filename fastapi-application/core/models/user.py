from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.types.user_id import UserIdType
from core.models.base import Base
from core.models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession  # noqa


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[UserIdType]):
    """Таблица пользователей"""

    first_name: Mapped[str] = mapped_column(
        String(50),
        comment="Имя пользователя",
    )

    # Получение данных из БД
    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
