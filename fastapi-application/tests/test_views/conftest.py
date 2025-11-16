import pytest

from fastapi import FastAPI
from typing import AsyncGenerator, Any
from httpx import AsyncClient, ASGITransport
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from api import router as api_router
from create_fastapi_app import create_app
from views import router as views_router

from core.dependencies import get_db_session
from core.models import User
from core.models.products import (
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


faker = Faker()


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
    fake_boat_data: dict[str, Any],
    test_category: Category,
    test_image: ImagePath,
) -> Boat:
    """
    Создаёт тестовый катер.
    """
    boat = Boat(
        category_id=test_category.id,
        **fake_boat_data,
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
    fake_trailer_data: dict[str, Any],
    test_category: Category,
    test_image: ImagePath,
) -> Trailer:
    """
    Создаёт тестовый прицеп.
    """
    trailer = Trailer(
        category_id=test_category.id,
        **fake_trailer_data,
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
    fake_outboard_motor_data: dict[str, Any],
    test_category: Category,
    test_image: ImagePath,
) -> OutboardMotor:
    """
    Создаёт тестовый лодочный мотор.
    """
    outboard_motor = OutboardMotor(
        category_id=test_category.id,
        **fake_outboard_motor_data,
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
    """
    Создаёт приложение FastAPI для тестов.
    """
    app = create_app(
        create_custom_static_urls=True,
        enable_rate_limit=False,
    )
    app.include_router(views_router)
    app.include_router(api_router)
    return app


@pytest.fixture
def base_client(
    fastapi_app: FastAPI,
    test_session: AsyncSession,
) -> AsyncClient:
    """
    Создаёт тестовый клиент с зависимостями.
    """

    def override_get_session():
        """
        Подменяет сессию на тестовую.
        """
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
    base_client: AsyncClient,
    fastapi_app: FastAPI,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Клиент с чистыми overrides.
    """
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
    """
    Клиент с подменой optional_user.
    """

    def override_optional_user():
        """
        Подменяет optional_user на тестового пользователя.
        """
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
    """
    Клиент с правами суперпользователя.
    """

    def override_current_active_superuser():
        """
        Подменяет current_active_superuser на тестового суперпользователя.
        """
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
