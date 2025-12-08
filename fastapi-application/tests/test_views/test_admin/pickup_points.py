import pytest

from httpx import AsyncClient

from core.config import settings
from core.models.orders.pickup_point import PickupPoint


@pytest.mark.anyio
async def test_admin_pickup_points_page(
    superuser_client: AsyncClient,
    test_pickup_point: PickupPoint,
):
    """
    Тест страницы пунктов выдачи в админке.
    """
    response = await superuser_client.get(
        f"{settings.view.admin}{settings.view.pickup_points}/"
    )
    assert response.status_code == 200
    assert test_pickup_point.name in response.text


@pytest.mark.anyio
async def test_admin_create_pickup_point(superuser_client: AsyncClient):
    """
    Тест создания пункта выдачи.
    """
    response = await superuser_client.post(
        url=f"{settings.view.admin}{settings.view.pickup_points}/create-pickup-point",
        data={
            "pickup_point_name": "Новый пункт выдачи",
            "address": "Новый адрес",
            "work_hours": "Пн-Вс 00:00-24:00",
        },
    )
    assert response.status_code == 200
    assert (
        f"Пункт выдачи с именем &#39;Новый пункт выдачи&#39; успешно создан."
        in response.text
    )


@pytest.mark.anyio
async def test_admin_update_pickup_point(
    superuser_client: AsyncClient,
    test_pickup_point: PickupPoint,
):
    """
    Тест обновления пункта выдачи.
    """
    response = await superuser_client.post(
        url=f"{settings.view.admin}{settings.view.pickup_points}/update-pickup-point",
        data={
            "pickup_point_id_up": test_pickup_point.id,
            "pickup_point_new_name": "Обновлённый пункт выдачи",
            "address": "Обновлённый адрес",
            "work_hours": "Обновлённый режим работы",
        },
    )
    assert response.status_code == 200
    assert (
        f"Пункт выдачи с ID {test_pickup_point.id} успешно обновлена." in response.text
    )


@pytest.mark.anyio
async def test_admin_delete_pickup_point(
    superuser_client: AsyncClient,
    test_pickup_point: PickupPoint,
):
    """
    Тест удаления пункта выдачи по id.
    """
    response = await superuser_client.post(
        url=f"{settings.view.admin}{settings.view.pickup_points}/delete-pickup-point",
        data={"pickup_point_id_del": test_pickup_point.id},
    )
    assert response.status_code == 200
    assert f"Пункт выдачи с ID {test_pickup_point.id} успешно удалена." in response.text
