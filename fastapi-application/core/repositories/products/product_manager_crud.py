import os

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
        self.image_dir = settings.image_upload_dir.path

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

        new_product = self.product_db(**product_data.model_dump())
        self.session.add(new_product)

        # Сохранение изображений
        for img_file in images:
            file_extension = os.path.splitext(img_file.filename)[1]
            filename = f"{uuid4().hex}{file_extension}"
            filepath = os.path.join(self.image_dir, filename)

            # Сохраняем изображение на диск
            contents = await img_file.read()
            with open(filepath, "wb") as buffer:
                buffer.write(contents)

            # Создаем запись в ImagePath
            image_path = image_path_db(path=filepath)
            self.session.add(image_path)

            # Добавляем изображение к прицепу
            self.product_db.images.append(image_path)

            # file_location = os.path.join(self.image_dir, f"{uuid4()}_{image.filename}")
            # with open(file_location, "wb+") as file_object:
            #     file_object.write(await image.read())
            # # Сохранение пути в БД
            # image_path = image_path_db(path=file_location)
            # self.session.add(image_path)
            # new_product.images.append(image_path)

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
