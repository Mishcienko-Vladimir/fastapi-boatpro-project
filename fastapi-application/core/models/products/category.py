from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from core.models.products.product_base import Product  # noqa


class Category(IntIdPkMixin, Base):
    """
    Таблица категорий товаров.

    Уникальность обеспечивается по полю name и id.
    """

    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        comment="Название категории",
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        comment="Описание категории",
    )
    # Связь с продуктами через полиморфное наследование
    products: Mapped[list["Product"]] = relationship(back_populates="category")

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id!r}, "
            f"name_product_type='{self.name!r}' "
            f"description='{self.description!r}')"
        )

    def __repr__(self):
        return str(self)
