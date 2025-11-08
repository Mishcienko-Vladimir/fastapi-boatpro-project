# Запуск тестов: python -m pytest fastapi-application/tests/ -v
import pytest

from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncIterator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.dependencies import get_db_session
from core.models import Base
from create_fastapi_app import create_app


# Тестовая БД в памяти
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def anyio_backend():
    """
    Фикстура, указывающая, какой асинхронный движок использовать (asyncio или trio)
    """
    return "asyncio"


@pytest.fixture(scope="session")
async def test_engine():
    """
    Создает тестовую БД и мигрирует модели в нее.
    """
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def test_session(test_engine):
    """
    Создает сессию для тестовой БД.
    :return: - откат изменений после каждого теста.
    """
    async_session = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session
        await session.rollback()


@asynccontextmanager
async def empty_lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Пустой lifespan для тестов."""
    yield


@pytest.fixture(scope="function")
async def client(test_session):
    """
    Создает тестовый клиент для тестирования API.
    """

    def override_get_session():
        """Заменяет реальную сессию на тестовую."""
        return test_session

    app: FastAPI = create_app(
        create_custom_static_urls=True, lifespan_override=empty_lifespan
    )
    app.dependency_overrides[get_db_session] = override_get_session  # type: ignore

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()  # type: ignore
