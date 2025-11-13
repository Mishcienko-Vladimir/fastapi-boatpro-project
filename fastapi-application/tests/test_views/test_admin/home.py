import pytest

from httpx import AsyncClient

from core.config import settings
from core.models.products import Boat


@pytest.mark.anyio
async def test_admin_home_access_denied(
    client: AsyncClient,
    test_boat: Boat,
):
    """
    Анонимный пользователь не может зайти в админ-панель.
    """
    response = await client.get(url=f"{settings.view.admin}/")

    assert response.status_code == 307


@pytest.mark.anyio
async def test_admin_home_access_allowed(
    superuser_client: AsyncClient,
    test_boat: Boat,
):
    """
    Суперпользователь может зайти в админ-панель.
    """
    response = await superuser_client.get(url=f"{settings.view.admin}/")

    assert response.status_code == 200
    assert "Admin Panel" in response.text
