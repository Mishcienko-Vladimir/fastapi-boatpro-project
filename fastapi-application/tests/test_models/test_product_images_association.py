import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models.products import (
    Product,
    ProductImagesAssociation,
)


@pytest.mark.anyio
async def test_product_images_association_empty_for_new_product(
    test_product: Product,
    test_session: AsyncSession,
):
    """
    Тест, что у нового товара нет записей в ассоциативной таблице (нет изображений).
    """

    stmt = (
        select(Product)
        .options(selectinload(Product.images))
        .where(Product.id == test_product.id)
    )
    result = await test_session.execute(stmt)
    loaded_product = result.scalar_one()

    assert hasattr(loaded_product, "images"), "Product должен иметь атрибут images"
    assert isinstance(loaded_product.images, list)
    assert len(loaded_product.images) == 0

    # Проверка, что в ассоциативной таблице нет записей.
    assoc_stmt = select(ProductImagesAssociation).where(
        ProductImagesAssociation.product_id == test_product.id
    )
    assoc_result = await test_session.execute(assoc_stmt)
    associations = assoc_result.scalars().all()

    assert len(associations) == 0


@pytest.mark.anyio
async def test_product_images_association_empty_for_new_product(
    test_product: Product,
    test_session: AsyncSession,
):
    """
    Тест, что у нового товара нет записей в ассоциативной таблице (нет изображений).
    """

    stmt = (
        select(Product)
        .options(selectinload(Product.images))
        .where(Product.id == test_product.id)
    )
    result = await test_session.execute(stmt)
    loaded_product = result.scalar_one()

    assert hasattr(loaded_product, "images"), "Product должен иметь атрибут images"
    assert isinstance(loaded_product.images, list)
    assert len(loaded_product.images) == 0

    # Проверка, что в ассоциативной таблице нет записей для этого товара
    assoc_stmt = select(ProductImagesAssociation).where(
        ProductImagesAssociation.product_id == test_product.id
    )
    assoc_result = await test_session.execute(assoc_stmt)
    associations = assoc_result.scalars().all()

    assert len(associations) == 0
