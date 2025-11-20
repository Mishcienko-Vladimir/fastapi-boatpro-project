import logging

from datetime import timedelta
from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.products import Product
from core.models.orders import Order, OrderStatus
from core.schemas.order import OrderCreate, OrderRead, OrderUpdate

from core.repositories.pickup_point_manager_crud import PickupPointManagerCrud
from core.repositories.products.product_manager_crud import ProductManagerCrud

from utils.payment.yookassa import generate_payment_link


log = logging.getLogger(__name__)


class OrdersService:
    """
    Сервис для управления операциями с заказами.

    :param session: - сессия для работы с БД.
    """

    def __init__(self, session: AsyncSession):
        self.repo_pickup_point = PickupPointManagerCrud(session=session)
        self.repo_product = ProductManagerCrud(session=session, product_db=Product)
        self.session = session

    async def get_order_by_id(
        self,
        order_id: int,
    ) -> Order | None:
        """
        Получение заказа по ID.
        """
        return await self.session.get(Order, order_id)

    async def create_order(
        self,
        user_id: int,
        order_data: OrderCreate,
    ) -> OrderRead:
        """
        Создание заказа:
        1. Проверка пункта самовывоза
        2. Проверка товара
        3. Создание заказа
        4. Генерация ссылки на оплату
        5. Возврат OrderRead
        """
        # 1. Проверка пункта самовывоза
        pickup_point = await self.repo_pickup_point.get_pickup_point_by_id(
            point_id=order_data.pickup_point_id,
        )
        if not pickup_point:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пункт самовывоза не найден",
            )

        # 2. Проверка товара
        product = await self.repo_product.get_product_by_id(
            product_id=order_data.product_id,
        )
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Товар не найден",
            )
        if not product.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Товара нет в наличии",
            )

        # 3. Создание заказа
        order = Order(
            user_id=user_id,
            pickup_point_id=pickup_point.id,
            product_id=product.id,
            total_price=product.price,
            status=OrderStatus.PENDING,
        )
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)

        # 4. Генерируем ссылку на оплату
        payment_data = generate_payment_link(
            order_id=order.id,
            amount=product.price,
            description=f"Оплата заказа №{order.id}",
        )

        # 5. Обновляем заказ и возвращаем данные
        order.payment_id = payment_data["payment_id"]
        order.payment_url = payment_data["confirmation_url"]
        order.expires_at = order.created_at + timedelta(minutes=15)
        await self.session.commit()

        return OrderRead(
            id=order.id,
            user_id=order.user_id,
            pickup_point_id=order.pickup_point_id,
            product_id=order.product_id,
            status=order.status,
            total_price=order.total_price,
            created_at=order.created_at,
            payment_id=order.payment_id,  # type: ignore
            payment_url=order.payment_url,  # type: ignore
            expires_at=order.expires_at,  # type: ignore
            pickup_point_name=pickup_point.name,
            product_name=product.name,
        )

    async def get_orders_by_user(
        self,
        user_id: int,
    ) -> list[OrderRead]:
        """
        Получение всех заказов пользователя.
        """
        result = await self.session.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .options(
                selectinload(Order.pickup_point),
                selectinload(Order.product),
            )
        )
        orders = result.scalars().all()

        return [
            OrderRead(
                id=order.id,
                user_id=order.user_id,
                pickup_point_id=order.pickup_point_id,
                product_id=order.product_id,
                status=order.status,
                total_price=order.total_price,
                created_at=order.created_at,
                payment_id=order.payment_id,
                payment_url=order.payment_url,
                expires_at=order.expires_at,
                pickup_point_name=order.pickup_point.name,
                product_name=order.product.name,
            )
            for order in orders
        ]

    async def get_all_orders(self) -> list[OrderRead]:
        """
        Получение всех заказов.
        """
        result = await self.session.execute(
            select(Order).options(
                selectinload(Order.pickup_point),
                selectinload(Order.product),
            )
        )
        orders = result.scalars().all()
        return [
            OrderRead(
                id=order.id,
                user_id=order.user_id,
                pickup_point_id=order.pickup_point_id,
                product_id=order.product_id,
                status=order.status,
                total_price=order.total_price,
                created_at=order.created_at,
                payment_id=order.payment_id,
                payment_url=order.payment_url,
                expires_at=order.expires_at,
                pickup_point_name=order.pickup_point.name,
                product_name=order.product.name,
            )
            for order in orders
        ]

    async def update_order_status(
        self,
        order_id: int,
        order_update: OrderUpdate,
    ) -> OrderRead:
        """
        Обновление статуса заказа (для админа).
        """
        stmt = (
            select(Order)
            .filter_by(id=order_id)
            .options(
                selectinload(Order.pickup_point),
                selectinload(Order.product),
            )
        )
        result = await self.session.execute(stmt)
        order = result.scalars().first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Заказ не найден",
            )
        order.status = order_update.status
        await self.session.commit()
        await self.session.refresh(order)

        return OrderRead(
            id=order.id,
            user_id=order.user_id,
            pickup_point_id=order.pickup_point_id,
            product_id=order.product_id,
            status=order.status,  # type: ignore
            total_price=order.total_price,
            created_at=order.created_at,
            payment_id=order.payment_id,
            payment_url=order.payment_url,
            expires_at=order.expires_at,
            pickup_point_name=order.pickup_point.name,
            product_name=order.product.name,
        )
