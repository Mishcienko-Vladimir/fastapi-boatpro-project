import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker

from api.api_v1.services.orders_service import OrdersService

from core.models.user import User
from core.models.products import Product
from core.models.orders import Order, PickupPoint, OrderStatus

from core.schemas.order import (
    OrderCreate,
    OrderUpdate,
)


faker = Faker()


@pytest.mark.anyio
async def test_create_order(
    test_session: AsyncSession,
    test_user: User,
    test_product: Product,
    test_pickup_point: PickupPoint,
):
    """
    Тест создания заказа через сервис OrderService.
    """
    order_data = OrderCreate(
        product_id=test_product.id,
        pickup_point_id=test_pickup_point.id,
    )
    service = OrdersService(session=test_session)
    order = await service.create_order(
        user_id=test_user.id,
        order_data=order_data,
    )

    assert order.id is not None
    assert order.created_at is not None
    assert order.product_id is not None
    assert order.status == "pending"
    assert order.user_id == test_user.id
    assert order.product_name == test_product.name
    assert order.total_price == test_product.price
    assert order.type_product == test_product.type_product
    assert order.pickup_point_name == test_pickup_point.name
    assert order.pickup_point_address == test_pickup_point.address
    assert order.work_hours == test_pickup_point.work_hours


@pytest.mark.anyio
async def test_get_orders_by_user(
    test_session: AsyncSession,
    test_order: Order,
):
    """
    Тест получения заказов пользователя через сервис OrderService.
    """
    service = OrdersService(session=test_session)
    orders = await service.get_orders_by_user(user_id=test_order.user_id)

    assert orders is not None
    assert len(orders) >= 1


@pytest.mark.anyio
async def test_get_all_orders(
    test_session: AsyncSession,
    test_order: Order,
):
    """
    Тест получения всех заказов через сервис OrderService.
    """
    service = OrdersService(session=test_session)
    orders = await service.get_all_orders()

    assert orders is not None
    assert len(orders) >= 1


@pytest.mark.anyio
async def test_update_order_status(
    test_session: AsyncSession,
    test_order: Order,
):
    """
    Тест обновления статуса заказа по id через сервис OrderService.
    """
    order_update = OrderUpdate(status=OrderStatus.PROCESSING)
    service = OrdersService(session=test_session)
    updated_order = await service.update_order_status(
        order_id=test_order.id,
        order_update=order_update,
    )

    assert updated_order is not None
    assert updated_order.id == test_order.id
    assert updated_order.status == OrderStatus.PROCESSING
