import pytest

from httpx import AsyncClient

from core.config import settings
from core.models.products import Boat


@pytest.mark.anyio
async def test_boats_page(
    client: AsyncClient,
    test_boat: Boat,
):
    """
    Тест страницы катеров.
    """
    response = await client.get(url=f"{settings.view.catalog}{settings.view.boats}/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Катера" in response.text


@pytest.mark.anyio
async def test_boat_detail_page(
    client: AsyncClient,
    test_boat: Boat,
):
    """
    Тест детальной страницы катера.
    """
    response = await client.get(
        url=f"{settings.view.catalog}{settings.view.boats}/{test_boat.name}"
    )

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert test_boat.name in response.text
