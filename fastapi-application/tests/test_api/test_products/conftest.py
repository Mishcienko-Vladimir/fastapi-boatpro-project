import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker

from core.config import settings
from core.models.products.category import Category


faker = Faker()


@pytest.fixture(scope="module")
def prefix_boats():
    """Префикс для катеров."""
    return f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.boats}"


@pytest.fixture(scope="module")
def prefix_outboard_motors():
    """Префикс для лодочных моторов."""
    return f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.outboard_motors}"


@pytest.fixture(scope="module")
def prefix_trailers():
    """Префикс для прицепов."""
    return f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.trailers}"


@pytest.fixture(scope="module")
def prefix_categories():
    """Префикс для категорий."""
    return f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.products}"


@pytest.fixture(scope="function")
def fake_images():
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
def fake_boat_data():
    """Создаёт тестовые данные для катера."""
    return {
        "category_id": 1,
        "name": faker.word().title(),
        "price": faker.random_int(10000, 1000000),
        "company_name": faker.company(),
        "description": faker.text(),
        "is_active": True,
        "length_hull": faker.random_int(300, 1000),
        "width_hull": faker.random_int(100, 300),
        "weight": faker.random_int(100, 500),
        "capacity": faker.random_int(1, 6),
        "maximum_load": faker.random_int(100, 1000),
        "hull_material": faker.random_element(
            elements=["Aluminum", "Steel", "Fiberglass", "Tree"]
        ),
        "thickness_side_sheet": faker.random_int(10, 1000),
        "bottom_sheet_thickness": faker.random_int(10, 1000),
        "fuel_capacity": faker.random_int(10, 1000),
        "maximum_engine_power": faker.random_int(10, 1000),
        "height_side_midship": faker.random_int(10, 1000),
        "transom_height": faker.random_int(10, 1000),
    }


@pytest.fixture(scope="function")
def fake_outboard_motor_data():
    """Создаёт тестовые данные для мотора."""
    return {
        "category_id": 1,
        "name": f"Motor {faker.word()}",
        "price": faker.random_int(10000, 3000000),
        "company_name": faker.company(),
        "description": faker.text(),
        "is_active": True,
        "engine_power": faker.random_int(5, 200),
        "engine_type": faker.random_element(elements=["двухтактный", "четырехтактный"]),
        "weight": faker.random_int(20, 100),
        "number_cylinders": faker.random_int(2, 6),
        "engine_displacement": faker.random_int(200, 2000),
        "control_type": faker.random_element(elements=["румпельное", "дистанционное"]),
        "starter_type": faker.random_element(elements=["ручной", "электрический"]),
    }


@pytest.fixture(scope="function")
def fake_trailer_data():
    """Создаёт тестовые данные для прицепа."""
    return {
        "category_id": 1,
        "name": f"Trailer {faker.word()}",
        "price": faker.random_int(30000, 300000),
        "company_name": faker.company(),
        "description": faker.text(),
        "is_active": True,
        "full_mass": faker.random_int(500, 2000),
        "load_capacity": faker.random_int(300, 1500),
        "trailer_length": faker.random_int(400, 1000),
        "max_ship_length": faker.random_int(300, 900),
    }


@pytest.fixture(scope="function")
def fake_category_data():
    """Создаёт тестовые данные для категории."""
    return {
        "name": f"Category {faker.word()}",
        "description": faker.text(),
    }


@pytest.fixture(scope="function")
async def create_test_category(
    test_session: AsyncSession,
    fake_category_data: dict,
):
    """Создаёт тестовую категорию."""
    category = Category(**fake_category_data)
    test_session.add(category)
    await test_session.commit()
    await test_session.refresh(category)
    return category


@pytest.fixture(scope="function")
async def create_test_boat(
    client: AsyncClient,
    prefix_boats: str,
    fake_boat_data: dict,
    create_test_category,
    fake_images,
):
    """
    Создаёт тестовый катер через API.
    """
    response = await client.post(
        url=prefix_boats,
        data=fake_boat_data,
        files=fake_images,
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture(scope="function")
async def create_test_outboard_motor(
    client: AsyncClient,
    prefix_outboard_motors: str,
    fake_outboard_motor_data: dict,
    create_test_category,
    fake_images,
):
    """
    Создаёт тестовый лодочный мотор через API.
    """
    response = await client.post(
        url=prefix_outboard_motors,
        data=fake_outboard_motor_data,
        files=fake_images,
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture(scope="function")
async def create_test_trailer(
    client: AsyncClient,
    prefix_trailers: str,
    fake_trailer_data: dict,
    create_test_category,
    fake_images,
):
    """
    Создаёт тестовый прицеп через API.
    """
    response = await client.post(
        url=prefix_trailers,
        data=fake_trailer_data,
        files=fake_images,
    )
    assert response.status_code == 201
    return response.json()
