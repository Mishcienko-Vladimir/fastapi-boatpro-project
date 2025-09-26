from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins import IntIdPkMixin, CreatedAtMixin

if TYPE_CHECKING:
    from core.models.user import User  # noqa
    from core.models.products.product_base import Product  # noqa


class Favorite(
    IntIdPkMixin,
    CreatedAtMixin,
    Base,
):
    """
    Таблица избранного: связывает пользователей и товары.
    """

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)

    # Связь с пользователем
    user: Mapped["User"] = relationship(back_populates="favorites")
    # Связь с товаром
    product: Mapped["Product"] = relationship(back_populates="favorites")

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id}, "
            f"user_id={self.user_id!r}, "
            f"product_id={self.product_id!r}, "
            f"created_at={self.created_at!r})"
        )

    def __repr__(self):
        return str(self)
