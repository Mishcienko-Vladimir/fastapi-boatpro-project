import pytest

from httpx import AsyncClient

from core.config import settings
from core.models.products import Category, OutboardMotor


@pytest.mark.anyio
async def test_admin_outboard_motors_page(
    superuser_client: AsyncClient,
    test_outboard_motor: OutboardMotor,
):
    """
    Тест страницы моторов в админке.
    """
    response = await superuser_client.get(
        url=f"{settings.view.admin}{settings.view.outboard_motors}/"
    )
    assert response.status_code == 200
    assert test_outboard_motor.name in response.text


@pytest.mark.anyio
async def test_admin_create_outboard_motor(
    superuser_client: AsyncClient,
    test_category: Category,
):
    """
    Тест создания мотора.
    """
    response = await superuser_client.post(
        url=f"{settings.view.admin}{settings.view.outboard_motors}/create-outboard-motor",
        data={
            "category_id": test_category.id,
            "name": "Новый Мотор",
            "price": 200000,
            "company_name": "MotorPro",
            "description": "Описание мотора",
            "is_active": "on",
            "engine_power": 150,
            "engine_type": "четырехтактный",
            "weight": 80,
            "number_cylinders": 6,
            "engine_displacement": 1800,
            "control_type": "дистанционное",
            "starter_type": "электрический",
        },
        files={"images": ("test_motor.jpg", b"file_content", "image/jpeg")},
    )
    assert response.status_code == 200
    assert "Прицеп с ID" in response.text
    assert "успешно создан" in response.text


@pytest.mark.anyio
async def test_admin_update_outboard_motor(
    superuser_client: AsyncClient,
    test_outboard_motor: OutboardMotor,
):
    """
    Тест обновления мотора.
    """
    response = await superuser_client.post(
        url=f"{settings.view.admin}{settings.view.outboard_motors}/update-outboard-motor",
        data={
            "outboard_motor_id_up": test_outboard_motor.id,
            "name": "Обновлённый Мотор",
            "price": 250000,
            "weight": 90,
        },
    )
    assert response.status_code == 200
    assert (
        f"Лодочный мотор с ID {test_outboard_motor.id} успешно обновлен"
        in response.text
    )


@pytest.mark.anyio
async def test_admin_delete_outboard_motor(
    superuser_client: AsyncClient,
    test_outboard_motor: OutboardMotor,
):
    """
    Тест удаления мотора.
    """
    response = await superuser_client.post(
        url=f"{settings.view.admin}{settings.view.outboard_motors}/delete-outboard-motor",
        data={"outboard_motor_id_del": test_outboard_motor.id},
    )
    assert response.status_code == 200
    assert (
        "успешно удален" in response.text or "missing from the folder" in response.text
    )
    list_response = await superuser_client.get(
        url=f"{settings.view.admin}{settings.view.outboard_motors}/"
    )
    assert test_outboard_motor.name not in list_response.text
