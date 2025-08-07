from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins import IntIdPkMixin
from core.models.products.product_base import product_images_association

if TYPE_CHECKING:
    from core.models.products.product_base import Product  # noqa


class ImagePath(IntIdPkMixin, Base):
    """
    Таблица для хранения путей к изображениям.

    Уникальность обеспечивается по полю id.
    """

    path: Mapped[str] = mapped_column(String(255), comment="Путь к изображению")

    # Many-to-Many обратная ссылка
    products: Mapped[list["Product"]] = relationship(
        secondary=product_images_association,
        back_populates="images",
    )

    def __str__(self):
        return f"{self.__class__.__name__} (id={self.id!r}, path={self.path!r})"

    def __repr__(self):
        return str(self)
