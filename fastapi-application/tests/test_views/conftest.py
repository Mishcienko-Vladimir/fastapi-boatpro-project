import pytest

from fastapi import FastAPI
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from api import router as api_router

from core.dependencies import get_db_session
from core.models import User
from core.models.products import (
    Product,
    Category,
    Boat,
    Trailer,
    OutboardMotor,
    ImagePath,
    ProductImagesAssociation,
)
from core.repositories.authentication.fastapi_users import (
    current_active_superuser,
    optional_user,
)
from create_fastapi_app import create_app
from views import router as views_router


faker = Faker()


@pytest.fixture
async def test_user(test_session: AsyncSession) -> User:
    """
    Создаёт тестового пользователя.
    """
    user = User(
        email=faker.email(),
        hashed_password="fakehash",
        first_name=faker.first_name(),
        is_active=True,
        is_superuser=False,
    )
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    return user


@pytest.fixture
async def test_category(test_session: AsyncSession) -> Category:
    """Создаёт тестовую категорию."""
    category = Category(
        name=f"Category {faker.uuid4()[:8]}",
        description=faker.text(),
    )
    test_session.add(category)
    await test_session.commit()
    await test_session.refresh(category)
    return category


@pytest.fixture
async def test_product(
    test_session: AsyncSession,
    test_category: Category,
) -> Product:
    """Создаёт тестовый товар."""
    product = Product(
        name=f"Product-{faker.uuid4()[:8]}",
        price=faker.random_int(10000, 1000000),
        company_name=faker.company()[:100],
        category_id=test_category.id,
        description=faker.text(),
    )
    test_session.add(product)
    await test_session.commit()
    await test_session.refresh(product)
    return product


@pytest.fixture
async def test_image(
    test_session: AsyncSession,
) -> ImagePath:
    """
    Создаёт тестовое изображение.
    """
    image = ImagePath(
        path=f"/static/test_images/{faker.file_name(extension='jpg')}",
    )
    test_session.add(image)
    await test_session.commit()
    await test_session.refresh(image)
    return image


@pytest.fixture
async def test_boat(
    test_session: AsyncSession,
    test_category: Category,
    test_image: ImagePath,
) -> Boat:
    """
    Создаёт тестовый катер.
    """
    boat = Boat(
        name=f"Boat-{faker.uuid4()[:8]}",
        price=faker.random_int(10000, 1000000),
        company_name=faker.company()[:100],
        category_id=test_category.id,
        description=faker.text(),
        is_active=True,
        length_hull=faker.random_int(300, 1000),
        width_hull=faker.random_int(100, 300),
        weight=faker.random_int(100, 500),
        capacity=faker.random_int(1, 6),
        maximum_load=faker.random_int(100, 1000),
        hull_material=faker.random_element(
            elements=["Aluminum", "Steel", "Fiberglass", "Tree"]
        ),
        thickness_side_sheet=faker.random_int(10, 1000),
        bottom_sheet_thickness=faker.random_int(10, 1000),
        fuel_capacity=faker.random_int(10, 1000),
        maximum_engine_power=faker.random_int(10, 1000),
        height_side_midship=faker.random_int(10, 1000),
        transom_height=faker.random_int(10, 1000),
    )
    test_session.add(boat)
    await test_session.commit()
    await test_session.refresh(boat)

    association = ProductImagesAssociation(
        product_id=boat.id,
        image_id=test_image.id,
    )
    test_session.add(association)
    await test_session.commit()
    return boat


@pytest.fixture
async def test_trailer(
    test_session: AsyncSession,
    test_category: Category,
    test_image: ImagePath,
) -> Trailer:
    """
    Создаёт тестовый прицеп.
    """
    trailer = Trailer(
        name=f"Trailer-{faker.uuid4()[:8]}",
        price=faker.random_int(10000, 1000000),
        company_name=faker.company()[:100],
        category_id=test_category.id,
        description=faker.text(),
        is_active=True,
        full_mass=faker.random_int(500, 2000),
        load_capacity=faker.random_int(300, 1500),
        trailer_length=faker.random_int(400, 1000),
        max_ship_length=faker.random_int(300, 900),
    )
    test_session.add(trailer)
    await test_session.commit()
    await test_session.refresh(trailer)

    association = ProductImagesAssociation(
        product_id=trailer.id,
        image_id=test_image.id,
    )
    test_session.add(association)
    await test_session.commit()
    return trailer


@pytest.fixture
async def test_outboard_motor(
    test_session: AsyncSession,
    test_category: Category,
    test_image: ImagePath,
) -> OutboardMotor:
    """
    Создаёт тестовый лодочный мотор.
    """
    outboard_motor = OutboardMotor(
        name=f"OutboardMotor-{faker.uuid4()[:8]}",
        price=faker.random_int(10000, 1000000),
        company_name=faker.company()[:100],
        category_id=test_category.id,
        description=faker.text(),
        is_active=True,
        engine_power=faker.random_int(5, 200),
        engine_type=faker.random_element(elements=["двухтактный", "четырехтактный"]),
        weight=faker.random_int(20, 100),
        number_cylinders=faker.random_int(2, 6),
        engine_displacement=faker.random_int(200, 2000),
        control_type=faker.random_element(elements=["румпельное", "дистанционное"]),
        starter_type=faker.random_element(elements=["ручной", "электрический"]),
    )
    test_session.add(outboard_motor)
    await test_session.commit()
    await test_session.refresh(outboard_motor)

    association = ProductImagesAssociation(
        product_id=outboard_motor.id,
        image_id=test_image.id,
    )
    test_session.add(association)
    await test_session.commit()
    return outboard_motor


@pytest.fixture
def fastapi_app():
    """Создаёт приложение FastAPI для тестов."""
    app = create_app(create_custom_static_urls=True, enable_rate_limit=False)
    app.include_router(views_router)
    app.include_router(api_router)
    return app


@pytest.fixture
def base_client(fastapi_app: FastAPI, test_session: AsyncSession) -> AsyncClient:
    """Создаёт тестовый клиент с зависимостями."""

    def override_get_session():
        return test_session

    fastapi_app.dependency_overrides[get_db_session] = override_get_session  # type: ignore
    transport = ASGITransport(app=fastapi_app)
    client = AsyncClient(
        transport=transport,
        base_url="http://test",
    )
    return client


@pytest.fixture
async def client(
    base_client: AsyncClient, fastapi_app: FastAPI
) -> AsyncGenerator[AsyncClient, None]:
    """Клиент с чистыми overrides."""
    try:
        yield base_client
    finally:
        fastapi_app.dependency_overrides.clear()  # type: ignore


@pytest.fixture
async def authenticated_client(
    base_client: AsyncClient,
    fastapi_app: FastAPI,
    test_user: User,
) -> AsyncGenerator[AsyncClient, None]:
    """Клиент с подменой optional_user."""

    def override_optional_user():
        return test_user

    fastapi_app.dependency_overrides[optional_user] = override_optional_user  # type: ignore
    try:
        yield base_client
    finally:
        fastapi_app.dependency_overrides.clear()  # type: ignore


@pytest.fixture
async def superuser_client(
    base_client: AsyncClient,
    fastapi_app: FastAPI,
    test_user: User,
) -> AsyncGenerator[AsyncClient, None]:
    """Клиент с правами суперпользователя."""

    def override_current_active_superuser():
        user = test_user
        user.is_superuser = True
        return user

    fastapi_app.dependency_overrides[current_active_superuser] = (  # type: ignore
        override_current_active_superuser
    )
    try:
        yield base_client
    finally:
        fastapi_app.dependency_overrides.clear()  # type: ignore
