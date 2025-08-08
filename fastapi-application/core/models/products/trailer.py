from sqlalchemy import SmallInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.models.products.product_base import Product


class Trailer(Product):
    """
    Таблица прицепов.

    Уникальность обеспечивается по полю name и id.
    """

    __mapper_args__ = {"polymorphic_identity": "trailer"}

    id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        primary_key=True,
        doc="Для полиморфной связи с таблицей products",
    )
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
        comment="Длина прицепа в см",
    )
    max_ship_length: Mapped[int] = mapped_column(
        SmallInteger,
        comment="Максимальная длина перевозимого судна в см",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id}, "
            f"name={self.name!r}, "
            f"price={self.price!r}, "
            f"company_name={self.company_name!r}, "
            f"description={self.description!r}, "
            f"images={self.images!r}, "
            f"is_active={self.is_active!r}, "
            f"full_mass={self.full_mass!r}, "
            f"load_capacity={self.load_capacity!r}, "
            f"trailer_length={self.trailer_length!r}, "
            f"max_ship_length={self.max_ship_length!r}, "
            f"category_id={self.category_id!r}, "
            f"type_product={self.type_product!r}, "
            f"created_at={self.created_at!r}, "
            f"updated_at={self.updated_at!r})"
        )

    def __repr__(self):
        return str(self)
