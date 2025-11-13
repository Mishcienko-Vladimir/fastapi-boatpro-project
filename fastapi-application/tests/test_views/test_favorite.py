import pytest

from httpx import AsyncClient

from core.config import settings


@pytest.mark.anyio
async def test_favorites_page_unauthenticated(client: AsyncClient):
    """
    Тест: неавторизованный пользователь → просит залогиниться.
    """
    response = await client.get(url=f"{settings.view.favorites}/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "зайдите в свой аккаунт" in response.text or "log" in response.text


@pytest.mark.anyio
async def test_favorites_page_authenticated(authenticated_client: AsyncClient):
    """
    Тест: авторизованный пользователь → видит избранное.
    """
    response = await authenticated_client.get(url=f"{settings.view.favorites}/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "избранное" in response.text or "favorites" in response.text
