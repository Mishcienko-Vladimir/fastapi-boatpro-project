from sqlalchemy import UniqueConstraint, Text, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base
from core.models.mixins import IntIdPkMixin, CreatedAtMixin, UpdatedAtMixin


class OutboardMotor(
    IntIdPkMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
    Base,
):
    """
    Таблица подвесных лодочных моторов.

    Уникальность модели обеспечивается по комбинации:
    - company_name
    - engine_power
    """

    __table_args__ = (
        UniqueConstraint("company_name", "engine_power", name="uq_company_engine"),
    )

    company_name: Mapped[str] = mapped_column(
        String(100),
        comment="Название производителя",
    )
    engine_power: Mapped[int] = mapped_column(
        SmallInteger,
        default=0,
        comment="Мощность двигателя в л.с.",
    )
    price: Mapped[int] = mapped_column(
        default=0,
        comment="Цена мотора в рублях",
    )
    weight: Mapped[int] = mapped_column(
        SmallInteger,
        default=0,
        comment="Вес мотора в кг",
    )
    description: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
        comment="Описание мотора",
    )
    image_id: Mapped[int] = mapped_column(
        default=0,
        comment="ID изображения мотора",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"company_name={self.company_name!r}, "
            f"engine_power={self.engine_power!r}, "
            f"price={self.price!r}, "
            f"weight={self.weight!r}, "
            f"description={self.description!r}, "
            f"image_id={self.image_id!r})"
        )

    def __repr__(self):
        return str(self)
