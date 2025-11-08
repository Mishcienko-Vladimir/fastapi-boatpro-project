import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker

from core.config import settings


faker = Faker()


@pytest.mark.anyio
async def test_register_and_login_flow(client: AsyncClient, test_session: AsyncSession):
    """
    Тестирование регистрации и логина.
    """

    email = faker.email()
    password = faker.password()
    first_name = faker.first_name()

    # /api/v1/auth
    prefix_auth = f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.auth}"

    # Регистрация
    response = await client.post(
        url=f"{prefix_auth}/register",
        json={
            "email": email,
            "password": password,
            "first_name": first_name,
        },
    )
    assert response.status_code == 201

    # Логин
    response = await client.post(
        url=f"{prefix_auth}/login",
        data={
            "username": email,
            "password": password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 204
    assert "fastapiusersauth" in response.cookies

    # Logout
    response = await client.post(url=f"{prefix_auth}/logout")
    assert response.status_code == 204
    # Проверяем, что кука удалена (или помечена как expired)
    assert "fastapiusersauth" not in response.cookies  # или проверяем Set-Cookie
