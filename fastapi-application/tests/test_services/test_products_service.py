import pytest

from typing import Any
from faker import Faker
from fastapi import UploadFile

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.products.products_service import ProductsService

from core.schemas.products.boat import BoatCreate, BoatUpdate
from core.models.products import Boat, Category


faker = Faker()


@pytest.mark.anyio
async def test_create_product_success(
    test_session: AsyncSession,
    test_category: Category,
    mock_upload_file: UploadFile,
    fake_boat_data: dict[str, Any],
):
    """Тест создание товара."""
    create_data = BoatCreate(
        name="Test Boat",
        price=50000,
        category_id=test_category.id,
        **fake_boat_data,
    )

    service = ProductsService(test_session, Boat)
    product = await service.create_product(create_data, [mock_upload_file])

    assert product.id is not None
    assert product.name == "Test Boat"
    assert len(product.images) == 1

    stmt = select(Boat).where(Boat.id == product.id)
    result = await test_session.execute(stmt)
    db_product = result.scalars().first()

    assert db_product is not None
    assert db_product.price == 50000


@pytest.mark.anyio
async def test_update_product_data_by_id(
    test_session: AsyncSession,
    test_category: Category,
    fake_boat_data: dict[str, Any],
):
    """
    Тест обновление данных товара.
    """
    boat = Boat(
        name="Old Name",
        price=10000,
        category_id=test_category.id,
        **fake_boat_data,
    )
    test_session.add(boat)
    await test_session.commit()
    await test_session.refresh(boat)

    service = ProductsService(test_session, Boat)
    new_boat_data = {"name": "Updated Boat", "price": 99999}

    updated = await service.update_product_data_by_id(
        boat.id,
        BoatUpdate(**new_boat_data),
    )

    assert updated.name == "Updated Boat"
    assert updated.price == 99999

    stmt = select(Boat).where(Boat.id == boat.id)
    result = await test_session.execute(stmt)
    db_boat = result.scalars().first()

    assert db_boat.name == "Updated Boat"


@pytest.mark.anyio
async def test_delete_product_by_id(
    test_session: AsyncSession,
    test_category: Category,
    mock_upload_file: UploadFile,
    fake_boat_data: dict[str, Any],
):
    """
    Тест удаление товара.
    """
    boat = Boat(
        name="Old Name",
        price=10000,
        category_id=test_category.id,
        **fake_boat_data,
    )
    test_session.add(boat)
    await test_session.commit()
    await test_session.refresh(boat)

    service = ProductsService(test_session, Boat)
    updated_boat = await service.update_product_images_by_id(
        product_id=boat.id,
        remove_images=None,
        add_images=[mock_upload_file],
    )

    await service.delete_product_by_id(updated_boat.id)

    stmt = select(Boat).where(Boat.id == updated_boat.id)
    result = await test_session.execute(stmt)

    assert result.scalars().first() is None
