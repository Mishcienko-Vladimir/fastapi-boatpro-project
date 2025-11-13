import pytest

from httpx import AsyncClient

from core.config import settings
from core.models.products import Trailer


@pytest.mark.anyio
async def test_trailers_page(
    client: AsyncClient,
    test_trailer: Trailer,
):
    """
    Тест страницы прицепов.
    """
    response = await client.get(f"{settings.view.catalog}{settings.view.trailers}/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Прицепы" in response.text


@pytest.mark.anyio
async def test_trailer_detail_page(
    client: AsyncClient,
    test_trailer: Trailer,
):
    """
    Тест детальной страницы прицепа.
    """
    response = await client.get(
        f"{settings.view.catalog}{settings.view.trailers}/{test_trailer.name}"
    )
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert test_trailer.name in response.text
