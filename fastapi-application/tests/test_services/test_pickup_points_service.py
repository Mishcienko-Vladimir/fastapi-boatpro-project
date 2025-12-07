import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker

from api.api_v1.services.pickup_points_service import PickupPointsService

from core.schemas.pickup_point import (
    PickupPointCreate,
    PickupPointUpdate,
    PickupPointRead,
)
from core.models.orders.pickup_point import PickupPoint


faker = Faker()


@pytest.mark.anyio
async def test_create_pickup_points(
    test_session: AsyncSession,
):
    """
    Тест создания точки самовывоза через сервис PickupPointsService.
    """
    service = PickupPointsService(session=test_session)
    pickup_point_data = PickupPointCreate(
        name=f"Pickup Point-{faker.uuid4()[:100]}",
        address=faker.address(),
        work_hours="Пн-Вс: 9:00-21:00",
    )
    pickup_point = await service.create_pickup_point(pickup_point_data)

    assert pickup_point.id is not None
    assert isinstance(pickup_point, PickupPointRead)

    result = await test_session.execute(
        select(PickupPoint).where(PickupPoint.id == pickup_point.id)
    )
    db_pickup_point = result.scalars().first()

    assert db_pickup_point is not None
    assert db_pickup_point.name == pickup_point_data.name
    assert db_pickup_point.address == pickup_point_data.address
    assert db_pickup_point.work_hours == pickup_point_data.work_hours


@pytest.mark.anyio
async def test_get_pickup_point_by_id(
    test_session: AsyncSession,
    test_pickup_point: PickupPoint,
):
    """
    Тест получения точки самовывоза по ID.
    """
    service = PickupPointsService(session=test_session)
    retrieved = await service.get_pickup_point_by_id(test_pickup_point.id)

    assert retrieved.id == test_pickup_point.id
    assert retrieved.name == test_pickup_point.name
    assert retrieved.address == test_pickup_point.address
    assert retrieved.work_hours == test_pickup_point.work_hours


@pytest.mark.anyio
async def test_get_pickup_point_by_name(
    test_session: AsyncSession,
    test_pickup_point: PickupPoint,
):
    """
    Тест получения точки самовывоза по имени.
    """
    service = PickupPointsService(session=test_session)
    retrieved = await service.get_pickup_point_by_name(test_pickup_point.name)

    assert retrieved.id == test_pickup_point.id
    assert retrieved.name == test_pickup_point.name
    assert retrieved.address == test_pickup_point.address


@pytest.mark.anyio
async def test_get_pickup_points(
    test_session: AsyncSession,
    test_pickup_point: PickupPoint,
):
    """
    Тест получения всех точек самовывоза.
    """
    service = PickupPointsService(session=test_session)
    all_points = await service.get_pickup_points()

    assert len(all_points) >= 1


@pytest.mark.anyio
async def test_update_pickup_point_by_id(
    test_session: AsyncSession,
    test_pickup_point: PickupPoint,
):
    """
    Тест обновления точки самовывоза по ID.
    """
    service = PickupPointsService(session=test_session)

    update_data = PickupPointUpdate(
        name=f"Updated-{faker.uuid4()[:100]}",
        address=faker.address(),
        work_hours="Пн-Пт: 10:00-18:00",
    )
    updated = await service.update_pickup_point_by_id(
        pickup_point_id=test_pickup_point.id,
        pickup_point_data=update_data,
    )

    assert updated.id == test_pickup_point.id
    assert updated.name == update_data.name
    assert updated.address == update_data.address
    assert updated.work_hours == update_data.work_hours

    result = await test_session.execute(
        select(PickupPoint).where(PickupPoint.id == test_pickup_point.id)
    )
    db_point = result.scalars().first()
    assert db_point.name == update_data.name
    assert db_point.address == update_data.address


@pytest.mark.anyio
async def test_delete_pickup_point_by_id(
    test_session: AsyncSession,
    test_pickup_point: PickupPoint,
):
    """
    Тест удаления точки самовывоза по ID.
    """
    service = PickupPointsService(session=test_session)
    await service.delete_pickup_point_by_id(pickup_point_id=test_pickup_point.id)

    stmt = select(PickupPoint).where(PickupPoint.id == test_pickup_point.id)
    result = await test_session.execute(stmt)
    assert result.scalars().first() is None
