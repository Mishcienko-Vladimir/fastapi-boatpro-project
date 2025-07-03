from pydantic import EmailStr
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base, str_256, intpk


class User(Base):
    """Таблица пользователей"""
    __tablename__ = 'users'

    id: Mapped[intpk]
    email: EmailStr = mapped_column(unique=True)
    first_name: Mapped[str_256]
    last_name: Mapped[str_256]