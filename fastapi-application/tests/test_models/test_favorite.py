import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models.user import User
from core.models.products import Product
from core.models.favorite import Favorite


@pytest.mark.anyio
async def test_favorite_creation(
    test_session: AsyncSession,
    test_user: User,
    test_product: Product,
):
    """
    Тест создания избранного.
    """
    favorite = Favorite(
        user_id=test_user.id,
        product_id=test_product.id,
    )
    test_session.add(favorite)
    await test_session.commit()
    await test_session.refresh(favorite)

    assert favorite.id is not None
    assert favorite.user_id == test_user.id
    assert favorite.product_id == test_product.id


@pytest.mark.anyio
async def test_favorite_relationships(
    test_session: AsyncSession,
    test_user: User,
    test_product: Product,
):
    """
    Тест обратных связей избранного.
    """
    favorite = Favorite(
        user_id=test_user.id,
        product_id=test_product.id,
    )
    test_session.add(favorite)
    await test_session.commit()
    await test_session.refresh(favorite)

    stmt = (
        select(User)
        .options(selectinload(User.favorites))
        .where(User.id == test_user.id)
    )
    result = await test_session.execute(stmt)
    loaded_user = result.scalar_one()

    stmt_product = (
        select(Product)
        .options(selectinload(Product.favorites))
        .where(Product.id == test_product.id)
    )
    result_product = await test_session.execute(stmt_product)
    loaded_product = result_product.scalar_one()

    assert len(loaded_user.favorites) == 1
    assert loaded_user.favorites[0].id == favorite.id

    assert len(loaded_product.favorites) == 1
    assert loaded_product.favorites[0].id == favorite.id
