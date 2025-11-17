from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins import IntIdPkMixin, CreatedAtMixin

if TYPE_CHECKING:
    from .pickup_point import PickupPoint  # noqa
    from core.models.user import User  # noqa
    from core.models.products.product_base import Product  # noqa


class OrderStatus(str, Enum):
    """Статус заказа."""

    PENDING = "pending"  # Ожидает оплаты
    PAID = "paid"  # Оплачен
    CANCELLED = "cancelled"  # Отменён
    PROCESSING = "processing"  # В обработке
    READY = "ready"  # Готов к выдаче
    COMPLETED = "completed"  # Завершён


class Order(
    IntIdPkMixin,
    CreatedAtMixin,
    Base,
):
    """
    Таблица заказов.
    """

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        comment="ID владельца заказа",
    )
    pickup_point_id: Mapped[int] = mapped_column(
        ForeignKey("pickup_points.id"),
        comment="ID пункта самовывоза",
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        comment="ID купленного товара",
    )
    status: Mapped[OrderStatus] = mapped_column(
        default=OrderStatus.PENDING,
        comment="Статус заказа",
    )
    total_price: Mapped[int] = mapped_column(
        comment="Цена на момент заказа",
    )
    payment_id: Mapped[str | None] = mapped_column(
        String(255),
        comment="ID платежа в YooKassa",
    )
    payment_url: Mapped[str | None] = mapped_column(
        String(500),
        comment="Ссылка для оплаты",
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        comment="Срок действия ссылки",
    )

    # Обратные ссылки на: Пользователя, Пункт выдачи и Товара.
    user: Mapped["User"] = relationship(
        back_populates="orders",
    )
    pickup_point: Mapped["PickupPoint"] = relationship(
        back_populates="orders",
    )
    product: Mapped["Product"] = relationship(
        back_populates="orders",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id}, "
            f"user_id={self.user_id!r}, "
            f"pickup_point_id={self.pickup_point_id!r}, "
            f"product_id={self.product_id!r}, "
            f"status={self.status!r}, "
            f"total_price={self.total_price!r}, "
            f"payment_id={self.payment_id!r}, "
            f"payment_url={self.payment_url!r}, "
            f"expires_at={self.expires_at!r}, "
            f"created_at={self.created_at!r})"
        )

    def __repr__(self):
        return str(self)
