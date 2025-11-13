import pytest

from httpx import AsyncClient

from core.config import settings
from core.models.products import Category, Trailer


@pytest.mark.anyio
async def test_admin_trailers_page(
    superuser_client: AsyncClient,
    test_trailer: Trailer,
):
    """
    Тест страницы прицепов в админке.
    """
    response = await superuser_client.get(
        url=f"{settings.view.admin}{settings.view.trailers}/"
    )
    assert response.status_code == 200
    assert test_trailer.name in response.text


@pytest.mark.anyio
async def test_admin_create_trailer(
    superuser_client: AsyncClient,
    test_category: Category,
):
    """
    Тест создания прицепа.
    """
    response = await superuser_client.post(
        url=f"{settings.view.admin}{settings.view.trailers}/create-trailer",
        data={
            "category_id": test_category.id,
            "name": "Новый Прицеп",
            "price": 150000,
            "company_name": "TrailerPro",
            "description": "Описание прицепа",
            "is_active": "on",
            "full_mass": 1000,
            "load_capacity": 800,
            "trailer_length": 600,
            "max_ship_length": 500,
        },
        files={"images": ("test_trailer.jpg", b"file_content", "image/jpeg")},
    )
    assert response.status_code == 200
    assert "Прицеп с ID" in response.text
    assert "успешно создан" in response.text


@pytest.mark.anyio
async def test_admin_update_trailer(
    superuser_client: AsyncClient,
    test_trailer: Trailer,
):
    """
    Тест обновления прицепа.
    """
    response = await superuser_client.post(
        url=f"{settings.view.admin}{settings.view.trailers}/update-trailer",
        data={
            "trailer_id_up": test_trailer.id,
            "name": "Обновлённый Прицеп",
            "price": 180000,
            "load_capacity": 900,
        },
    )
    assert response.status_code == 200
    assert f"Прицеп с ID {test_trailer.id} успешно обновлен" in response.text


@pytest.mark.anyio
async def test_admin_delete_trailer(
    superuser_client: AsyncClient,
    test_trailer: Trailer,
):
    """
    Тест удаления прицепа.
    """
    response = await superuser_client.post(
        url=f"{settings.view.admin}{settings.view.trailers}/delete-trailer",
        data={"trailer_id_del": test_trailer.id},
    )
    assert response.status_code == 200
    assert (
        "успешно удален" in response.text or "missing from the folder" in response.text
    )
    list_response = await superuser_client.get(
        url=f"{settings.view.admin}{settings.view.trailers}/"
    )
    assert test_trailer.name not in list_response.text
