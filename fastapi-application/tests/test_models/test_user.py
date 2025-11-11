import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models.user import User


@pytest.mark.anyio
async def test_user_creation(test_user: User):
    """Тест создания пользователя через fixture."""

    assert test_user.id is not None
    assert isinstance(test_user.email, str)
    assert "@" in test_user.email
    assert test_user.first_name is not None


@pytest.mark.anyio
async def test_user_relationship_favorites_empty(
    test_user: User,
    test_session: AsyncSession,
):
    """Тест: у нового пользователя нет избранного."""

    stmt = (
        select(User)
        .options(selectinload(User.favorites))
        .where(User.id == test_user.id)
    )
    result = await test_session.execute(stmt)
    loaded_user = result.scalar_one()

    assert hasattr(loaded_user, "favorites"), "User должен иметь атрибут favorites"
    assert isinstance(loaded_user.favorites, list)
    assert len(loaded_user.favorites) == 0
