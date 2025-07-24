from sqlalchemy import Text, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base
from core.models.mixins import IntIdPkMixin, CreatedAtMixin, UpdatedAtMixin


class Trailer(
    IntIdPkMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
    Base,
):
    """
    Таблица прицепов.

    Уникальность обеспечивается по полю model_name.
    """

    model_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        comment="Модель прицепа",
    )
    full_mass: Mapped[int] = mapped_column(
        SmallInteger,
        default=0,
        comment="Общая масса прицепа в кг",
    )
    load_capacity: Mapped[int] = mapped_column(
        SmallInteger,
        default=0,
        comment="Грузоподъемность в кг",
    )
    trailer_length: Mapped[int] = mapped_column(
        SmallInteger,
        default=0,
        comment="Длина прицепа в мм",
    )
    max_ship_length: Mapped[int] = mapped_column(
        SmallInteger,
        default=0,
        comment="Максимальная длина перевозимого судна в мм",
    )
    description: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
        comment="Описание прицепа",
    )
    price: Mapped[int] = mapped_column(
        default=0,
        comment="Цена прицепа в рублях",
    )
    image_id: Mapped[list[int]] = mapped_column(
        comment="ID изображения прицепа",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"model_name={self.model_name!r}, "
            f"full_mass={self.full_mass!r}, "
            f"load_capacity={self.load_capacity!r}, "
            f"trailer_length={self.trailer_length!r}, "
            f"max_ship_length={self.max_ship_length!r}, "
            f"description={self.description!r}, "
            f"price={self.price!r}, "
            f"image_id={self.image_id!r})"
        )

    def __repr__(self):
        return str(self)
