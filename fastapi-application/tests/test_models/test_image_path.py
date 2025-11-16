import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models.products import ImagePath


@pytest.mark.anyio
async def test_image_path_creation(test_session: AsyncSession):
    """
    Тест создания пути к изображению.
    """
    image = ImagePath(path="/static/images/test_image.jpg")
    test_session.add(image)
    await test_session.commit()
    await test_session.refresh(image)

    assert image.id is not None
    assert isinstance(image.path, str)
    assert image.path == "/static/images/test_image.jpg"


@pytest.mark.anyio
async def test_image_path_relationship_products_empty(
    test_session: AsyncSession,
):
    """
    Тест, что у нового изображения нет привязанных товаров.
    """
    image = ImagePath(path="/static/images/empty.jpg")
    test_session.add(image)
    await test_session.commit()
    await test_session.refresh(image)

    stmt = (
        select(ImagePath)
        .options(selectinload(ImagePath.products))
        .where(ImagePath.id == image.id)
    )
    result = await test_session.execute(stmt)
    loaded_image = result.scalar_one()

    assert hasattr(loaded_image, "products"), "ImagePath должен иметь атрибут products"
    assert isinstance(loaded_image.products, list)
    assert len(loaded_image.products) == 0


@pytest.mark.anyio
async def test_image_path_str_repr():
    """
    Тест строкового представления ImagePath.
    """
    image = ImagePath(id=1, path="/static/images/demo.jpg")
    result = str(image)

    assert "ImagePath" in result
    assert "id=1" in result
    assert "path='/static/images/demo.jpg'" in result
