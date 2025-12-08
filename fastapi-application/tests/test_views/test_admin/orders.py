import pytest

from httpx import AsyncClient

from core.config import settings
from core.models.orders.order import Order, OrderStatus


@pytest.mark.anyio
async def test_admin_orders_page(
    superuser_client: AsyncClient,
    test_order: Order,
):
    """
    Тест страницы заказов в админке.
    """
    response = await superuser_client.get(
        f"{settings.view.admin}{settings.view.orders}/"
    )
    assert response.status_code == 200
    assert test_order.product_name in response.text


@pytest.mark.anyio
async def test_admin_update_order(
    superuser_client: AsyncClient,
    test_order: Order,
):
    """
    Тест обновления статуса заказа.
    """
    response = await superuser_client.post(
        url=f"{settings.view.admin}{settings.view.orders}/update-order",
        data={
            "order_id_up": test_order.id,
            "status": "processing",
        },
    )
    assert response.status_code == 200
    assert f"Заказ с ID {test_order.id} успешно обновлен" in response.text
