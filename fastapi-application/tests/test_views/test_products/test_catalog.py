import pytest

from httpx import AsyncClient

from core.config import settings


@pytest.mark.anyio
async def test_catalog_page(client: AsyncClient):
    """
    Тест страницы каталога.
    """
    response = await client.get(url=f"{settings.view.catalog}/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "catalog" in response.text
