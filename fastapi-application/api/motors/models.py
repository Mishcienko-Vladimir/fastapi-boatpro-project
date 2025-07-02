from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base, str_256, intpk


class OutboardMotor(Base):
    """Таблица подвесных лодочных моторов"""
    __tablename__ = "outboard_motors"

    id: Mapped[intpk]
    company_name: Mapped[str_256]
    engine_power: Mapped[int]
    price: Mapped[int]
    image_id: Mapped[int]
    weight: Mapped[int]
    description: Mapped[str] = mapped_column(Text)
