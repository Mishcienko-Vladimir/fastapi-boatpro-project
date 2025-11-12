import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from core.models.user import User
from core.repositories.user_manager_crud import UserManagerCrud


@pytest.mark.anyio
async def test_get_all_users(
    test_session: AsyncSession,
    test_user: User,
):
    """
    Тест получения всех пользователей.
    """
    repo = UserManagerCrud(test_session)
    users = await repo.get_all_users()

    assert len(users) >= 1
    assert any(user.id == test_user.id for user in users)


@pytest.mark.anyio
async def test_get_user_by_id(
    test_session: AsyncSession,
    test_user: User,
):
    """
    Тест получения пользователя по ID.
    """
    repo = UserManagerCrud(test_session)
    user = await repo.get_user_by_id(test_user.id)

    assert user is not None
    assert user.id == test_user.id
    assert user.email == test_user.email


@pytest.mark.anyio
async def test_get_user_by_id_not_found(
    test_session: AsyncSession,
):
    """
    Тест получения несуществующего пользователя.
    """
    repo = UserManagerCrud(test_session)
    user = await repo.get_user_by_id(999)

    assert user is None


@pytest.mark.anyio
async def test_delete_user(
    test_session: AsyncSession,
    test_user: User,
):
    """
    Тест удаления пользователя по ID.
    """
    repo = UserManagerCrud(test_session)
    deleted_user = await repo.delete_user(test_user.id)

    assert deleted_user is not None
    assert deleted_user.id == test_user.id

    user_in_db = await repo.get_user_by_id(test_user.id)
    assert user_in_db is None


@pytest.mark.anyio
async def test_delete_user_not_found(
    test_session: AsyncSession,
):
    """
    Тест удаления несуществующего пользователя.
    """
    repo = UserManagerCrud(test_session)
    deleted_user = await repo.delete_user(999)

    assert deleted_user is None
