import pytest

from httpx import AsyncClient
from faker import Faker

from core.models.user import User
from core.models.products import Product
from core.config import settings


faker = Faker()


@pytest.fixture(scope="module")
def prefix_favorites() -> str:
    """Префикс для избранного."""
    return f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.favorites}/"


@pytest.mark.anyio
async def test_add_to_favorites(
    client: AsyncClient,
    prefix_favorites: str,
    test_user: User,
    test_product: Product,
):
    """
    Тест добавления в избранное.
    """
    response = await client.post(
        url=prefix_favorites,
        json={"user_id": test_user.id, "product_id": test_product.id},
    )
    assert response.status_code == 201
    data = response.json()

    assert data["user_id"] == test_user.id
    assert data["product_id"] == test_product.id


@pytest.mark.anyio
async def test_add_duplicate_favorite(
    client: AsyncClient,
    prefix_favorites: str,
    test_user: User,
    test_product: Product,
):
    """
    Тест добавления дубликата в избранное.
    """
    data = {
        "user_id": test_user.id,
        "product_id": test_product.id,
    }
    await client.post(
        url=prefix_favorites,
        json=data,
    )
    response = await client.post(
        url=prefix_favorites,
        json=data,
    )

    assert response.status_code == 400


@pytest.mark.anyio
async def test_get_favorites(
    client: AsyncClient,
    prefix_favorites: str,
    test_user: User,
    test_product: Product,
):
    """
    Тест получения избранного.
    """
    await client.post(
        url=prefix_favorites,
        json={"user_id": test_user.id, "product_id": test_product.id},
    )
    response = await client.get(
        url=prefix_favorites,
        params={"user_id": test_user.id},
    )

    assert response.status_code == 200
    assert len(response.json()["favorites"]) >= 1


@pytest.mark.anyio
async def test_delete_favorite(
    client: AsyncClient,
    prefix_favorites: str,
    test_user: User,
    test_product: Product,
):
    """
    Тест удаления из избранного.
    """
    resp = await client.post(
        url=prefix_favorites,
        json={"user_id": test_user.id, "product_id": test_product.id},
    )
    favorite_id = resp.json()["id"]

    response = await client.delete(
        url=prefix_favorites,
        params={"favorite_id": favorite_id},
    )
    assert response.status_code == 204
