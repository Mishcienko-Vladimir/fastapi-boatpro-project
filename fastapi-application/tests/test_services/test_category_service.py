import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.products.category import CategoryService

from core.models.products import Category
from core.schemas.products import CategoryCreate, CategoryUpdate


@pytest.mark.anyio
async def test_create_category(test_session: AsyncSession):
    """
    Тест создание категории.
    """
    service = CategoryService(test_session)
    create_data = CategoryCreate(
        name="New Category",
        description="Test",
    )

    category = await service.create_category(create_data)

    assert category.id is not None
    assert category.name == "New Category"

    stmt = select(Category).where(Category.id == category.id)
    result = await test_session.execute(stmt)
    db_category = result.scalars().first()

    assert db_category is not None
    assert db_category.name == "New Category"


@pytest.mark.anyio
async def test_update_category(test_session: AsyncSession):
    """
    Тест обновление категории.
    """

    category = Category(
        name="Old Category",
        description="Old",
    )
    test_session.add(category)
    await test_session.commit()
    await test_session.refresh(category)

    service = CategoryService(test_session)
    update_data = CategoryUpdate(name="Updated Category", description="New desc,")
    updated = await service.update_category_by_id(
        category.id,
        update_data,
    )

    assert updated.name == "Updated Category"

    stmt = select(Category).where(Category.id == category.id)
    result = await test_session.execute(stmt)
    db_category = result.scalars().first()
    assert db_category.name == "Updated Category"


@pytest.mark.anyio
async def test_delete_category(test_session: AsyncSession):
    """
    Тест удаление категории.
    """
    category = Category(
        name="To Delete",
        description="Delete me",
    )
    test_session.add(category)
    await test_session.commit()
    await test_session.refresh(category)

    service = CategoryService(test_session)
    await service.delete_category_by_id(category.id)

    stmt = select(Category).where(Category.id == category.id)
    result = await test_session.execute(stmt)
    assert result.scalars().first() is None
