import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.favorite import FavoriteCreate
from core.models.user import User
from core.models.products import Product
from core.repositories.favorite_manager_crud import FavoriteManagerCrud


@pytest.mark.anyio
async def test_create_favorite(
    test_session: AsyncSession,
    test_user: User,
    test_product: Product,
):
    """
    Тест создания избранного, через репозиторий.
    """
    repo = FavoriteManagerCrud(session=test_session)
    fav_data = FavoriteCreate(
        user_id=test_user.id,
        product_id=test_product.id,
    )
    favorite = await repo.create_favorite(favorite_data=fav_data)

    assert favorite.id is not None
    assert favorite.user_id == test_user.id
    assert favorite.product_id == test_product.id


@pytest.mark.anyio
async def test_is_favorite_exists(
    test_session: AsyncSession,
    test_user: User,
    test_product: Product,
):
    """
    Тест проверки существования избранного, через репозиторий.
    """
    repo = FavoriteManagerCrud(session=test_session)
    fav_data = FavoriteCreate(
        user_id=test_user.id,
        product_id=test_product.id,
    )
    await repo.create_favorite(favorite_data=fav_data)
    exists = await repo.is_favorite_exists(
        user_id=test_user.id,
        product_id=test_product.id,
    )

    assert exists is True


@pytest.mark.anyio
async def test_get_favorites_user(
    test_session: AsyncSession,
    test_user: User,
    test_product: Product,
):
    """
    Тест получения избранных товаров пользователя, через репозиторий.
    """
    repo = FavoriteManagerCrud(session=test_session)
    fav_data = FavoriteCreate(
        user_id=test_user.id,
        product_id=test_product.id,
    )
    await repo.create_favorite(favorite_data=fav_data)
    favorites = await repo.get_favorites_user(user_id=test_user.id)

    assert len(favorites) == 1
    assert favorites[0].product_id == test_product.id
