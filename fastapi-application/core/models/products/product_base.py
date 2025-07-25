from typing import TYPE_CHECKING

from sqlalchemy import Text, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins import IntIdPkMixin, CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from core.models.products import ProductType


class ProductBase(
    IntIdPkMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
    Base,
):
    """
    Базовая модель для товаров
    """

    __abstract__ = True  # Абстрактная модель, не создает таблицу

    type_id: Mapped[int] = mapped_column(
        ForeignKey("product_types.id"),
    )
    model_name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        comment="Название модели",
    )
    price: Mapped[int] = mapped_column(
        comment="Цена в рублях",
    )
    company_name: Mapped[str] = mapped_column(
        String(100),
        comment="Название производителя",
    )
    description: Mapped[str] = mapped_column(
        Text,
        comment="Описание",
    )
    image_id: Mapped[list[int]] = mapped_column(
        comment="ID изображения",
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        comment="Наличие товара",
    )

    type: Mapped["ProductType"] = relationship(back_populates="products")
