import pytest

from typing import Any
from httpx import AsyncClient

from core.models.products.category import Category


@pytest.mark.anyio
async def test_create_outboard_motor(
    client: AsyncClient,
    prefix_outboard_motors: str,
    fake_outboard_motor_data: dict[str, Any],
    test_category: Category,
    fake_images: list,
):
    """
    Тест создания лодочного мотора, через API.
    """
    fake_outboard_motor_data = fake_outboard_motor_data.copy()
    fake_outboard_motor_data["category_id"] = test_category.id

    response = await client.post(
        url=f"{prefix_outboard_motors}/",
        data=fake_outboard_motor_data,
        files=fake_images,
    )
    assert response.status_code == 201
    motor = response.json()

    assert motor["name"] == fake_outboard_motor_data["name"]
    assert motor["price"] == fake_outboard_motor_data["price"]
    assert motor["company_name"] == fake_outboard_motor_data["company_name"]
    assert len(motor["images"]) == len(fake_images)


@pytest.mark.anyio
async def test_get_outboard_motor_by_id(
    client: AsyncClient,
    prefix_outboard_motors: str,
    create_test_outboard_motor: dict[str, Any],
):
    """
    Тест получения лодочного мотора по ID, через API.
    """
    motor_id = create_test_outboard_motor["id"]
    response = await client.get(
        url=f"{prefix_outboard_motors}/outboard-motor-id/{motor_id}"
    )
    assert response.status_code == 200
    motor = response.json()

    assert motor["id"] == motor_id
    assert motor["name"] == create_test_outboard_motor["name"]


@pytest.mark.anyio
async def test_get_outboard_motor_by_name(
    client: AsyncClient,
    prefix_outboard_motors: str,
    create_test_outboard_motor: dict[str, Any],
):
    """
    Тест получения лодочного мотора по имени, через API.
    """
    name = create_test_outboard_motor["name"]
    response = await client.get(
        url=f"{prefix_outboard_motors}/outboard-motor-name/{name}"
    )
    assert response.status_code == 200
    motor = response.json()

    assert motor["name"] == name
    assert motor["id"] == create_test_outboard_motor["id"]


@pytest.mark.anyio
async def test_get_all_outboard_motors(
    client: AsyncClient,
    prefix_outboard_motors: str,
    create_test_outboard_motor: dict[str, Any],
):
    """
    Тест получения всех лодочных моторов, через API.
    """
    response = await client.get(url=f"{prefix_outboard_motors}/")
    assert response.status_code == 200
    motors = response.json()

    assert isinstance(motors, list)
    assert len(motors) >= 1
    assert any(motor["id"] == create_test_outboard_motor["id"] for motor in motors)


@pytest.mark.anyio
async def test_get_outboard_motors_summary(
    client: AsyncClient,
    prefix_outboard_motors: str,
    create_test_outboard_motor: dict[str, Any],
):
    """
    Тест получения краткой информации о лодочных моторах (с одним изображением), через API.
    """
    response = await client.get(url=f"{prefix_outboard_motors}/summary")
    assert response.status_code == 200
    summary_list_motors = response.json()

    assert isinstance(summary_list_motors, list)

    if len(summary_list_motors) > 0:
        summary = summary_list_motors[0]
        assert "name" in summary
        assert "price" in summary
        assert "image" in summary  # Должно быть одно изображение
        assert isinstance(summary["image"], dict) or summary["image"] is None


@pytest.mark.anyio
async def test_update_outboard_motor_data(
    client: AsyncClient,
    prefix_outboard_motors: str,
    create_test_outboard_motor: dict[str, Any],
):
    """
    Тест обновления данных лодочного мотора (без изображений), через API.
    """
    motor_id = create_test_outboard_motor["id"]
    update_data = {
        "price": 777777,
        "description": "Обновлённое описание мотора",
        "is_active": False,
    }

    response = await client.patch(
        url=f"{prefix_outboard_motors}/{motor_id}",
        json=update_data,
    )
    assert response.status_code == 200
    updated_motor = response.json()

    assert updated_motor["id"] == motor_id
    assert updated_motor["price"] == update_data["price"]
    assert updated_motor["description"] == update_data["description"]
    assert updated_motor["is_active"] == update_data["is_active"]


@pytest.mark.anyio
async def test_update_outboard_motor_images(
    client: AsyncClient,
    prefix_outboard_motors: str,
    create_test_outboard_motor: dict[str, Any],
):
    """
    Тест обновления изображений лодочного мотора: удаление и добавление, через API.
    """
    motor_id = create_test_outboard_motor["id"]
    response = await client.get(
        url=f"{prefix_outboard_motors}/outboard-motor-id/{motor_id}"
    )
    assert response.status_code == 200
    initial_images = response.json()["images"]

    assert len(initial_images) >= 1  # У мотора должно быть хотя бы одно изображение
    image_to_remove_id = initial_images[0]["id"]  # ID первого изображения для удаления

    new_images = [
        ("add_images", ("new_motor_img_1.jpg", b"newcontent1", "image/jpeg")),
        ("add_images", ("new_motor_img_2.jpg", b"newcontent2", "image/jpeg")),
    ]

    response = await client.patch(
        url=f"{prefix_outboard_motors}/images/{motor_id}",
        data={"remove_images": str(image_to_remove_id)},
        files=new_images,
    )
    assert response.status_code == 200
    updated_images = response.json()["images"]

    # Проверка итогового количества: было N, 1 - удалили, 2 - добавили. Итого: N - 1 + 2
    assert len(updated_images) == len(initial_images) - 1 + 2


@pytest.mark.anyio
async def test_delete_outboard_motor(
    client: AsyncClient,
    prefix_outboard_motors: str,
    create_test_outboard_motor: dict[str, Any],
):
    """
    Тест удаления лодочного мотора, через API.
    """
    motor_id = create_test_outboard_motor["id"]

    response = await client.delete(url=f"{prefix_outboard_motors}/{motor_id}")
    assert response.status_code == 204

    get_response = await client.get(
        url=f"{prefix_outboard_motors}/outboard-motor-id/{motor_id}"
    )
    assert get_response.status_code == 404

    delete_response = await client.delete(url=f"{prefix_outboard_motors}/{motor_id}")
    assert delete_response.status_code == 404
