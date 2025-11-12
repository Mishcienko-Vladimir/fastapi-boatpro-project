import pytest
import uuid

from typing import Any
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.user import User
from core.models.products import Category, Product


faker = Faker()


@pytest.fixture(scope="function")
def fake_user_data() -> dict[str, Any]:
    """Генерация тестовых данных пользователя."""
    return {
        "email": faker.email(),
        "hashed_password": "fakehash",
        "first_name": faker.first_name(),
        "is_active": True,
        "is_superuser": False,
    }


@pytest.fixture(scope="function")
async def test_user(
    test_session: AsyncSession,
    fake_user_data: dict[str, Any],
) -> User:
    """Создаёт тестового пользователя в БД."""
    user = User(**fake_user_data)
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
        name=f"Product {uuid.uuid4().hex[:8]}",
        price=faker.random_int(10000, 1000000),
        company_name=faker.company(),
        category_id=test_category.id,
        description=faker.text(),
    )
    test_session.add(product)
    await test_session.commit()
    await test_session.refresh(product)
    return product
