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

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"company_name={self.company_name!r}, "
            f"engine_power={self.engine_power!r}, "
            f"price={self.price!r}, "
            f"image_id={self.image_id!r}, "
            f"weight={self.weight!r}, "
            f"description={self.description!r})"
        )

    def __repr__(self):
        return str(self)
