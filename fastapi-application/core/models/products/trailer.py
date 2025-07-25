from sqlalchemy import Text, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from core.models.products import ProductBase


class Trailer(ProductBase):
    """
    Таблица прицепов.

    Уникальность обеспечивается по полю model_name.
    """

    full_mass: Mapped[int] = mapped_column(
        SmallInteger,
        comment="Общая масса прицепа в кг",
    )
    load_capacity: Mapped[int] = mapped_column(
        SmallInteger,
        comment="Грузоподъемность в кг",
    )
    trailer_length: Mapped[int] = mapped_column(
        SmallInteger,
        comment="Длина прицепа в мм",
    )
    max_ship_length: Mapped[int] = mapped_column(
        SmallInteger,
        comment="Максимальная длина перевозимого судна в мм",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"model_name={self.model_name!r}, "
            f"company_name={self.company_name!r}, "
            f"full_mass={self.full_mass!r}, "
            f"load_capacity={self.load_capacity!r}, "
            f"trailer_length={self.trailer_length!r}, "
            f"max_ship_length={self.max_ship_length!r}, "
            f"description={self.description!r}, "
            f"price={self.price!r}, "
            f"image_id={self.image_id!r}"
            f"type={self.type!r}, "
            f"created_at={self.created_at!r})"
        )

    def __repr__(self):
        return str(self)
