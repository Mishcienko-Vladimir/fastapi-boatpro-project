import pytest

from httpx import AsyncClient

from core.config import settings


@pytest.mark.anyio
async def test_home_page(client: AsyncClient):
    """
    Тест главной страницы.
    """
    response = await client.get(url=f"{settings.view.home}/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Главная" in response.text or "index" in response.text
