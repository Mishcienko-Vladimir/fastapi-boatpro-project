import pytest

from io import BytesIO
from fastapi import UploadFile
from starlette.datastructures import Headers
from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker

from core.models.user import User
from core.models.products import Product
from core.models.orders import Order, PickupPoint


faker = Faker()


@pytest.fixture
def mock_upload_file() -> UploadFile:
    """
    Создаёт реалистичный UploadFile для тестов.
    Использует BytesIO для имитации загруженного файла.
    """
    file = UploadFile(
        filename="test_image.jpg",
        file=BytesIO(b"fake image content"),
        headers=Headers({"content-type": "image/jpeg"}),
    )
    return file


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
