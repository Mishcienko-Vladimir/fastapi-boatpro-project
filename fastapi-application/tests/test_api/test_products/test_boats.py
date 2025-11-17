import pytest

from typing import Any
from httpx import AsyncClient

from core.models.products.category import Category


@pytest.mark.anyio
async def test_create_boat(
    client: AsyncClient,
    prefix_boats: str,
    fake_boat_data: dict[str, Any],
    test_category: Category,
    fake_images: list,
):
    """
    Тест создания катера, через API.
    """
    fake_boat_data = fake_boat_data.copy()
    fake_boat_data["category_id"] = test_category.id

    response = await client.post(
        url=f"{prefix_boats}/",
        data=fake_boat_data,
        files=fake_images,
    )
    assert response.status_code == 201
    boat = response.json()

    assert boat["name"] == fake_boat_data["name"]
    assert boat["price"] == fake_boat_data["price"]
    assert boat["company_name"] == fake_boat_data["company_name"]
    assert len(boat["images"]) == len(fake_images)


@pytest.mark.anyio
async def test_get_boat_by_id(
    client: AsyncClient,
    prefix_boats: str,
    create_test_boat: dict[str, Any],
):
    """
    Тест получения катера по ID, через API.
    """
    boat_id = create_test_boat["id"]
    response = await client.get(url=f"{prefix_boats}/boat-id/{boat_id}")
    assert response.status_code == 200
    boat = response.json()

    assert boat["id"] == boat_id
    assert boat["name"] == create_test_boat["name"]


@pytest.mark.anyio
async def test_get_boat_by_name(
    client: AsyncClient,
    prefix_boats: str,
    create_test_boat: dict[str, Any],
):
    """
    Тест получения катера по имени, через API.
    """
    name = create_test_boat["name"]
    response = await client.get(url=f"{prefix_boats}/boat-name/{name}")
    assert response.status_code == 200
    boat = response.json()

    assert boat["name"] == name
    assert boat["id"] == create_test_boat["id"]


@pytest.mark.anyio
async def test_get_all_boats(
    client: AsyncClient,
    prefix_boats: str,
    create_test_boat: dict[str, Any],
):
    """
    Тест получения всех катеров, через API.
    """
    response = await client.get(url=f"{prefix_boats}/")
    assert response.status_code == 200
    boats = response.json()

    assert isinstance(boats, list)
    assert len(boats) >= 1
    assert any(boat["id"] == create_test_boat["id"] for boat in boats)


@pytest.mark.anyio
async def test_get_boats_summary(
    client: AsyncClient,
    prefix_boats: str,
    create_test_boat: dict[str, Any],
):
    """
    Тест получения краткой информации о катерах (с одним изображением), через API.
    """
    response = await client.get(url=f"{prefix_boats}/summary")
    assert response.status_code == 200
    summary_list_boats = response.json()

    assert isinstance(summary_list_boats, list)

    if len(summary_list_boats) > 0:
        summary = summary_list_boats[0]
        assert "name" in summary
        assert "price" in summary
        assert "image" in summary  # Должно быть одно изображение
        assert isinstance(summary["image"], dict) or summary["image"] is None


@pytest.mark.anyio
async def test_update_boat_data(
    client: AsyncClient,
    prefix_boats: str,
    create_test_boat: dict[str, Any],
):
    """
    Тест обновления данных катера (без изображений), через API.
    """
    boat_id = create_test_boat["id"]
    update_data = {
        "price": 888888,
        "description": "Обновлённое описание катера",
        "is_active": False,
    }

    response = await client.patch(
        url=f"{prefix_boats}/{boat_id}",
        json=update_data,
    )
    assert response.status_code == 200
    updated_boat = response.json()

    assert updated_boat["id"] == boat_id
    assert updated_boat["price"] == update_data["price"]
    assert updated_boat["description"] == update_data["description"]
    assert updated_boat["is_active"] == update_data["is_active"]


@pytest.mark.anyio
async def test_update_boat_images(
    client: AsyncClient,
    prefix_boats: str,
    create_test_boat: dict[str, Any],
):
    """
    Тест обновления изображений катера: удаление и добавление, через API.
    """
    boat_id = create_test_boat["id"]
    response = await client.get(url=f"{prefix_boats}/boat-id/{boat_id}")
    assert response.status_code == 200
    initial_images = response.json()["images"]

    assert len(initial_images) >= 1  # У катера должно быть хотя бы одно изображение
    image_to_remove_id = initial_images[0]["id"]  # ID первого изображения для удаления

    new_images = [
        ("add_images", ("new_boat_img_1.jpg", b"newcontent1", "image/jpeg")),
        ("add_images", ("new_boat_img_2.jpg", b"newcontent2", "image/jpeg")),
    ]

    response = await client.patch(
        url=f"{prefix_boats}/images/{boat_id}",
        data={"remove_images": str(image_to_remove_id)},
        files=new_images,
    )
    assert response.status_code == 200
    updated_images = response.json()["images"]

    # Проверка итогового количества: было N, 1 - удалили, 2 - добавили. Итого: N - 1 + 2
    assert len(updated_images) == len(initial_images) - 1 + 2


@pytest.mark.anyio
async def test_delete_boat(
    client: AsyncClient,
    prefix_boats: str,
    create_test_boat: dict[str, Any],
):
    """
    Тест удаления катера, через API.
    """
    boat_id = create_test_boat["id"]

    response = await client.delete(url=f"{prefix_boats}/{boat_id}")
    assert response.status_code == 204, f"Ответ: {response.text}"

    get_response = await client.get(url=f"{prefix_boats}/boat-id/{boat_id}")
    assert get_response.status_code == 404

    delete_response = await client.delete(url=f"{prefix_boats}/{boat_id}")
    assert delete_response.status_code == 404
