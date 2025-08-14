import aiofiles

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from core.config import settings


class ProductManagerCrud:
    """
    Помощник для работы с товарами.
    """

    def __init__(
        self,
        session: AsyncSession,
        product_db,
    ):
        self.session = session
        self.product_db = product_db  # Тип модели SQLAlchemy (Boat, Trailer и т.д.)

    async def create_category(self, category_data):
        """
        Создает новую категорию.
        """

        new_category = self.product_db(**category_data.model_dump())
        self.session.add(new_category)
        await self.session.commit()
        return new_category

    async def create_product_with_images(self, product_data, images, image_path_db):
        """
        Создает новый товар с изображением.
        """

        # Создаем продукт
        new_product = self.product_db(**product_data.model_dump())
        self.session.add(new_product)

        for image in images:
            file_path = f"{settings.image_upload_dir.path}/{uuid4().hex}.jpg"

            # Сохранение изображений в папку .../MFBoats/fastapi-application/static/images
            async with aiofiles.open(file_path, "wb") as file:
                await file.write(image.file.read())

            # Сокращаем путь до /static/images/...
            shortened_path = file_path.partition("fastapi-application")[2]

            # Создаем запись в таблицу ImagePath
            image_path = image_path_db(path=shortened_path)
            self.session.add(image_path)

            # Добавляем изображение к прицепу
            new_product.images.append(image_path)
        await self.session.commit()
        return {"message": "Product and images created successfully"}

    async def get_product_by_name(self, name: str, options=None):
        """
        Найдет товар по name.
        """

        stmt = select(self.product_db).filter_by(name=name)
        if options:
            stmt = stmt.options(*options)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_product_by_id(self, product_id: int, options=None):
        """
        Получает товар по id.
        """

        stmt = select(self.product_db).filter_by(id=product_id)
        if options:
            stmt = stmt.options(*options)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all_products(self, options=None):
        """
        Получает все товары.
        """

        stmt = select(self.product_db)
        if options:
            stmt = stmt.options(*options)
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def update_product_by_id(
        self,
        product_id: int,
        product_update_schema,
    ):
        """
        Обновляет товар по id.
        """

        product = await self.get_product_by_id(product_id)
        if product:
            for name, value in product_update_schema.model_dump(
                exclude_unset=True
            ).items():
                setattr(product, name, value)
            await self.session.commit()
            return product
        return None

    async def delete_product_by_id(self, product_id: int) -> bool:
        """
        Удаляет товар по id.
        """

        product = await self.get_product_by_id(product_id)
        if product:
            await self.session.delete(product)
            await self.session.commit()
            return True
        return False
