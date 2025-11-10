import pytest

from httpx import AsyncClient


@pytest.mark.anyio
async def test_search_by_boat_name(
    client: AsyncClient,
    create_test_boat,
    prefix_search,
):
    """
    Тест поиска по названию катера.
    """
    boat = create_test_boat
    search_query = boat["name"]

    response = await client.get(
        url=prefix_search,
        params={"query": search_query},
    )
    assert response.status_code == 200
    results = response.json()

    assert isinstance(results, list)
    assert len(results) >= 1
    assert any(product["name"] == boat["name"] for product in results)


@pytest.mark.anyio
async def test_search_by_outboard_motor_company(
    client: AsyncClient,
    create_test_outboard_motor,
    prefix_search,
):
    """
    Тест поиска по названию компании лодочного мотора.
    """
    motor = create_test_outboard_motor
    search_query = motor["company_name"]

    response = await client.get(
        url=prefix_search,
        params={"query": search_query},
    )
    assert response.status_code == 200
    results = response.json()

    assert any(product["company_name"] == motor["company_name"] for product in results)


@pytest.mark.anyio
async def test_search_by_trailer_description_keyword(
    client: AsyncClient,
    create_test_trailer,
    prefix_search,
):
    """
    Тест поиска по ключевому слову из описания прицепа.
    """
    trailer = create_test_trailer
    keyword = trailer["description"].split()[0]  # первое слово

    response = await client.get(
        url=prefix_search,
        params={"query": keyword},
    )
    assert response.status_code == 200
    results = response.json()

    assert any(keyword.lower() in product["description"].lower() for product in results)


@pytest.mark.anyio
async def test_search_no_results(
    client: AsyncClient,
    prefix_search,
):
    """
    Тест поиска — нет совпадений.
    """
    response = await client.get(
        url=prefix_search,
        params={"query": "NonExistentProduct999"},
    )
    assert response.status_code == 200
    assert response.json() == []
