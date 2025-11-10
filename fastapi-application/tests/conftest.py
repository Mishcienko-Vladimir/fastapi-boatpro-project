# Запуск тестов: python -m pytest fastapi-application/tests/ -v
import pytest
import shutil

from fastapi import FastAPI
from fastapi_cache.coder import JsonCoder
from fastapi_cache.backends.inmemory import InMemoryBackend

from contextlib import asynccontextmanager
from typing import AsyncIterator
from httpx import AsyncClient, ASGITransport
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from core.dependencies import get_db_session
from core.models import Base
from core.config import settings, BASE_DIR

from api import router as api_router
from views import router as views_router
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
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=StaticPool,
    )
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
        autoflush=False,
        autocommit=False,
    )
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture(autouse=True)
def mock_image_upload_dir(monkeypatch):
    """
    Подменяет computed field в image_upload_dir на тестовый путь.
    Во время тестов создается тестовая папка для изображений. В конце теста она удаляется.
    """
    test_images_path = Path(BASE_DIR / "static" / "test_images")
    if test_images_path.exists():
        shutil.rmtree(test_images_path)
    test_images_path.mkdir(exist_ok=True)

    test_config = {
        "base_dir": str(BASE_DIR) + "\\",
        "path": str(test_images_path),
        "url": "/static/test_images",
    }

    with monkeypatch.context() as m:
        m.setattr(
            settings.image_upload_dir.__class__,
            "image_upload_dir",
            property(lambda self: test_config),
        )
        yield
    if test_images_path.exists():
        shutil.rmtree(test_images_path)


@asynccontextmanager
async def empty_lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Пустой lifespan для тестов."""
    yield


@pytest.fixture(autouse=True)
def disable_fastapi_cache(monkeypatch):
    """
    Полностью отключает FastAPICache в тестах.
    """
    # Заглушка для backend
    backend = InMemoryBackend()

    async def async_noop(*args, **kwargs):
        """Асинхронная заглушка."""
        pass

    # Заглушка init и clear
    monkeypatch.setattr(
        "fastapi_cache.FastAPICache.init",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        "fastapi_cache.FastAPICache.clear",
        async_noop,
    )

    # Заглушка методов, которые проверяют инициализацию
    monkeypatch.setattr(
        "fastapi_cache.FastAPICache.get_prefix",
        lambda: "test-prefix",
    )
    monkeypatch.setattr(
        "fastapi_cache.FastAPICache.get_coder",
        lambda: JsonCoder,
    )
    monkeypatch.setattr(
        "fastapi_cache.FastAPICache.get_backend",
        lambda: backend,
    )
    monkeypatch.setattr(
        "fastapi_cache.FastAPICache.get_cache_status_header",
        lambda: "X-Cache-Status",
    )

    # Отключение декоратор @cache
    monkeypatch.setattr(
        "fastapi_cache.decorator.cache",
        lambda *args, **kwargs: lambda f: f,
    )


@pytest.fixture(scope="function")
async def client(test_session):
    """
    Создает тестовый клиент для тестирования API.
    """

    def override_get_session():
        """Заменяет реальную сессию на тестовую."""
        return test_session

    app: FastAPI = create_app(
        create_custom_static_urls=True,
        lifespan_override=empty_lifespan,
        enable_rate_limit=False,
    )
    app.include_router(api_router)
    app.include_router(views_router)
    app.dependency_overrides[get_db_session] = override_get_session  # type: ignore

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()  # type: ignore
