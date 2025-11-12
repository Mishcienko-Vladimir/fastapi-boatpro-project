import pytest

from httpx import AsyncClient


@pytest.mark.anyio
async def test_home_page(client: AsyncClient):
    """
    Тест главной страницы.
    """
    response = await client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Главная" in response.text or "index" in response.text


@pytest.mark.anyio
async def test_catalog_page(client: AsyncClient):
    """
    Тест страницы каталога.
    """
    response = await client.get("/catalog/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "catalog" in response.text


@pytest.mark.anyio
async def test_search_page(
    client: AsyncClient,
    test_product,
):
    """
    Тест страницы поиска.
    """
    response = await client.get("/search/", params={"query": test_product.name})

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert test_product.name in response.text


@pytest.mark.anyio
async def test_favorites_page_unauthenticated(client: AsyncClient):
    """
    Тест: неавторизованный пользователь → просит залогиниться.
    """
    response = await client.get("/favorites/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "зайдите в свой аккаунт" in response.text or "log" in response.text


@pytest.mark.anyio
async def test_favorites_page_authenticated(authenticated_client: AsyncClient):
    """
    Тест: авторизованный пользователь → видит избранное.
    """
    response = await authenticated_client.get("/favorites/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "избранное" in response.text or "favorites" in response.text
