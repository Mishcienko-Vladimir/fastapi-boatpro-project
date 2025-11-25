import pytest

from typing import Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.products.category_service import CategoryService

from core.models.products import Category
from core.schemas.products import CategoryCreate, CategoryUpdate


@pytest.mark.anyio
async def test_create_category(
    test_session: AsyncSession,
    fake_category_data: dict[str, Any],
):
    """
    Тест создание категории, через сервис.
    """
    fake_category_data["name"] = "New Category"
    create_data = CategoryCreate(**fake_category_data)

    service = CategoryService(session=test_session)
    category = await service.create_category(category_data=create_data)

    assert category.id is not None
    assert category.name == "New Category"

    stmt = select(Category).where(Category.id == category.id)
    result = await test_session.execute(stmt)
    db_category = result.scalars().first()

    assert db_category is not None
    assert db_category.name == "New Category"


@pytest.mark.anyio
async def test_update_category(
    test_session: AsyncSession,
    test_category: Category,
):
    """
    Тест обновление категории, через сервис.
    """
    update_data = CategoryUpdate(
        name="Updated Category",
        description="New desc",
    )
    service = CategoryService(session=test_session)
    updated = await service.update_category_by_id(
        category_id=test_category.id,
        category_data=update_data,
    )

    assert updated.name == "Updated Category"
    assert updated.description == "New desc"

    stmt = select(Category).where(Category.id == test_category.id)
    result = await test_session.execute(stmt)
    db_category = result.scalars().first()
    assert db_category.name == "Updated Category"


@pytest.mark.anyio
async def test_delete_category(
    test_session: AsyncSession,
    test_category: Category,
):
    """
    Тест удаление категории, через сервис.
    """
    service = CategoryService(session=test_session)
    await service.delete_category_by_id(category_id=test_category.id)

    stmt = select(Category).where(Category.id == test_category.id)
    result = await test_session.execute(stmt)
    assert result.scalars().first() is None
