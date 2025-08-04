from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from core.models.products.product_base import ProductBase


class ProductType(IntIdPkMixin, Base):
    """
    Таблица категорий товаров.

    Уникальность обеспечивается по полю name_product_type.
    """

    name_product_type: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    products: Mapped[list["ProductBase"]] = relationship(back_populates="type")

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id!r}, "
            f"name_product_type='{self.name_product_type}')"
        )

    def __repr__(self):
        return str(self)
