from datetime import datetime
from pydantic import Field

from core.schemas.base_model import BaseSchemaModel
from core.models.orders.order import OrderStatus


class OrderCreate(BaseSchemaModel):
    """
    Модель создания заказа.
    """

    product_id: int = Field(
        description="ID товар для заказа",
    )
    pickup_point_id: int = Field(
        description="ID пункта самовывоза",
    )


class OrderCreateExtended(OrderCreate):
    """
    Расширенная модель создания заказа.
    """

    user_id: int = Field(
        description="ID владельца заказа",
    )
    status: OrderStatus = Field(
        description="Статус заказа",
    )
    total_price: int = Field(
        description="Общая цена заказа",
    )
    pickup_point_name: str = Field(
        description="Имя пункта самовывоза",
    )
    product_name: str = Field(
        description="Название товара",
    )


class OrderUpdate(BaseSchemaModel):
    """
    Модель обновления заказа.
    """

    status: OrderStatus = Field(
        description="Статус заказа",
    )


class OrderRead(OrderCreateExtended):
    """
    Модель чтения заказа.
    """

    id: int = Field(
        description="ID заказа",
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


class OrderPaymentUpdate(BaseSchemaModel):
    """
    Модель оплаты заказа.
    """

    payment_id: str = Field(
        description="ID платежа в YooKassa",
    )
    payment_url: str = Field(
        description="Ссылка на оплату",
    )
    expires_at: datetime = Field(
        description="Срок действия ссылки",
    )
