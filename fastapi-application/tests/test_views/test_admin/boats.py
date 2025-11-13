import pytest

from httpx import AsyncClient

from core.config import settings
from core.models.products import Category, Boat


@pytest.mark.anyio
async def test_admin_boats_page(
    superuser_client: AsyncClient,
    test_boat: Boat,
):
    """
    Тест страницы катеров в админке.
    """
    response = await superuser_client.get(
        url=f"{settings.view.admin}{settings.view.boats}/"
    )
    assert response.status_code == 200
    assert test_boat.name in response.text


@pytest.mark.anyio
async def test_admin_create_boat(
    superuser_client: AsyncClient,
    test_category: Category,
):
    """
    Тест создания катера.
    """
    response = await superuser_client.post(
        url=f"{settings.view.admin}{settings.view.boats}/create-boat",
        data={
            "category_id": test_category.id,
            "name": "Новый Катер",
            "price": 500000,
            "company_name": "BoatPro",
            "description": "Описание катера",
            "is_active": "on",
            "length_hull": 500,
            "width_hull": 200,
            "weight": 300,
            "capacity": 4,
            "maximum_load": 800,
            "hull_material": "Fiberglass",
            "thickness_side_sheet": 50,
            "bottom_sheet_thickness": 60,
            "fuel_capacity": 50,
            "maximum_engine_power": 150,
            "height_side_midship": 100,
            "transom_height": 50,
        },
        files={"images": ("test_boat.jpg", b"file_content", "image/jpeg")},
    )
    assert response.status_code == 200
    assert "Катер с ID" in response.text
    assert "успешно создан" in response.text


@pytest.mark.anyio
async def test_admin_update_boat(
    superuser_client: AsyncClient,
    test_boat: Boat,
):
    """
    Тест обновления катера.
    """
    response = await superuser_client.post(
        url=f"{settings.view.admin}{settings.view.boats}/update-boat",
        data={
            "boat_id_up": test_boat.id,
            "name": "Обновлённый Катер",
            "price": 600000,
            "capacity": 5,
        },
    )
    assert response.status_code == 200
    assert f"Катер с ID {test_boat.id} успешно обновлен" in response.text


@pytest.mark.anyio
async def test_admin_delete_boat(
    superuser_client: AsyncClient,
    test_boat: Boat,
):
    """
    Тест удаления катера.
    """
    response = await superuser_client.post(
        url=f"{settings.view.admin}{settings.view.boats}/delete-boat",
        data={"boat_id_del": test_boat.id},
    )
    assert response.status_code == 200
    assert (
        "успешно удален" in response.text or "missing from the folder" in response.text
    )
    list_response = await superuser_client.get(
        url=f"{settings.view.admin}{settings.view.boats}/"
    )
    assert test_boat.name not in list_response.text
