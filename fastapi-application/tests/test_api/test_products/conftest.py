import pytest

from typing import Any
from httpx import AsyncClient
from faker import Faker

from core.config import settings
from core.models.products.category import Category


faker = Faker()


@pytest.fixture(scope="module")
def prefix_boats() -> str:
    """Префикс для катеров."""
    return f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.products}{settings.api.v1.boats}"


@pytest.fixture(scope="module")
def prefix_outboard_motors() -> str:
    """Префикс для лодочных моторов."""
    return f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.products}{settings.api.v1.outboard_motors}"


@pytest.fixture(scope="module")
def prefix_trailers() -> str:
    """Префикс для прицепов."""
    return f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.products}{settings.api.v1.trailers}"


@pytest.fixture(scope="module")
def prefix_categories() -> str:
    """Префикс для категорий."""
    return f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.products}"


@pytest.fixture(scope="module")
def prefix_search() -> str:
    """Префикс для категорий."""
    return f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.search}/"


@pytest.fixture(scope="function")
def fake_images() -> list:
    """
    Возвращает список из рандомного количества фейкововых изображений.
    """
    fake_image = ("images", ("test_image.jpg", b"fakeimagecontent", "image/jpeg"))
    return [
        fake_image
        for _ in range(
            faker.random_int(1, 6),
        )
    ]


@pytest.fixture(scope="function")
async def create_test_boat(
    client: AsyncClient,
    prefix_boats: str,
    fake_boat_data: dict[str, Any],
    test_category: Category,
    fake_images: list,
) -> dict[str, Any]:
    """
    Создаёт тестовый катер через API.
    """
    fake_boat_data = fake_boat_data.copy()
    fake_boat_data["category_id"] = test_category.id

    response = await client.post(
        url=f"{prefix_boats}/",
        data=fake_boat_data,
        files=fake_images,
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture(scope="function")
async def create_test_outboard_motor(
    client: AsyncClient,
    prefix_outboard_motors: str,
    fake_outboard_motor_data: dict[str, Any],
    test_category: Category,
    fake_images: list,
) -> dict[str, Any]:
    """
    Создаёт тестовый лодочный мотор через API.
    """
    fake_outboard_motor_data = fake_outboard_motor_data.copy()
    fake_outboard_motor_data["category_id"] = test_category.id

    response = await client.post(
        url=f"{prefix_outboard_motors}/",
        data=fake_outboard_motor_data,
        files=fake_images,
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture(scope="function")
async def create_test_trailer(
    client: AsyncClient,
    prefix_trailers: str,
    fake_trailer_data: dict[str, Any],
    test_category: Category,
    fake_images: list,
) -> dict[str, Any]:
    """
    Создаёт тестовый прицеп через API.
    """
    fake_trailer_data = fake_trailer_data.copy()
    fake_trailer_data["category_id"] = test_category.id

    response = await client.post(
        url=f"{prefix_trailers}/",
        data=fake_trailer_data,
        files=fake_images,
    )
    assert response.status_code == 201
    return response.json()
