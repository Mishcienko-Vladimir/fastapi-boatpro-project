import pytest

from httpx import AsyncClient
from faker import Faker


faker = Faker()


@pytest.mark.anyio
async def test_create_trailer(
    client: AsyncClient,
    prefix_trailers: str,
    fake_trailer_data: dict,
    create_test_category,
    fake_images,
):
    """
    Тест создания прицепа.
    """
    response = await client.post(
        url=f"{prefix_trailers}/",
        data=fake_trailer_data,
        files=fake_images,
    )
    assert response.status_code == 201
    trailer = response.json()

    assert trailer["name"] == fake_trailer_data["name"]
    assert trailer["price"] == fake_trailer_data["price"]
    assert trailer["company_name"] == fake_trailer_data["company_name"]
    assert len(trailer["images"]) == len(fake_images)


@pytest.mark.anyio
async def test_get_trailer_by_id(
    client: AsyncClient,
    prefix_trailers: str,
    create_test_trailer: dict,
):
    """
    Тест получения прицепа по ID.
    """
    trailer_id = create_test_trailer["id"]
    response = await client.get(f"{prefix_trailers}/trailer-id/{trailer_id}")
    assert response.status_code == 200
    json = response.json()

    assert json["id"] == trailer_id
    assert json["name"] == create_test_trailer["name"]


@pytest.mark.anyio
async def test_get_trailer_by_name(
    client: AsyncClient,
    prefix_trailers: str,
    create_test_trailer: dict,
):
    """
    Тест получения прицепа по имени.
    """
    name = create_test_trailer["name"]
    response = await client.get(f"{prefix_trailers}/trailer-name/{name}")
    assert response.status_code == 200
    json = response.json()

    assert json["name"] == name
    assert json["id"] == create_test_trailer["id"]


@pytest.mark.anyio
async def test_get_all_trailers(
    client: AsyncClient,
    prefix_trailers: str,
    create_test_trailer: dict,
):
    """
    Тест получения всех прицепов.
    """
    response = await client.get(url=f"{prefix_trailers}/")
    assert response.status_code == 200
    trailers = response.json()

    assert isinstance(trailers, list)
    assert len(trailers) >= 1
    assert any(trailer["id"] == create_test_trailer["id"] for trailer in trailers)


@pytest.mark.anyio
async def test_get_trailers_summary(
    client: AsyncClient,
    prefix_trailers: str,
    create_test_trailer: dict,
):
    """
    Тест получения краткой информации о прицепах (с одним изображением).
    """
    response = await client.get(f"{prefix_trailers}/summary")
    assert response.status_code == 200
    summary_list = response.json()

    assert isinstance(summary_list, list)

    if len(summary_list) > 0:
        summary = summary_list[0]
        assert "name" in summary
        assert "price" in summary
        assert "image" in summary  # Должно быть одно изображение
        assert isinstance(summary["image"], dict) or summary["image"] is None


@pytest.mark.anyio
async def test_update_trailer_data(
    client: AsyncClient,
    prefix_trailers: str,
    create_test_trailer: dict,
):
    """
    Тест обновления данных прицепа (без изображений).
    """
    trailer_id = create_test_trailer["id"]
    update_data = {
        "price": 999999,
        "description": "Обновлённое описание прицепа",
        "is_active": False,
    }

    response = await client.patch(
        url=f"{prefix_trailers}/{trailer_id}",
        json=update_data,
    )
    assert response.status_code == 200
    updated = response.json()

    assert updated["id"] == trailer_id
    assert updated["price"] == update_data["price"]
    assert updated["description"] == update_data["description"]
    assert updated["is_active"] == update_data["is_active"]


@pytest.mark.anyio
async def test_update_trailer_images(
    client: AsyncClient,
    prefix_trailers: str,
    create_test_trailer: dict,
):
    """
    Тест обновления изображений прицепа: удаление и добавление.
    """
    trailer_id = create_test_trailer["id"]
    response = await client.get(f"{prefix_trailers}/trailer-id/{trailer_id}")
    assert response.status_code == 200
    initial_images = response.json()["images"]

    assert len(initial_images) >= 1
    image_to_remove_id = initial_images[0]["id"]  # ID первого изображения для удаления

    new_images = [
        ("add_images", ("new_img_1.jpg", b"newcontent1", "image/jpeg")),
        ("add_images", ("new_img_2.jpg", b"newcontent2", "image/jpeg")),
    ]

    response = await client.patch(
        url=f"{prefix_trailers}/images/{trailer_id}",
        data={"remove_images": str(image_to_remove_id)},
        files=new_images,
    )
    assert response.status_code == 200
    updated_images = response.json()["images"]
    assert image_to_remove_id not in [img["id"] for img in updated_images]

    # Проверка итогового количества: было N, 1 - удалили, 2 - добавили. Итого: N - 1 + 2
    assert len(updated_images) == len(initial_images) - 1 + 2


@pytest.mark.anyio
async def test_delete_trailer(
    client: AsyncClient,
    prefix_trailers: str,
    create_test_trailer: dict,
):
    """
    Тест удаления прицепа.
    """
    trailer_id = create_test_trailer["id"]

    response = await client.delete(f"{prefix_trailers}/{trailer_id}")
    assert response.status_code == 204, f"Ответ: {response.text}"

    get_response = await client.get(f"{prefix_trailers}/trailer-id/{trailer_id}")
    assert get_response.status_code == 404

    delete_response = await client.delete(f"{prefix_trailers}/{trailer_id}")
    assert delete_response.status_code == 404
