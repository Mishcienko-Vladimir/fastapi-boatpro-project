import pytest

from httpx import AsyncClient
from faker import Faker

from core.config import settings
from core.models.orders.order import Order, OrderStatus
from core.models.products import Product
from core.models.orders.pickup_point import PickupPoint


faker = Faker()


@pytest.fixture(scope="module")
def prefix_orders() -> str:
    """Префикс для заказов."""
    return f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.orders}"


@pytest.mark.anyio
async def test_create_order(
    logged_in_client: AsyncClient,
    test_product: Product,
    test_pickup_point: PickupPoint,
    prefix_orders: str,
):
    """
    Тест создания заказа, через API.
    """
    order_data = {
        "product_id": test_product.id,
        "pickup_point_id": test_pickup_point.id,
    }
    response = await logged_in_client.post(
        url=f"{prefix_orders}/",
        json=order_data,
    )
    assert response.status_code == 201
    result = response.json()

    assert result["id"] is not None
    assert result["user_id"] is not None
    assert result["created_at"] is not None
    assert result["product_id"] is not None
    assert result["status"] == "pending"
    assert result["product_name"] == test_product.name
    assert result["total_price"] == test_product.price
    assert result["type_product"] == test_product.type_product
    assert result["pickup_point_name"] == test_pickup_point.name
    assert result["pickup_point_address"] == test_pickup_point.address
    assert result["work_hours"] == test_pickup_point.work_hours


@pytest.mark.anyio
async def test_get_user_orders(
    logged_in_client: AsyncClient,
    test_product: Product,
    test_pickup_point: PickupPoint,
    prefix_orders: str,
):
    """
    Тест получения заказа текущего пользователя, через API.
    """
    order_data = {
        "product_id": test_product.id,
        "pickup_point_id": test_pickup_point.id,
    }
    response = await logged_in_client.post(
        url=f"{prefix_orders}/",
        json=order_data,
    )
    assert response.status_code == 201

    get_orders = await logged_in_client.get(url=f"{prefix_orders}/")
    assert get_orders.status_code == 200
    result = get_orders.json()

    assert len(result) >= 1


@pytest.mark.anyio
async def test_get_all_orders(
    client: AsyncClient,
    test_order: Order,
    prefix_orders: str,
):
    """
    Тест получения всех заказов, через API.
    """
    response = await client.get(url=f"{prefix_orders}/all-orders")
    assert response.status_code == 200
    result = response.json()

    assert len(result) >= 1


@pytest.mark.anyio
async def test_update_order_status(
    client: AsyncClient,
    test_order: Order,
    prefix_orders: str,
):
    """
    Тест изменения статуса заказа по id, через API.
    """
    update_data = {
        "status": OrderStatus.CANCELLED,
    }
    response = await client.patch(
        url=f"{prefix_orders}/{test_order.id}/",
        json=update_data,
    )
    assert response.status_code == 200
    result = response.json()

    assert result["id"] == test_order.id
    assert result["status"] == OrderStatus.CANCELLED
