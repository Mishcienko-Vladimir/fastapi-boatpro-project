from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from core.models.products import ProductBase


class ProductType(IntIdPkMixin, Base):
    """
    Таблица категорий товаров.

    Уникальность обеспечивается по полю name_product_type.
    """

    name_product_type: Mapped[str] = mapped_column(String(50), unique=True)

    products: Mapped[list["ProductBase"]] = relationship(back_populates="type")
