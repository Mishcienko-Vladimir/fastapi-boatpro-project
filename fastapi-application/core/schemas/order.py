from datetime import datetime
from pydantic import Field

from core.schemas.base_model import BaseSchemaModel
from core.models.orders.order import OrderStatus


class OrderCreate(BaseSchemaModel):
    """
    Модель создания заказа.
    """

    product_id: int = Field(
        description="ID владельца заказа",
    )
    pickup_point_id: int = Field(
        description="ID пункта самовывоза",
    )


class OrderUpdate(BaseSchemaModel):
    """
    Модель обновления заказа.
    """

    status: OrderStatus = Field(
        description="Статус заказа",
    )


class OrderRead(BaseSchemaModel):
    """
    Модель чтения заказа.
    """

    id: int = Field(
        description="ID заказа",
    )
    user_id: int = Field(
        description="ID владельца заказа",
    )
    pickup_point_id: int = Field(
        description="ID пункта самовывоза",
    )
    product_id: int = Field(
        description="ID товара",
    )
    status: OrderStatus = Field(
        description="Статус заказа",
    )
    total_price: int = Field(
        description="Общая цена заказа",
    )
    pickup_point_name: str = Field(
        description="Имея пункта самовывоза",
    )
    product_name: str = Field(
        description="Название товара",
    )
    created_at: datetime = Field(
        description="Дата создания заказа",
    )
    payment_id: str | None = Field(
        description="ID платежа в YooKassa",
    )
    payment_url: str | None = Field(
        description="Ссылка на оплату",
    )
    expires_at: datetime | None = Field(
        description="Срок действия ссылки",
    )
