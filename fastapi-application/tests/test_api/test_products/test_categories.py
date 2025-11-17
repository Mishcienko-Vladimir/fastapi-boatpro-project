import pytest

from typing import Any
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_category(
    client: AsyncClient,
    prefix_categories: str,
    fake_category_data: dict[str, Any],
):
    """
    Тест создания категории, через API.
    """
    response = await client.post(
        url=f"{prefix_categories}/",
        json=fake_category_data,
    )
    assert response.status_code == 201
    json = response.json()

    assert json["name"] == fake_category_data["name"]


@pytest.mark.anyio
async def test_get_all_categories(
    client: AsyncClient,
    prefix_categories: str,
    fake_category_data: dict[str, Any],
):
    """
    Тест получения всех категорий, через API.
    """
    await client.post(
        url=f"{prefix_categories}/",
        json=fake_category_data,
    )

    response = await client.get(url=f"{prefix_categories}/")
    assert response.status_code == 200
    categories = response.json()

    assert len(categories) >= 1
    assert any(
        category["name"] == fake_category_data["name"] for category in categories
    )


@pytest.mark.anyio
async def test_get_category_by_name(
    client: AsyncClient,
    prefix_categories: str,
    fake_category_data: dict[str, Any],
):
    """
    Тест получения категории по имени, через API.
    """
    await client.post(
        url=f"{prefix_categories}/",
        json=fake_category_data,
    )

    name = fake_category_data["name"]
    response = await client.get(url=f"{prefix_categories}/category-name/{name}")

    assert response.status_code == 200
    assert response.json()["name"] == name


@pytest.mark.anyio
async def test_get_category_by_id(
    client: AsyncClient,
    prefix_categories: str,
    fake_category_data: dict[str, Any],
):
    """
    Тест получения категории по id, через API.
    """
    response = await client.post(
        url=f"{prefix_categories}/",
        json=fake_category_data,
    )
    assert response.status_code == 201
    category_id = response.json()["id"]

    response = await client.get(url=f"{prefix_categories}/category-id/{category_id}")
    assert response.status_code == 200
    fetched_category = response.json()

    assert fetched_category["id"] == category_id
    assert fetched_category["name"] == fake_category_data["name"]


@pytest.mark.anyio
async def test_update_category_by_id(
    client: AsyncClient,
    prefix_categories: str,
    fake_category_data: dict[str, Any],
):
    """
    Тест обновления категории по id, через API.
    """
    response = await client.post(
        url=f"{prefix_categories}/",
        json=fake_category_data,
    )
    assert response.status_code == 201
    category_id = response.json()["id"]

    update_data = {
        "name": f"Updated New Category",
        "description": "Обновлённое описание",
    }

    response = await client.patch(
        url=f"{prefix_categories}/{category_id}",
        json=update_data,
    )
    assert response.status_code == 200
    updated = response.json()

    assert updated["id"] == category_id
    assert updated["name"] == update_data["name"]
    assert updated["description"] == update_data["description"]


@pytest.mark.anyio
async def test_delete_category_by_id(
    client: AsyncClient,
    prefix_categories: str,
    fake_category_data: dict[str, Any],
):
    """
    Тест удаления категории по id, через API.
    """
    response = await client.post(
        url=f"{prefix_categories}/",
        json=fake_category_data,
    )
    assert response.status_code == 201
    category_id = response.json()["id"]

    response = await client.delete(url=f"{prefix_categories}/{category_id}")
    assert response.status_code == 204

    get_response = await client.get(
        url=f"{prefix_categories}/category-id/{category_id}"
    )
    assert get_response.status_code == 404

    delete_response = await client.delete(url=f"{prefix_categories}/{category_id}")
    assert delete_response.status_code == 404
