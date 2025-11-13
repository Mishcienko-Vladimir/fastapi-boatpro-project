import pytest

from httpx import AsyncClient

from core.config import settings


@pytest.mark.anyio
async def test_search_page(
    client: AsyncClient,
    test_product,
):
    """
    Тест страницы поиска.
    """
    response = await client.get(
        url=f"{settings.view.search}/",
        params={"query": test_product.name},
    )

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert test_product.name in response.text
