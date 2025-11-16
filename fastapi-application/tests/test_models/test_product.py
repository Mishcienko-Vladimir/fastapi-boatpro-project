import pytest

from typing import Any
from datetime import datetime
from faker import Faker

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models.products import (
    Category,
    Product,
    OutboardMotor,
    Trailer,
    Boat,
)


faker = Faker()


@pytest.mark.anyio
async def test_product_creation(test_product: Product):
    """
    Тест создания товара через fixture.
    """

    assert test_product.id is not None
    assert isinstance(test_product.name, str)
    assert len(test_product.name) > 0
    assert test_product.price > 0
    assert isinstance(test_product.company_name, str)
    assert len(test_product.company_name) > 0
    assert isinstance(test_product.description, str)
    assert len(test_product.description) > 0
    assert test_product.type_product == "product"
    assert test_product.is_active is True
    assert isinstance(test_product.created_at, datetime)
    assert isinstance(test_product.updated_at, datetime)


@pytest.mark.anyio
async def test_product_relationship_category(
    test_product: Product,
    test_session: AsyncSession,
):
    """
    Тест, что товар привязан к категории.
    """
    stmt = (
        select(Product)
        .options(selectinload(Product.category))
        .where(Product.id == test_product.id)
    )
    result = await test_session.execute(stmt)
    loaded_product = result.scalar_one()

    assert hasattr(loaded_product, "category"), "Product должен иметь атрибут category"
    assert loaded_product.category is not None
    assert loaded_product.category_id == loaded_product.category.id
    assert isinstance(loaded_product.category, Category)


@pytest.mark.anyio
async def test_product_relationship_images_empty(
    test_product: Product,
    test_session: AsyncSession,
):
    """
    Тест, что у нового товара нет изображений.
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


@pytest.mark.anyio
async def test_product_relationship_favorites_empty(
    test_product: Product,
    test_session: AsyncSession,
):
    """
    Тест, что у нового товара нет записей в избранном.
    """
    stmt = (
        select(Product)
        .options(selectinload(Product.favorites))
        .where(Product.id == test_product.id)
    )
    result = await test_session.execute(stmt)
    loaded_product = result.scalar_one()

    assert hasattr(
        loaded_product, "favorites"
    ), "Product должен иметь атрибут favorites"
    assert isinstance(loaded_product.favorites, list)
    assert len(loaded_product.favorites) == 0


@pytest.mark.anyio
async def test_product_polymorphic_identity_outboard_motor(
    test_session: AsyncSession,
    fake_outboard_motor_data: dict[str, Any],
    test_category: Category,
):
    """
    Тест: OutboardMotor корректно устанавливает полиморфную метку.
    """
    motor = OutboardMotor(
        category_id=test_category.id,
        **fake_outboard_motor_data,
    )
    test_session.add(motor)
    await test_session.commit()
    await test_session.refresh(motor)

    assert motor.type_product == "outboard_motor"
    assert motor.__class__.__name__ == "OutboardMotor"


@pytest.mark.anyio
async def test_product_polymorphic_identity_trailer(
    test_session: AsyncSession,
    fake_trailer_data: dict[str, Any],
    test_category: Category,
):
    """
    Тест: Trailer корректно устанавливает полиморфную метку.
    """
    trailer = Trailer(
        category_id=test_category.id,
        **fake_trailer_data,
    )
    test_session.add(trailer)
    await test_session.commit()
    await test_session.refresh(trailer)

    assert trailer.type_product == "trailer"
    assert trailer.__class__.__name__ == "Trailer"


@pytest.mark.anyio
async def test_product_polymorphic_identity_boat(
    test_session: AsyncSession,
    fake_boat_data: dict[str, Any],
    test_category: Category,
):
    """
    Тест: Boat корректно устанавливает полиморфную метку.
    """
    boat = Boat(
        category_id=test_category.id,
        **fake_boat_data,
    )
    test_session.add(boat)
    await test_session.commit()
    await test_session.refresh(boat)

    assert boat.type_product == "boat"
    assert boat.__class__.__name__ == "Boat"
