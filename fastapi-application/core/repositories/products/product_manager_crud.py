from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession


class ProductManagerCrud:
    """
    Помощник для работы с товарами и категориями.

    :session: - сессия для работы с БД.
    :product_db: - модель БД (Boat, Trailer и т.д.).
    """

    def __init__(
        self,
        session: AsyncSession,
        product_db,
    ):
        self.session = session
        self.product_db = product_db

    async def get_product_by_name(self, name: str, options: bool = None):
        """
        Получает товар по name.

        :name: - имя товара.
        :options: - True - загрузить связанные данные.
        :return: - экземпляр модели товара или None.
        """

        stmt = select(self.product_db).filter_by(name=name)
        if options:
            stmt = stmt.options(
                joinedload(self.product_db.category),
                joinedload(self.product_db.images),
            )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_product_by_id(self, product_id: int, options: bool = None):
        """
        Получает товар по id.

        :param product_id: - id товара.
        :param options: - True - загрузить связанные данные.
        :return: - экземпляр модели товара или None.
        """

        stmt = select(self.product_db).filter_by(id=product_id)
        if options:
            stmt = stmt.options(
                joinedload(self.product_db.category),
                joinedload(self.product_db.images),
            )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all_products(self, options: bool = None):
        """
        Получает все товары.

        :param options: - True - загрузить связанные данные.
        :return: - список всех товаров или None.
        """

        stmt = select(self.product_db)
        if options:
            stmt = stmt.options(
                joinedload(self.product_db.category),
                joinedload(self.product_db.images),
            )
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def create_product(self, product_data):
        """
        Создает новый товар.

        :product_data: - данные для создания товара.
        :return: - экземпляр модели товара.
        """

        product = self.product_db(**product_data.model_dump())
        self.session.add(product)

        await self.session.commit()
        return product

    async def update_product_data(self, product, product_data):
        """
        Обновляет товар, без обработки изображений.

        :param product: - экземпляр модели товара для обновления.
        :param product_data: - данные для обновления.
        :return: - обновленный экземпляр модели товара.
        """

        for name, value in product_data.model_dump(exclude_unset=True).items():
            setattr(product, name, value)
        await self.session.commit()
        return product

    async def delete_product(self, product) -> bool:
        """
        Удаляет товар.

        :param product: - экземпляр модели товара для удаления.
        :return: - удаление прошло успешно True.
        """

        await self.session.delete(product)
        await self.session.commit()
        return True
