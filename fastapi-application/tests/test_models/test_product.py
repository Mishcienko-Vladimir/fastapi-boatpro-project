import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from datetime import datetime
from faker import Faker

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
    """Тест создания товара через fixture."""

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
    """Тест: товар привязан к категории."""
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
    """Тест: у нового товара нет изображений."""
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
    """Тест: у нового товара нет записей в избранном."""
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
async def test_product_unique_name_constraint(
    test_session: AsyncSession,
    test_category: Category,
):
    """Тест: имя товара должно быть уникальным."""
    name = f"Unique Product {faker.word()}"

    product1 = Product(
        name=name,
        price=100000,
        company_name="Test Co",
        category_id=test_category.id,
        description="First product",
    )
    test_session.add(product1)
    await test_session.commit()
    await test_session.refresh(product1)

    product2 = Product(
        name=name,
        price=120000,
        company_name="Another Co",
        category_id=test_category.id,
        description="Second product",
    )
    test_session.add(product2)

    with pytest.raises(Exception):
        await test_session.commit()
    await test_session.rollback()

    stmt = select(Product).where(Product.name == name)
    result = await test_session.execute(stmt)
    products = result.scalars().all()
    assert len(products) == 1


@pytest.mark.anyio
async def test_product_polymorphic_identity_outboard_motor(
    test_session: AsyncSession,
    test_category: Category,
):
    """Тест: OutboardMotor корректно устанавливает полиморфную метку."""
    motor = OutboardMotor(
        name=f"Motor {faker.word()}",
        price=faker.random_int(10000, 3000000),
        company_name=faker.company(),
        category_id=test_category.id,
        description=faker.text(),
        is_active=True,
        engine_power=faker.random_int(5, 200),
        engine_type=faker.random_element(elements=["двухтактный", "четырехтактный"]),
        weight=faker.random_int(20, 100),
        number_cylinders=faker.random_int(2, 6),
        engine_displacement=faker.random_int(200, 2000),
        control_type=faker.random_element(elements=["румпельное", "дистанционное"]),
        starter_type=faker.random_element(elements=["ручной", "электрический"]),
    )
    test_session.add(motor)
    await test_session.commit()
    await test_session.refresh(motor)

    assert motor.type_product == "outboard_motor"
    assert motor.__class__.__name__ == "OutboardMotor"


@pytest.mark.anyio
async def test_product_polymorphic_identity_trailer(
    test_session: AsyncSession,
    test_category: Category,
):
    """Тест: Trailer корректно устанавливает полиморфную метку."""
    trailer = Trailer(
        name=f"Trailer {faker.word()}",
        price=faker.random_int(10000, 3000000),
        company_name=faker.company(),
        category_id=test_category.id,
        description=faker.text(),
        is_active=True,
        full_mass=faker.random_int(500, 2000),
        load_capacity=faker.random_int(300, 1500),
        trailer_length=faker.random_int(400, 1000),
        max_ship_length=faker.random_int(300, 900),
    )
    test_session.add(trailer)
    await test_session.commit()
    await test_session.refresh(trailer)

    assert trailer.type_product == "trailer"
    assert trailer.__class__.__name__ == "Trailer"


@pytest.mark.anyio
async def test_product_polymorphic_identity_boat(
    test_session: AsyncSession,
    test_category: Category,
):
    """Тест: Boat корректно устанавливает полиморфную метку."""
    boat = Boat(
        name=f"Boat {faker.word()}",
        price=faker.random_int(10000, 3000000),
        company_name=faker.company(),
        category_id=test_category.id,
        description=faker.text(),
        is_active=True,
        length_hull=faker.random_int(300, 1000),
        width_hull=faker.random_int(100, 300),
        weight=faker.random_int(100, 500),
        capacity=faker.random_int(1, 6),
        maximum_load=faker.random_int(100, 1000),
        hull_material=faker.random_element(
            elements=["Aluminum", "Steel", "Fiberglass", "Tree"]
        ),
        thickness_side_sheet=faker.random_int(10, 1000),
        bottom_sheet_thickness=faker.random_int(10, 1000),
        fuel_capacity=faker.random_int(10, 1000),
        maximum_engine_power=faker.random_int(10, 1000),
        height_side_midship=faker.random_int(10, 1000),
        transom_height=faker.random_int(10, 1000),
    )
    test_session.add(boat)
    await test_session.commit()
    await test_session.refresh(boat)

    assert boat.type_product == "boat"
    assert boat.__class__.__name__ == "Boat"
