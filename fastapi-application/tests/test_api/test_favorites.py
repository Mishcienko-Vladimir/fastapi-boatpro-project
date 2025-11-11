import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker

from core.models.user import User
from core.models.products import Product, Category
from core.config import settings


faker = Faker()


def prefix_favorites():
    """Префикс для избранного."""
    return f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.favorites}/"


async def create_test_user(session):
    """Создание тестового пользователя."""
    user = User(
        email=faker.email(),
        hashed_password="fakehashed",
        first_name=faker.first_name(),
        is_active=True,
        is_superuser=False,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def create_test_category(session):
    """Создание тестовой категории."""
    category = Category(name=f"Category {faker.word()}", description=faker.text())
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


async def create_test_product(session, category_id):
    """Создание тестового продукта."""
    product = Product(
        name=f"Favorite {faker.word()}",
        price=faker.random_int(50000, 2000000),
        company_name=faker.company(),
        description=faker.text(),
        category_id=category_id,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@pytest.mark.anyio
async def test_add_to_favorites(
    client: AsyncClient,
    test_session: AsyncSession,
):
    """Тест добавления в избранное."""
    user = await create_test_user(test_session)
    category = await create_test_category(test_session)
    product = await create_test_product(test_session, category.id)

    response = await client.post(
        url=prefix_favorites(),
        json={"user_id": user.id, "product_id": product.id},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == user.id
    assert data["product_id"] == product.id


@pytest.mark.anyio
async def test_add_duplicate_favorite(
    client: AsyncClient,
    test_session: AsyncSession,
):
    """Тест добавления дубликата в избранное."""
    user = await create_test_user(test_session)
    category = await create_test_category(test_session)
    product = await create_test_product(test_session, category.id)

    data = {"user_id": user.id, "product_id": product.id}

    await client.post(
        url=prefix_favorites(),
        json=data,
    )
    response = await client.post(
        url=prefix_favorites(),
        json=data,
    )
    assert response.status_code == 400


@pytest.mark.anyio
async def test_get_favorites(
    client: AsyncClient,
    test_session: AsyncSession,
):
    """Тест получения избранного."""
    user = await create_test_user(test_session)
    category = await create_test_category(test_session)
    product = await create_test_product(test_session, category.id)

    await client.post(
        url=prefix_favorites(),
        json={"user_id": user.id, "product_id": product.id},
    )

    response = await client.get(
        url=prefix_favorites(),
        params={"user_id": user.id},
    )
    assert response.status_code == 201
    assert len(response.json()["favorites"]) >= 1


@pytest.mark.anyio
async def test_delete_favorite(
    client: AsyncClient,
    test_session: AsyncSession,
):
    """Тест удаления из избранного."""
    user = await create_test_user(test_session)
    category = await create_test_category(test_session)
    product = await create_test_product(test_session, category.id)

    resp = await client.post(
        url=prefix_favorites(),
        json={"user_id": user.id, "product_id": product.id},
    )
    favorite_id = resp.json()["id"]

    response = await client.delete(
        url=prefix_favorites(),
        params={"favorite_id": favorite_id},
    )
    assert response.status_code == 204
