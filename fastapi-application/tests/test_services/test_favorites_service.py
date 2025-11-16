import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.favorites_service import FavoritesService

from core.schemas.favorite import FavoriteCreate
from core.models import Favorite, User
from core.models.products import Product


@pytest.mark.anyio
async def test_create_favorite(
    test_session: AsyncSession,
    test_user: User,
    test_product: Product,
):
    """
    Тест добавление в избранное, через сервис.
    """
    service = FavoritesService(session=test_session)
    favorite_data = FavoriteCreate(
        user_id=test_user.id,
        product_id=test_product.id,
    )
    favorite = await service.create_favorite(favorite_data=favorite_data)

    assert favorite.user_id == test_user.id
    assert favorite.product_id == test_product.id

    stmt = select(Favorite).where(
        Favorite.user_id == test_user.id,
        Favorite.product_id == test_product.id,
    )
    result = await test_session.execute(stmt)
    db_favorite = result.scalars().first()

    assert db_favorite is not None


@pytest.mark.anyio
async def test_get_favorites(
    test_session: AsyncSession,
    test_user: User,
    test_product: Product,
):
    """
    Тест получение избранных товаров, через сервис.
    """
    service = FavoritesService(session=test_session)
    favorite_data = FavoriteCreate(
        user_id=test_user.id,
        product_id=test_product.id,
    )
    await service.create_favorite(favorite_data=favorite_data)

    result = await service.get_favorites(user_id=test_user.id)

    assert len(result.favorites) >= 1
    assert result.favorites[0].product_id == test_product.id


@pytest.mark.anyio
async def test_delete_favorite(
    test_session: AsyncSession,
    test_user: User,
    test_product: Product,
):
    """
    Тест удаление из избранного, через сервис.
    """
    service = FavoritesService(session=test_session)
    favorite_data = FavoriteCreate(
        user_id=test_user.id,
        product_id=test_product.id,
    )
    favorite = await service.create_favorite(favorite_data=favorite_data)

    await service.delete_favorite_by_id(favorite_id=favorite.id)

    stmt = select(Favorite).where(Favorite.id == favorite.id)
    result = await test_session.execute(stmt)

    assert result.scalars().first() is None
