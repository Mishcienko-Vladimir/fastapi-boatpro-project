import pytest

from httpx import AsyncClient
from faker import Faker

from core.config import settings
from core.models.orders.pickup_point import PickupPoint

faker = Faker()


@pytest.fixture(scope="module")
def prefix_pickup_points() -> str:
    """Префикс для пунктов выдачи."""
    return (
        f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.pickup_points}"
    )


@pytest.mark.anyio
async def test_create_pickup_point(
    client: AsyncClient,
    prefix_pickup_points: str,
):
    """
    Тест создания пункта выдачи, через API.
    """
    pickup_point_data = {
        "name": f"Pickup Point-{faker.uuid4()[:100]}",
        "address": faker.address(),
        "work_hours": "Пн-Вс с 9:00 до 18:00",
    }
    response = await client.post(
        url=f"{prefix_pickup_points}/",
        json=pickup_point_data,
    )
    assert response.status_code == 201
    result = response.json()

    assert result["id"] is not None
    assert result["name"] == pickup_point_data["name"]
    assert result["address"] == pickup_point_data["address"]
    assert result["work_hours"] == pickup_point_data["work_hours"]


@pytest.mark.anyio
async def test_get_pickup_point_by_name(
    client: AsyncClient,
    test_pickup_point: PickupPoint,
    prefix_pickup_points: str,
):
    """
    Тест получения пункта выдачи по имени, через API.
    """
    response = await client.get(
        url=f"{prefix_pickup_points}/pickup-point-name/{test_pickup_point.name}/",
    )
    assert response.status_code == 200
    result = response.json()

    assert result["id"] == test_pickup_point.id
    assert result["name"] == test_pickup_point.name
    assert result["address"] == test_pickup_point.address
    assert result["work_hours"] == test_pickup_point.work_hours


@pytest.mark.anyio
async def test_get_pickup_point_by_id(
    client: AsyncClient,
    test_pickup_point: PickupPoint,
    prefix_pickup_points: str,
):
    """
    Тест получения пункта выдачи по id, через API.
    """
    response = await client.get(
        url=f"{prefix_pickup_points}/pickup-point-id/{test_pickup_point.id}/",
    )
    assert response.status_code == 200
    result = response.json()

    assert result["id"] == test_pickup_point.id
    assert result["name"] == test_pickup_point.name
    assert result["address"] == test_pickup_point.address
    assert result["work_hours"] == test_pickup_point.work_hours


@pytest.mark.anyio
async def test_get_all_pickup_points(
    client: AsyncClient,
    test_pickup_point: PickupPoint,
    prefix_pickup_points: str,
):
    """
    Тест получения всех пунктов выдачи, через API.
    """
    response = await client.get(url=f"{prefix_pickup_points}/")
    assert response.status_code == 200
    result = response.json()

    assert len(result) >= 1


@pytest.mark.anyio
async def test_update_pickup_point_by_id(
    client: AsyncClient,
    test_pickup_point: PickupPoint,
    prefix_pickup_points: str,
):
    """
    Тест обновления пункта выдачи по id, через API.
    """
    update_data = {
        "address": "Обновлённый адрес",
        "work_hours": "Не работает",
    }

    response = await client.patch(
        url=f"{prefix_pickup_points}/{test_pickup_point.id}/",
        json=update_data,
    )
    assert response.status_code == 200
    updated = response.json()

    assert updated["id"] == test_pickup_point.id
    assert updated["name"] == test_pickup_point.name
    assert updated["address"] == update_data["address"]
    assert updated["work_hours"] == update_data["work_hours"]


@pytest.mark.anyio
async def test_delete_pickup_point_by_id(
    client: AsyncClient,
    test_pickup_point: PickupPoint,
    prefix_pickup_points: str,
):
    """
    Тест удаления пункта выдачи по id, через API.
    """
    pickup_point_id = test_pickup_point.id
    response = await client.delete(
        url=f"{prefix_pickup_points}/{pickup_point_id}/",
    )
    assert response.status_code == 204

    get_response = await client.get(
        url=f"{prefix_pickup_points}/pickup-point-id/{pickup_point_id}/",
    )
    assert get_response.status_code == 404

    delete_response = await client.delete(
        url=f"{prefix_pickup_points}/{pickup_point_id}/",
    )
    assert delete_response.status_code == 404
