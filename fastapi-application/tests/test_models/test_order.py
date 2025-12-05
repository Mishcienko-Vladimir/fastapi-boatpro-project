import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from core.models.user import User
from core.models.products.product_base import Product
from core.models.orders import PickupPoint, Order


@pytest.mark.anyio
async def test_order_creation(
    test_session: AsyncSession,
    test_user: User,
    test_product: Product,
    test_pickup_point: PickupPoint,
):
    """
    Тест создания заказа.
    """
    order = Order(
        user_id=test_user.id,
        pickup_point_id=test_pickup_point.id,
        product_id=test_product.id,
        status="pending",
        total_price=test_product.price,
        product_name=test_product.name,
        type_product=test_product.type_product,
        pickup_point_name=test_pickup_point.name,
        pickup_point_address=test_pickup_point.address,
        work_hours=test_pickup_point.work_hours,
        payment_id="",
        payment_url="",
        expires_at=None,
    )
    test_session.add(order)
    await test_session.commit()
    await test_session.refresh(order)

    assert order.id is not None
    assert order.user_id == test_user.id
    assert order.pickup_point_id == test_pickup_point.id
    assert order.product_id == test_product.id
    assert order.status == "pending"
    assert order.total_price == test_product.price
    assert order.product_name == test_product.name
    assert order.type_product == test_product.type_product
    assert order.pickup_point_name == test_pickup_point.name
    assert order.pickup_point_address == test_pickup_point.address
    assert order.work_hours == test_pickup_point.work_hours
