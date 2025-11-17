import pytest

from typing import Any
from httpx import AsyncClient


@pytest.mark.anyio
async def test_search_by_boat_name(
    client: AsyncClient,
    create_test_boat: dict[str, Any],
    prefix_search: str,
):
    """
    Тест поиска по названию катера, через API.
    """
    response = await client.get(
        url=prefix_search,
        params={"query": create_test_boat["name"]},
    )
    assert response.status_code == 200
    results = response.json()

    assert isinstance(results, list)
    assert len(results) >= 1
    assert any(product["name"] == create_test_boat["name"] for product in results)


@pytest.mark.anyio
async def test_search_by_outboard_motor_company(
    client: AsyncClient,
    create_test_outboard_motor: dict[str, Any],
    prefix_search: str,
):
    """
    Тест поиска по названию компании лодочного мотора, через API.
    """
    response = await client.get(
        url=prefix_search,
        params={"query": create_test_outboard_motor["company_name"]},
    )
    assert response.status_code == 200
    results = response.json()

    assert any(
        product["company_name"] == create_test_outboard_motor["company_name"]
        for product in results
    )


@pytest.mark.anyio
async def test_search_by_trailer_description_keyword(
    client: AsyncClient,
    create_test_trailer: dict[str, Any],
    prefix_search: str,
):
    """
    Тест поиска по ключевому слову из описания прицепа, через API.
    """
    keyword = create_test_trailer["description"].split()[0]  # первое слово

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
    prefix_search: str,
):
    """
    Тест поиска — нет совпадений, через API.
    """
    response = await client.get(
        url=prefix_search,
        params={"query": "NonExistentProduct999"},
    )
    assert response.status_code == 200
    assert response.json() == []
