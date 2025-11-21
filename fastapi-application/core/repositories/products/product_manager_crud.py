from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession


class ProductManagerCrud:
    """
    Помощник для работы с товарами и категориями.

    :session: - сессия для работы с БД.
    :product_db: - модель БД (Boat, Trailer и т.д.).

    :methods:
        - get_product_by_name - получает товар по name.
        - get_product_by_id - получает товар по id.
        - get_all_products - получает все товары.
        - get_search_products - получает товары по ключевому слову.
        - create_product - создает новый товар.
        - update_product_data - обновляет товар, без обработки изображений.
        - delete_product - удаляет товар.
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
                selectinload(self.product_db.category),
                selectinload(self.product_db.images),
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
                selectinload(self.product_db.category),
                selectinload(self.product_db.images),
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
                selectinload(self.product_db.category),
                selectinload(self.product_db.images),
            )
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def get_search_products(self, query: str):
        """
        Получение товаров по ключевому слову (название, производитель, описание).

        :param query: - ключевое слово для поиска.
        :return: - список товаров или None.
        """

        stmt = (
            select(self.product_db)
            .where(
                (self.product_db.name.ilike(f"%{query}%"))
                | (self.product_db.company_name.ilike(f"%{query}%"))
                | (self.product_db.description.ilike(f"%{query}%")),
            )
            .options(
                selectinload(self.product_db.category),
                selectinload(self.product_db.images),
            )
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
