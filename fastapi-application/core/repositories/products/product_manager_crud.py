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
        self.product_db = product_db

    async def create_product(self, product_data):
        """
        Создает новый товар.
        """

        new_product = self.product_db(**product_data.model_dump())
        self.session.add(new_product)
        await self.session.commit()
        return new_product

    async def create_product_with_images(self, product_data, images, image_path_db):
        """
        Создает новый товар с изображением.
        """

        # Создаем продукт
        new_product = self.product_db(**product_data.model_dump())
        self.session.add(new_product)

        for image in images:
            file_path = f"{settings.image_upload_dir.path}/{uuid4().hex}.jpg"

            # Сохранение изображений в папку images
            async with aiofiles.open(file_path, "wb") as file:
                await file.write(image.file.read())

            # Создаем запись в таблицу ImagePath
            image_path = image_path_db(path=file_path)
            self.session.add(image_path)

            # Добавляем изображение к прицепу
            self.product_db.images.append(image_path)

        await self.session.commit()
        return new_product

    async def get_product_by_name(self, name: str):
        """
        Найдет товар по name.
        """

        stmt = select(self.product_db).filter_by(name=name)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_product_by_id(self, product_id: int):
        """
        Получает товар по id.
        """

        return await self.session.get(self.product_db, product_id)

    async def get_all_products(self):
        """
        Получает все товары.
        """

        stmt = select(self.product_db).order_by(self.product_db.id)
        result = await self.session.scalars(stmt)
        return result.all()

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
