import asyncio
import pytest

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.models import Base
from main import main_app
from core.models.db_helper import db_helper


# Тестовая БД в памяти
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """
    Создает событийный цикл для тестов.
    Этот fixture нужен для корректной работы тестов с asyncio.
    """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


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


@pytest.fixture(scope="function")
async def client(test_session):
    """
    Создает тестовый клиент для тестирования API.
    """

    def override_get_session():
        """Заменяет реальную сессию на тестовую."""
        return test_session

    app = main_app
    app.dependency_overrides[db_helper.get_scoped_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
