import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models.orders.pickup_point import PickupPoint


@pytest.mark.anyio
async def test_pickup_point_creation(
    test_session: AsyncSession,
    test_pickup_point: PickupPoint,
):
    """
    Тест создания пункта выдачи.
    """

    assert test_pickup_point.id is not None
    assert test_pickup_point.name is not None
    assert test_pickup_point.address is not None
    assert test_pickup_point.work_hours is not None
    assert isinstance(test_pickup_point.address, str)


@pytest.mark.anyio
async def test_pickup_point_relationship_orders_empty(
    test_session: AsyncSession,
    test_pickup_point: PickupPoint,
):
    """
    Тест, что у нового пункта выдачи нет заказов.
    """

    stmt = (
        select(PickupPoint)
        .options(selectinload(PickupPoint.orders))
        .where(PickupPoint.id == test_pickup_point.id)
    )
    result = await test_session.execute(stmt)
    loaded_pickup_point = result.scalar_one()

    assert hasattr(
        loaded_pickup_point, "orders"
    ), "PickupPoint должна иметь атрибут orders"
    assert isinstance(loaded_pickup_point.orders, list)
    assert len(loaded_pickup_point.orders) == 0
