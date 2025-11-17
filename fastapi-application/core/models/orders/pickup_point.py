from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .order import Order  # noqa


class PickupPoint(
    IntIdPkMixin,
    Base,
):
    """
    Таблица пункт самовывоза.

    Уникальность обеспечивается по полю name и id.
    """

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        comment="Название пункта",
    )
    address: Mapped[str] = mapped_column(
        Text,
        comment="Полный адрес",
    )
    work_hours: Mapped[str] = mapped_column(
        String(100),
        comment="Время работы. Пример: Пн-Пт, 9:00-19:00",
    )

    # Обратная связь
    orders: Mapped[list["Order"]] = relationship(back_populates="pickup_point")

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id}, "
            f"name={self.name!r}, "
            f"address={self.address!r}, "
            f"work_hours={self.work_hours!r})"
        )

    def __repr__(self):
        return str(self)
