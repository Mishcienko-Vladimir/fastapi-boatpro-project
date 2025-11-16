import pytest

from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker

from core.schemas.products import ProductBaseModelUpdate, ProductBaseModelCreate
from core.repositories.products.product_manager_crud import ProductManagerCrud
from core.models.products import Category, Product


faker = Faker()


@pytest.mark.anyio
async def test_create_product(
    test_session: AsyncSession,
    fake_product_data: dict[str, Any],
    test_category: Category,
):
    """
    Тест создания продукта, через репозиторий.
    """

    fake_product_data["name"] = "New Product"
    product_data = ProductBaseModelCreate(
        category_id=test_category.id,
        **fake_product_data,
    )

    repo = ProductManagerCrud(
        session=test_session,
        product_db=Product,
    )
    product = await repo.create_product(product_data=product_data)

    assert product.id is not None
    assert product.name == "New Product"


@pytest.mark.anyio
async def test_get_product_by_name(
    test_session: AsyncSession,
    test_product: Product,
):
    """
    Тест получения продукта по имени, через репозиторий.
    """
    repo = ProductManagerCrud(
        session=test_session,
        product_db=Product,
    )
    found = await repo.get_product_by_name(name=test_product.name)

    assert found is not None
    assert found.id == test_product.id


@pytest.mark.anyio
async def test_get_product_by_id(
    test_session: AsyncSession,
    test_product: Product,
):
    """
    Тест получения продукта по ID, через репозиторий.
    """
    repo = ProductManagerCrud(
        session=test_session,
        product_db=Product,
    )
    found = await repo.get_product_by_id(product_id=test_product.id)

    assert found is not None
    assert found.name == test_product.name


@pytest.mark.anyio
async def test_search_products(
    test_session: AsyncSession,
    test_product: Product,
):
    """
    Тест поиска продуктов, через репозиторий.
    """
    repo = ProductManagerCrud(
        session=test_session,
        product_db=Product,
    )
    results = await repo.get_search_products(query="Product")

    assert len(results) >= 1
    assert any(p.name == test_product.name for p in results)


@pytest.mark.anyio
async def test_get_all_products(
    test_session: AsyncSession,
    test_product: Product,
):
    """
    Тест получения всех продуктов, через репозиторий.
    """
    repo = ProductManagerCrud(
        session=test_session,
        product_db=Product,
    )
    products = await repo.get_all_products()

    assert len(products) >= 1
    assert any(p.id == test_product.id for p in products)


@pytest.mark.anyio
async def test_update_product_data(
    test_session: AsyncSession,
    test_product: Product,
):
    """
    Тест обновления данных продукта, через репозиторий.
    """
    update_data = ProductBaseModelUpdate(
        name="Updated Name",
        price=99999,
    )
    repo = ProductManagerCrud(
        session=test_session,
        product_db=Product,
    )
    updated = await repo.update_product_data(
        product=test_product,
        product_data=update_data,
    )

    assert updated.name == "Updated Name"
    assert updated.price == 99999


@pytest.mark.anyio
async def test_delete_product(
    test_session: AsyncSession,
    test_product: Product,
):
    """
    Тест удаления продукта, через репозиторий.
    """
    repo = ProductManagerCrud(
        session=test_session,
        product_db=Product,
    )

    result = await repo.delete_product(product=test_product)
    assert result is True

    found = await repo.get_product_by_id(product_id=test_product.id)
    assert found is None
