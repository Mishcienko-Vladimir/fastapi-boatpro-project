import pytest

from httpx import AsyncClient


@pytest.mark.anyio
async def test_register_success(
    client: AsyncClient,
    prefix_auth: str,
    fake_user_data: dict,
):
    """Успешная регистрация."""
    response = await client.post(
        url=f"{prefix_auth}/register",
        json=fake_user_data,
    )
    assert response.status_code == 201
    json = response.json()
    assert json["email"] == fake_user_data["email"]
    assert "id" in json


@pytest.mark.anyio
async def test_register_duplicate_email(
    client: AsyncClient,
    prefix_auth: str,
    fake_user_data: dict,
):
    """Регистрация с уже существующим email."""

    # Первый раз — OK
    response = await client.post(
        url=f"{prefix_auth}/register",
        json=fake_user_data,
    )
    assert response.status_code == 201

    # Второй раз — ошибка
    response = await client.post(
        url=f"{prefix_auth}/register",
        json=fake_user_data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "REGISTER_USER_ALREADY_EXISTS"


@pytest.mark.anyio
async def test_register_invalid_email(
    client: AsyncClient,
    prefix_auth: str,
):
    """Регистрация с невалидным email."""
    response = await client.post(
        url=f"{prefix_auth}/register",
        json={
            "email": "invalid-email",
            "password": "password123",
            "first_name": "Test",
        },
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_register_missing_fields(
    client: AsyncClient,
    prefix_auth: str,
):
    """Регистрация без обязательных полей."""
    response = await client.post(
        url=f"{prefix_auth}/register",
        json={"email": "test@example.com"},
    )
    assert response.status_code == 422
