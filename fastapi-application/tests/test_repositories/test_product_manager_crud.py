import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker

from core.schemas.products import ProductBaseModelUpdate, ProductBaseModelCreate
from core.repositories.products.product_manager_crud import ProductManagerCrud
from core.models.products import Category, Product


faker = Faker()


@pytest.mark.anyio
async def test_create_product(
    test_session: AsyncSession,
    test_category: Category,
):
    """Тест создания продукта"""
    repo = ProductManagerCrud(
        test_session,
        Product,
    )

    product_data = ProductBaseModelCreate(
        name=f"New Product",
        price=faker.random_int(10000, 1000000),
        company_name=faker.company(),
        category_id=test_category.id,
        is_active=True,
        description=faker.text(),
    )
    product = await repo.create_product(product_data)

    assert product.id is not None
    assert product.name == "New Product"


@pytest.mark.anyio
async def test_get_product_by_name(
    test_session: AsyncSession,
    test_product: Product,
):
    """Тест получения продукта по имени"""
    repo = ProductManagerCrud(
        test_session,
        type(test_product),
    )
    found = await repo.get_product_by_name(test_product.name)

    assert found is not None
    assert found.id == test_product.id


@pytest.mark.anyio
async def test_get_product_by_id(
    test_session: AsyncSession,
    test_product: Product,
):
    """Тест получения продукта по ID"""
    repo = ProductManagerCrud(
        test_session,
        type(test_product),
    )
    found = await repo.get_product_by_id(test_product.id)

    assert found is not None
    assert found.name == test_product.name


@pytest.mark.anyio
async def test_search_products(
    test_session: AsyncSession,
    test_product: Product,
):
    """Тест поиска продуктов"""
    repo = ProductManagerCrud(
        test_session,
        type(test_product),
    )
    results = await repo.get_search_products("Product")

    assert len(results) >= 1
    assert any(p.name == test_product.name for p in results)


@pytest.mark.anyio
async def test_get_all_products(
    test_session: AsyncSession,
    test_product: Product,
):
    """Тест получения всех продуктов"""
    repo = ProductManagerCrud(
        test_session,
        type(test_product),
    )
    products = await repo.get_all_products()

    assert len(products) >= 1
    assert any(p.id == test_product.id for p in products)


@pytest.mark.anyio
async def test_update_product_data(
    test_session: AsyncSession,
    test_product: Product,
):
    """Тест обновления данных продукта"""
    repo = ProductManagerCrud(
        test_session,
        type(test_product),
    )
    update_data = ProductBaseModelUpdate(
        name="Updated Name",
        price=99999,
    )
    updated = await repo.update_product_data(
        test_product,
        update_data,
    )

    assert updated.name == "Updated Name"
    assert updated.price == 99999


@pytest.mark.anyio
async def test_delete_product(
    test_session: AsyncSession,
    test_product: Product,
):
    """Тест удаления продукта"""
    repo = ProductManagerCrud(
        test_session,
        type(test_product),
    )

    result = await repo.delete_product(test_product)
    assert result is True

    found = await repo.get_product_by_id(test_product.id)
    assert found is None
