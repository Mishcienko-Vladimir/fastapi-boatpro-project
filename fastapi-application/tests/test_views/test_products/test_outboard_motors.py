import pytest

from httpx import AsyncClient

from core.config import settings
from core.models.products import OutboardMotor


@pytest.mark.anyio
async def test_outboard_motors_page(
    client: AsyncClient,
    test_outboard_motor: OutboardMotor,
):
    """
    Тест страницы лодочных моторов.
    """
    response = await client.get(
        f"{settings.view.catalog}{settings.view.outboard_motors}/"
    )
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Лодочные моторы" in response.text


@pytest.mark.anyio
async def test_outboard_motor_detail_page(
    client: AsyncClient,
    test_outboard_motor: OutboardMotor,
):
    """
    Тест детальной страницы лодочного мотора.
    """
    response = await client.get(
        f"{settings.view.catalog}{settings.view.outboard_motors}/{test_outboard_motor.name}"
    )
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert test_outboard_motor.name in response.text
