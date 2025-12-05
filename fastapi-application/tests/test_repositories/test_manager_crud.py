import pytest

from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker

from core.schemas.products import ProductBaseModelUpdate, ProductBaseModelCreate
from core.repositories.manager_сrud import ManagerCrud
from core.models.products import Category, Product


faker = Faker()


@pytest.mark.anyio
async def test_create_product(
    test_session: AsyncSession,
    fake_product_data: dict[str, Any],
    test_category: Category,
):
    """
    Тест создания продукта, через универсальный репозиторий ManagerCrud.
    """

    fake_product_data["name"] = f"Product-{faker.uuid4()}"
    product_data = ProductBaseModelCreate(
        category_id=test_category.id,
        **fake_product_data,
    )

    repo = ManagerCrud(
        session=test_session,
        model_db=Product,
    )
    product = await repo.create(data=product_data)

    assert product.id is not None
    assert product.name == fake_product_data.get("name")


@pytest.mark.anyio
async def test_get_product_by_id(
    test_session: AsyncSession,
    test_product: Product,
):
    """
    Тест получения продукта по id, через универсальный репозиторий ManagerCrud.
    """
    repo = ManagerCrud(
        session=test_session,
        model_db=Product,
    )
    found = await repo.get_by_id(instance_id=test_product.id)

    assert found is not None
    assert found.name == test_product.name


@pytest.mark.anyio
async def test_get_all_products_by_field_with_relations(
    test_session: AsyncSession,
    fake_product_data: dict[str, Any],
    test_category: Category,
):
    """
    Тест получения продукта по полю field со значением value, с подгруженными связями.
    """
    fake_product_data["name"] = f"Product-{faker.uuid4()}"
    product = Product(
        category_id=test_category.id,
        **fake_product_data,
    )
    test_session.add(product)
    await test_session.commit()
    await test_session.refresh(product)

    repo = ManagerCrud(
        session=test_session,
        model_db=Product,
    )
    found_list = await repo.get_all_by_field_with_relations(
        "name",
        product.name,
        ("category", Category),
    )
    found = found_list[0] if found_list else None

    assert found is not None
    assert found.category.name == test_category.name
    assert found.category.description == test_category.description


@pytest.mark.anyio
async def test_get_all_product_by_field(
    test_session: AsyncSession,
    test_product: Product,
):
    """
    Тест получения продукта по полю field со значением value.
    """
    repo = ManagerCrud(
        session=test_session,
        model_db=Product,
    )
    found_list = await repo.get_all_by_field(
        field="name",
        value=test_product.name,
    )
    found = found_list[0] if found_list else None

    assert found is not None
    assert found.id == test_product.id
    assert found.name == test_product.name
    assert found.price == test_product.price


@pytest.mark.anyio
async def test_get_all_product_by_fields(
    test_session: AsyncSession,
    test_category: Category,
):
    """
    Тест получения продукта по нескольким полям field со значениями value.
    """
    product_one = Product(
        category_id=test_category.id,
        name=f"Product-{faker.uuid4()}",
        price=100000,
        company_name="Company",
        is_active=True,
        description=faker.text(),
    )
    product_two = Product(
        category_id=test_category.id,
        name=f"Product-{faker.uuid4()}",
        price=222222,
        company_name="Company",
        is_active=True,
        description=faker.text(),
    )
    test_session.add(product_one)
    test_session.add(product_two)
    await test_session.commit()

    repo = ManagerCrud(
        session=test_session,
        model_db=Product,
    )
    found_list = await repo.get_by_fields(
        company_name="Company",
        price=100000,
    )
    found = found_list[0] if found_list else None

    assert found_list is not None
    assert len(found_list) == 1
    assert found.company_name == "Company"
    assert found.price == 100000


@pytest.mark.anyio
async def test_get_all_products(
    test_session: AsyncSession,
    test_product: Product,
):
    """
    Тест получения всех продуктов, через универсальный репозиторий ManagerCrud.
    """
    repo = ManagerCrud(
        session=test_session,
        model_db=Product,
    )
    products = await repo.get_all()

    assert len(products) >= 1
    assert any(p.id == test_product.id for p in products)


@pytest.mark.anyio
async def test_update_product(
    test_session: AsyncSession,
    test_product: Product,
):
    """
    Тест обновления продукта, через универсальный репозиторий ManagerCrud.
    """
    update_data = ProductBaseModelUpdate(
        name=f"Updated-{faker.uuid4()}",
        price=99999,
    )
    repo = ManagerCrud(
        session=test_session,
        model_db=Product,
    )
    updated = await repo.update(
        instance=test_product,
        data=update_data,
    )

    assert updated.name == update_data.name
    assert updated.price == 99999


@pytest.mark.anyio
async def test_delete_product(
    test_session: AsyncSession,
    test_product: Product,
):
    """
    Тест удаления продукта, через универсальный репозиторий ManagerCrud.
    """
    repo = ManagerCrud(
        session=test_session,
        model_db=Product,
    )

    result = await repo.delete(instance=test_product)
    assert result is True

    found = await repo.get_by_id(instance_id=test_product.id)
    assert found is None
