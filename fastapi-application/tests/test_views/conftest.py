import pytest

from fastapi import FastAPI
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from api import router as api_router

from core.dependencies import get_db_session
from core.models import User
from core.models.products import Product, Category
from core.repositories.authentication.fastapi_users import (
    current_active_superuser,
    optional_user,
)
from create_fastapi_app import create_app
from views import router as views_router


faker = Faker()


@pytest.fixture
async def test_user(test_session: AsyncSession) -> User:
    """
    Создаёт тестового пользователя.
    """
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


@pytest.fixture
async def test_category(test_session: AsyncSession) -> Category:
    """Создаёт тестовую категорию."""
    category = Category(
        name=f"Category {faker.uuid4()[:8]}",
        description=faker.text(),
    )
    test_session.add(category)
    await test_session.commit()
    await test_session.refresh(category)
    return category


@pytest.fixture
async def test_product(
    test_session: AsyncSession,
    test_category: Category,
) -> Product:
    """Создаёт тестовый товар."""
    product = Product(
        name=f"Product-{faker.uuid4()[:8]}",
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
def fastapi_app():
    """Создаёт приложение FastAPI для тестов."""
    app = create_app(create_custom_static_urls=True, enable_rate_limit=False)
    app.include_router(views_router)
    app.include_router(api_router)
    return app


@pytest.fixture
def base_client(fastapi_app: FastAPI, test_session: AsyncSession) -> AsyncClient:
    """Создаёт тестовый клиент с зависимостями."""

    def override_get_session():
        return test_session

    fastapi_app.dependency_overrides[get_db_session] = override_get_session
    transport = ASGITransport(app=fastapi_app)
    client = AsyncClient(transport=transport, base_url="http://test")
    return client


@pytest.fixture
async def client(
    base_client: AsyncClient, fastapi_app: FastAPI
) -> AsyncGenerator[AsyncClient, None]:
    """Клиент с чистыми overrides."""
    try:
        yield base_client
    finally:
        fastapi_app.dependency_overrides.clear()


@pytest.fixture
async def authenticated_client(
    base_client: AsyncClient,
    fastapi_app: FastAPI,
    test_user: User,
) -> AsyncGenerator[AsyncClient, None]:
    """Клиент с подменой optional_user."""

    def override_optional_user():
        return test_user

    fastapi_app.dependency_overrides[optional_user] = override_optional_user
    try:
        yield base_client
    finally:
        fastapi_app.dependency_overrides.clear()


@pytest.fixture
async def superuser_client(
    base_client: AsyncClient,
    fastapi_app: FastAPI,
    test_user: User,
) -> AsyncGenerator[AsyncClient, None]:
    """Клиент с правами суперпользователя."""

    def override_current_active_superuser():
        user = test_user
        user.is_superuser = True
        return user

    fastapi_app.dependency_overrides[current_active_superuser] = (
        override_current_active_superuser
    )
    try:
        yield base_client
    finally:
        fastapi_app.dependency_overrides.clear()
