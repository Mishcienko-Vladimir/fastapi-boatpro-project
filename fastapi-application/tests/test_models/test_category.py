import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models.products import Category


@pytest.mark.anyio
async def test_category_creation(test_category: Category):
    """
    Тест создания категории.
    """

    assert test_category.id is not None
    assert test_category.name is not None
    assert test_category.description is not None
    assert isinstance(test_category.name, str)
    assert isinstance(test_category.description, str)


@pytest.mark.anyio
async def test_category_relationship_products_empty(
    test_category: Category,
    test_session: AsyncSession,
):
    """
    Тест, что у новой категории нет товаров.
    """

    stmt = (
        select(Category)
        .options(selectinload(Category.products))
        .where(Category.id == test_category.id)
    )
    result = await test_session.execute(stmt)
    loaded_category = result.scalar_one()

    assert hasattr(
        loaded_category, "products"
    ), "Category должна иметь атрибут products"
    assert isinstance(loaded_category.products, list)
    assert len(loaded_category.products) == 0
