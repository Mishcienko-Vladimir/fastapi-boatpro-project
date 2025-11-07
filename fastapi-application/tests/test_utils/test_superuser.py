import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from actions.create_superuser import create_superuser_if_not_exists

from core.config import settings
from core.models import User


@pytest.mark.anyio
async def test_create_superuser_if_not_exists_creates_user(test_session: AsyncSession):
    """
    Тест создания суперпользователя.
    """

    # Проверка, что суперпользователя нет.
    result = await test_session.execute(
        select(User).where(User.email == settings.admin.admin_email)
    )
    user = result.scalar_one_or_none()
    assert user is None

    # Создания суперпользователя.
    user = await create_superuser_if_not_exists(test_session)
    assert user is not None
    assert user.email == settings.admin.admin_email
    assert user.is_superuser is True


@pytest.mark.anyio
async def test_create_superuser_if_not_exists_does_not_duplicate(
    test_session: AsyncSession,
):
    """
    Тест, что суперпользователь не создаётся повторно.
    """

    user1 = await create_superuser_if_not_exists(test_session)
    assert user1 is not None
    assert user1.email == settings.admin.admin_email

    result = await test_session.execute(
        select(User).where(User.email == settings.admin.admin_email)
    )
    user2 = result.scalar_one()
    assert user2.id == user1.id
    assert user2.is_superuser is True
