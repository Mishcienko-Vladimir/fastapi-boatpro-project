from typing import TYPE_CHECKING

from sqlalchemy import Text, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins import IntIdPkMixin, CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from core.models.products import Category  # noqa
    from core.models.products import ImagePath  # noqa
    from core.models.favorite import Favorite  # noqa


class Product(
    IntIdPkMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
    Base,
):
    """
    Базовая модель для товаров, с полиморфизмом.
    """

    __mapper_args__ = {
        "polymorphic_identity": "product",
        "polymorphic_on": "type_product",
    }

    type_product: Mapped[str] = mapped_column(
        String(50),
        doc="Полиморфизм для разделения типов товаров",
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        doc="Внешний ключ к ID категории",
    )
    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
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
    is_active: Mapped[bool] = mapped_column(
        default=True,
        comment="Наличие товара",
    )

    # Many-to-Many отношение к изображениям
    images: Mapped[list["ImagePath"]] = relationship(
        secondary="product_images_associations",
        back_populates="products",
    )

    # Обратная ссылка на категорию
    category: Mapped["Category"] = relationship(
        back_populates="products",
    )

    # Обратная связь с избранным
    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="product",
    )
