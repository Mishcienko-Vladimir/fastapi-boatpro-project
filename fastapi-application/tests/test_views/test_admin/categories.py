import pytest

from httpx import AsyncClient

from core.config import settings
from core.models.products import Category


@pytest.mark.anyio
async def test_admin_categories_page(
    superuser_client: AsyncClient,
    test_category: Category,
):
    """
    Тест страницы категорий в админке.
    """
    response = await superuser_client.get(
        f"{settings.view.admin}{settings.view.catalog}/"
    )
    assert response.status_code == 200
    assert test_category.name in response.text


@pytest.mark.anyio
async def test_admin_create_category(superuser_client: AsyncClient):
    """
    Тест создания категории.
    """
    response = await superuser_client.post(
        url=f"{settings.view.admin}{settings.view.catalog}/create-category",
        data={
            "category_name": "Новая Категория",
            "category_description": "Описание новой категории",
        },
    )
    assert response.status_code == 200
    assert f"Категория &#39;Новая Категория&#39; успешно создана." in response.text


@pytest.mark.anyio
async def test_admin_update_category(
    superuser_client: AsyncClient,
    test_category: Category,
):
    """
    Тест обновления категории.
    """
    response = await superuser_client.post(
        url=f"{settings.view.admin}{settings.view.catalog}/update-category",
        data={
            "category_id_up": test_category.id,
            "new_name": "Обновлённая Категория",
        },
    )
    assert response.status_code == 200
    assert f"Категория с ID {test_category.id} успешно обновлена." in response.text


@pytest.mark.anyio
async def test_admin_delete_category(
    superuser_client: AsyncClient,
    test_category: Category,
):
    """
    Тест удаления категории.
    """
    response = await superuser_client.post(
        url=f"{settings.view.admin}{settings.view.catalog}/delete-category",
        data={"category_id_del": test_category.id},
    )
    assert response.status_code == 200
    assert f"Категория с ID {test_category.id} успешно удалена." in response.text
