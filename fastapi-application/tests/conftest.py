import pytest
import shutil
import uuid

from fastapi import FastAPI
from fastapi_cache.coder import JsonCoder
from fastapi_cache.backends.inmemory import InMemoryBackend

from contextlib import asynccontextmanager
from typing import AsyncIterator, Any
from httpx import AsyncClient, ASGITransport
from pathlib import Path
from faker import Faker

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.pool import StaticPool

from api import router as api_router
from views import router as views_router
from create_fastapi_app import create_app

from core.dependencies import get_db_session
from core.config import settings, BASE_DIR
from core.models import Base, User
from core.models.products import Product, Category
from core.models.orders import Order, PickupPoint


faker = Faker()

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


@pytest.fixture(scope="function")
def fake_user_data() -> dict[str, Any]:
    """
    Генерация тестовых данных пользователя.
    """
    return {
        "email": faker.email(),
        "hashed_password": faker.password(),
        "first_name": faker.first_name(),
        "is_active": True,
        "is_superuser": False,
    }


@pytest.fixture(scope="function")
def fake_category_data() -> dict[str, Any]:
    """
    Генерация тестовых данных категории.
    """
    return {
        "name": f"Category-{uuid.uuid4().hex[:40]}",
        "description": faker.text(),
    }


@pytest.fixture(scope="function")
def fake_product_data() -> dict[str, Any]:
    """
    Создаёт тестовые данные для товара.
    """
    return {
        "name": f"Product-{uuid.uuid4().hex[:100]}",
        "price": faker.random_int(10000, 1000000),
        "company_name": faker.company()[:100],
        "is_active": True,
        "description": faker.text(),
    }


@pytest.fixture(scope="function")
def fake_boat_data() -> dict[str, Any]:
    """
    Создаёт тестовые данные для катера.
    """
    return {
        "name": f"Boat-{uuid.uuid4().hex[:100]}",
        "price": faker.random_int(20000, 20000000),
        "company_name": faker.company()[:100],
        "description": faker.text(),
        "is_active": True,
        "length_hull": faker.random_int(200, 10000),
        "width_hull": faker.random_int(100, 900),
        "weight": faker.random_int(100, 30000),
        "capacity": faker.random_int(1, 20),
        "maximum_load": faker.random_int(100, 4000),
        "hull_material": faker.random_element(
            elements=["Aluminum", "Steel", "Fiberglass", "Tree"]
        ),
        "thickness_side_sheet": faker.random_int(10, 1000),
        "bottom_sheet_thickness": faker.random_int(10, 1000),
        "fuel_capacity": faker.random_int(10, 1000),
        "maximum_engine_power": faker.random_int(10, 1000),
        "height_side_midship": faker.random_int(10, 1000),
        "transom_height": faker.random_int(10, 1000),
    }


@pytest.fixture(scope="function")
def fake_trailer_data():
    """
    Создаёт тестовые данные для прицепа.
    """
    return {
        "name": f"Trailer-{uuid.uuid4().hex[:100]}",
        "price": faker.random_int(20000, 3000000),
        "company_name": faker.company()[:100],
        "description": faker.text(),
        "is_active": True,
        "full_mass": faker.random_int(200, 10000),
        "load_capacity": faker.random_int(200, 5000),
        "trailer_length": faker.random_int(200, 2000),
        "max_ship_length": faker.random_int(200, 10000),
    }


@pytest.fixture(scope="function")
def fake_outboard_motor_data():
    """
    Создаёт тестовые данные для мотора.
    """
    return {
        "name": f"Motor-{uuid.uuid4().hex[:100]}",
        "price": faker.random_int(10000, 5000000),
        "company_name": faker.company()[:100],
        "description": faker.text(),
        "is_active": True,
        "engine_power": faker.random_int(2, 600),
        "engine_type": faker.random_element(elements=["двухтактный", "четырехтактный"]),
        "weight": faker.random_int(5, 1000),
        "number_cylinders": faker.random_int(2, 6),
        "engine_displacement": faker.random_int(100, 9000),
        "control_type": faker.random_element(elements=["румпельное", "дистанционное"]),
        "starter_type": faker.random_element(elements=["ручной", "электрический"]),
    }


@pytest.fixture(scope="function")
async def test_user(
    test_session: AsyncSession,
    fake_user_data: dict[str, Any],
) -> User:
    """
    Создаёт тестового пользователя.
    """
    user = User(**fake_user_data)
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    return user


@pytest.fixture(scope="function")
async def test_category(
    test_session: AsyncSession,
    fake_category_data: dict[str, Any],
) -> Category:
    """
    Создаёт тестовую категорию.
    """
    category = Category(**fake_category_data)
    test_session.add(category)
    await test_session.commit()
    await test_session.refresh(category)
    return category


@pytest.fixture(scope="function")
async def test_product(
    test_session: AsyncSession,
    fake_product_data: dict[str, Any],
    test_category: Category,
) -> Product:
    """
    Создаёт тестовый товар.
    """
    product = Product(
        category_id=test_category.id,
        **fake_product_data,
    )
    test_session.add(product)
    await test_session.commit()
    await test_session.refresh(product)
    return product


@pytest.fixture(scope="function")
async def test_pickup_point(
    test_session: AsyncSession,
) -> PickupPoint:
    """
    Создаёт тестовый пункт выдачи.
    """
    pickup_point = PickupPoint(
        name=f"Pickup Point-{faker.uuid4()[:100]}",
        address=faker.address(),
        work_hours="Пн-Вс: 9:00-21:00",
    )
    test_session.add(pickup_point)
    await test_session.commit()
    await test_session.refresh(pickup_point)
    return pickup_point


@pytest.fixture(scope="function")
async def test_order(
    test_session: AsyncSession,
    test_user: User,
    test_product: Product,
    test_pickup_point: PickupPoint,
) -> Order:
    """
    Создаёт тестовый заказ.
    """
    order = Order(
        user_id=test_user.id,
        product_id=test_product.id,
        pickup_point_id=test_pickup_point.id,
        status="pending",
        payment_id=faker.uuid4()[:255],
        payment_url=faker.url()[:255],
        expires_at=faker.date_time(),
        created_at=faker.date_time(),
        product_name=test_product.name,
        total_price=test_product.price,
        type_product=test_product.type_product,
        pickup_point_name=test_pickup_point.name,
        pickup_point_address=test_pickup_point.address,
        work_hours=test_pickup_point.work_hours,
    )
    test_session.add(order)
    await test_session.commit()
    await test_session.refresh(order)
    return order
