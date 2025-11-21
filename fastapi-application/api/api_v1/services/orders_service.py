import logging

from datetime import timedelta
from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.products import Product
from core.models.orders import Order, OrderStatus, PickupPoint
from core.schemas.order import OrderCreate, OrderRead, OrderUpdate, Payment

from core.repositories.manager_сrud import ManagerCrud
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
        pickup_point = await ManagerCrud(
            session=self.session, model_db=PickupPoint
        ).get_by_id(instance_id=order_data.pickup_point_id)

        if not pickup_point:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пункт самовывоза не найден",
            )

        # 2. Проверка товара
        product = await ManagerCrud(
            session=self.session,
            model_db=Product,
        ).get_by_id(instance_id=order_data.product_id)

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
        order_data.update(
            {
                "user_id": user_id,
                "total_price": product.price,
                "status": OrderStatus.PENDING,
                "product_name": product.name,
                "pickup_point_name": pickup_point.name,
            }
        )
        order = await ManagerCrud(
            session=self.session,
            model_db=Order,
        ).create(data=order_data)

        # 4. Генерируем ссылку на оплату
        payment_data = generate_payment_link(
            order_id=order.id,
            amount=product.price,
            description=f"Оплата заказа №{order.id}",
        )

        # 5. Обновляем заказ и возвращаем данные
        data_update = Payment(
            payment_id=payment_data["payment_id"],
            payment_url=payment_data["confirmation_url"],
            expires_at=order.created_at + timedelta(minutes=15),
        )
        updated_order = await ManagerCrud(
            session=self.session,
            model_db=Order,
        ).update(
            instance=order,
            data=data_update,
        )
        log.info("Created order with id: %r", updated_order.id)
        return OrderRead.model_validate(updated_order)

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
