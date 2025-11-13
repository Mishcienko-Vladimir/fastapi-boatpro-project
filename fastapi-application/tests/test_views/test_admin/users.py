import pytest

from httpx import AsyncClient

from core.config import settings
from core.models import User


@pytest.mark.anyio
async def test_admin_users_page(
    superuser_client: AsyncClient,
    test_user: User,
):
    """
    Тест страницы пользователей в админке.
    """
    response = await superuser_client.get(
        url=f"{settings.view.admin}{settings.view.users}/"
    )
    assert response.status_code == 200
    assert test_user.email in response.text


@pytest.mark.anyio
async def test_admin_delete_user(
    superuser_client: AsyncClient,
    test_user: User,
):
    """
    Тест удаления пользователя.
    """
    response = await superuser_client.post(
        url=f"{settings.view.admin}{settings.view.users}/delete-user",
        data={"user_id_del": test_user.id},
    )
    assert response.status_code == 200
    assert f"Пользователь с ID {test_user.id} успешно удалён." in response.text
