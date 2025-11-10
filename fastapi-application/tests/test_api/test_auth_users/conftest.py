import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker

from core.config import settings
from utils.limiter import limiter


faker = Faker()


@pytest.fixture(scope="module")
def prefix_auth():
    """Префикс для всех auth-роутеров."""
    return f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.auth}"


@pytest.fixture(scope="module")
def prefix_users():
    """Префикс для users-роутеров."""
    return f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.users}"


@pytest.fixture(scope="function")
def fake_user_data():
    """Генерация тестовых данных пользователя."""
    return {
        "email": faker.email(),
        "password": faker.password(),
        "first_name": faker.first_name(),
    }


@pytest.fixture(scope="function")
async def registered_user(
    client: AsyncClient,
    test_session: AsyncSession,
    prefix_auth: str,
    fake_user_data: dict,
):
    """Регистрирует пользователя и возвращает его данные."""
    response = await client.post(
        url=f"{prefix_auth}/register",
        json=fake_user_data,
    )
    assert response.status_code == 201
    return fake_user_data


@pytest.fixture(scope="function")
async def logged_in_client(
    client: AsyncClient,
    registered_user: dict,
    prefix_auth: str,
):
    """Возвращает клиент с активной сессией (кукой)."""
    response = await client.post(
        url=f"{prefix_auth}/login",
        data={
            "username": registered_user["email"],
            "password": registered_user["password"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 204
    assert "fastapiusersauth" in response.cookies
    return client


@pytest.fixture(autouse=True)
def reset_limiter():
    """Сбрасывает счётчики лимитов перед каждым тестом."""
    limiter.reset()
    yield
    limiter.reset()
