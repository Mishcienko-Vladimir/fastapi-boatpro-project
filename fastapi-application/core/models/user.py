from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTable

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable):
    """Таблица пользователей"""
    pass
