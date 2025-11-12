import pytest
import uuid

from io import BytesIO
from typing import Any
from fastapi import UploadFile
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import Headers

from core.models.user import User
from core.models.products import Category, Product


faker = Faker()


@pytest.fixture(scope="function")
def fake_boat_data() -> dict[str, Any]:
    """Создаёт тестовые данные для катера, кроме полей: name и price."""
    return {
        "company_name": faker.company()[:100],
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
async def test_user(
    test_session: AsyncSession,
) -> User:
    """Создаёт тестового пользователя в БД."""
    user = User(
        email=faker.email(),
        hashed_password="fakehash",
        first_name=faker.first_name(),
        is_active=True,
        is_superuser=False,
    )
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    return user


@pytest.fixture(scope="function")
async def test_category(
    test_session: AsyncSession,
) -> Category:
    """Создаёт тестовую категорию."""
    category = Category(
        name=f"Category {uuid.uuid4().hex[:8]}",
        description=faker.text(),
    )
    test_session.add(category)
    await test_session.commit()
    await test_session.refresh(category)
    return category


@pytest.fixture(scope="function")
async def test_product(
    test_session: AsyncSession,
    test_category: Category,
) -> Product:
    """Создаёт тестовый товар."""
    product = Product(
        name=f"Product-{uuid.uuid4().hex[:8]}",
        price=faker.random_int(10000, 1000000),
        company_name=faker.company(),
        category_id=test_category.id,
        description=faker.text(),
    )
    test_session.add(product)
    await test_session.commit()
    await test_session.refresh(product)
    return product


@pytest.fixture
def mock_upload_file() -> UploadFile:
    """
    Создаёт реалистичный UploadFile для тестов.
    Использует BytesIO для имитации загруженного файла.
    """
    file = UploadFile(
        filename="test_image.jpg",
        file=BytesIO(b"fake image content"),
        headers=Headers({"content-type": "image/jpeg"}),
    )
    return file
