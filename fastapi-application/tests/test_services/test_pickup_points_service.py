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
async def test_get_pickup_point_by_id(test_session: AsyncSession):
    """
    Тест получения точки самовывоза по ID.
    """
    service = PickupPointsService(session=test_session)
    pickup_point_data = PickupPointCreate(
        name=f"Pickup Point-{faker.uuid4()[:100]}",
        address=faker.address(),
        work_hours="Пн-Вс: 9:00-21:00",
    )
    created = await service.create_pickup_point(pickup_point_data)
    retrieved = await service.get_pickup_point_by_id(created.id)

    assert retrieved.id == created.id
    assert retrieved.name == created.name
    assert retrieved.address == created.address
    assert retrieved.work_hours == created.work_hours


@pytest.mark.anyio
async def test_get_pickup_point_by_name(test_session: AsyncSession):
    """
    Тест получения точки самовывоза по имени.
    """
    service = PickupPointsService(session=test_session)
    original_name = f"Pickup Point-{faker.uuid4()[:100]}"
    pickup_point_data = PickupPointCreate(
        name=original_name,
        address=faker.address(),
        work_hours="Пн-Вс: 9:00-21:00",
    )
    created = await service.create_pickup_point(pickup_point_data)
    retrieved = await service.get_pickup_point_by_name(original_name)

    assert retrieved.id == created.id
    assert retrieved.name == original_name
    assert retrieved.address == created.address


@pytest.mark.anyio
async def test_get_pickup_points(test_session: AsyncSession):
    """
    Тест получения всех точек самовывоза.
    """
    service = PickupPointsService(session=test_session)

    names = [f"Pickup-{faker.uuid4()[:8]}" for _ in range(3)]
    created_ids = []

    for name in names:
        data = PickupPointCreate(
            name=name,
            address=faker.address(),
            work_hours="Пн-Вс: 9:00-21:00",
        )
        created = await service.create_pickup_point(data)
        created_ids.append(created.id)

    all_points = await service.get_pickup_points()
    retrieved_ids = {p.id for p in all_points}

    assert all(created_id in retrieved_ids for created_id in created_ids)
    assert len(all_points) >= 3


@pytest.mark.anyio
async def test_update_pickup_point_by_id(test_session: AsyncSession):
    """
    Тест обновления точки самовывоза по ID.
    """
    service = PickupPointsService(session=test_session)

    pickup_point_data = PickupPointCreate(
        name=f"Pickup Point-{faker.uuid4()[:100]}",
        address=faker.address(),
        work_hours="Пн-Вс: 9:00-21:00",
    )
    created = await service.create_pickup_point(pickup_point_data)

    update_data = PickupPointUpdate(
        name=f"Updated-{faker.uuid4()[:10]}",
        address=faker.address(),
        work_hours="Пн-Пт: 10:00-18:00",
    )
    updated = await service.update_pickup_point_by_id(
        pickup_point_id=created.id,
        pickup_point_data=update_data,
    )

    assert updated.id == created.id
    assert updated.name == update_data.name
    assert updated.address == update_data.address
    assert updated.work_hours == update_data.work_hours

    result = await test_session.execute(
        select(PickupPoint).where(PickupPoint.id == created.id)
    )
    db_point = result.scalars().first()
    assert db_point.name == update_data.name
    assert db_point.address == update_data.address
