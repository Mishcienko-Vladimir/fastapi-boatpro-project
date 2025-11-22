import logging

from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.products import Product
from core.models.orders import Order, OrderStatus, PickupPoint
from core.repositories.manager_сrud import ManagerCrud
from core.schemas.order import (
    OrderCreate,
    OrderCreateExtended,
    OrderRead,
    OrderUpdate,
    OrderPaymentUpdate,
)

from utils.payment.yookassa import generate_payment_link


log = logging.getLogger(__name__)


class OrdersService:
    """
    Сервис для управления операциями с заказами.

    Attributes:
        repo_order (ManagerCrud): Репозиторий для работы с заказами в БД
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с БД

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с БД

    Methods:
        create_order(user_id, order_data): - Создание нового заказа
        get_orders_by_user(user_id): - Получение всех заказов пользователя
        get_all_orders(): - Получение всех заказов в системе
        update_order_status(order_id, status): - Обновление статуса заказа
    """

    def __init__(self, session: AsyncSession):
        self.repo_order = ManagerCrud(session=session, model_db=Order)
        self.session = session

    async def create_order(
        self,
        user_id: int,
        order_data: OrderCreate,
    ) -> OrderRead:
        """
        Создаёт новый заказ с привязкой к пользователю.

        Используется при оформлении заказа пользователем.

        Процесс:
            1. Проверяется существование пункта самовывоза.
            2. Проверяется наличие и активность товара.
            3. Создаётся заказ со статусом `pending`.
            4. Генерируется ссылка на оплату через YooKassa.
            5. Заказ обновляется с данными платежа.
            6. Возвращается полная модель заказа.

        Args:
            user_id (int): Уникальный идентификатор пользователя
            order_data (OrderCreate): Схема с `product_id` и `pickup_point_id`

        Raises:
            HTTPException: 404 NOT FOUND — Если пункт самовывоза или товар не найден
            HTTPException: 400 BAD REQUEST — Если товар нет в наличии

        Returns:
            OrderRead: Модель созданного заказа с данными для оплаты
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
        new_order_data = OrderCreateExtended(
            user_id=user_id,
            total_price=product.price,
            status=OrderStatus.PENDING,
            product_name=product.name,
            pickup_point_name=pickup_point.name,
            **order_data.model_dump(),
        )
        order = await self.repo_order.create(data=new_order_data)

        # 4. Генерируем ссылку на оплату
        payment_data = generate_payment_link(
            order_id=order.id,
            amount=product.price,
            description=f"Оплата заказа №{order.id}",
        )

        # 5. Обновляем заказ и возвращаем данные
        data_update = OrderPaymentUpdate(
            payment_id=payment_data["payment_id"],
            payment_url=payment_data["confirmation_url"],
            expires_at=order.created_at + timedelta(minutes=15),
        )
        updated_order = await self.repo_order.update(
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
        Получает все заказы, принадлежащие пользователю.

        Выполняет выборку заказов по `user_id`.
        Возвращает список заказов в виде модели `OrderRead`.

        Используется в личном кабинете пользователя для отображения истории заказов.

        Args:
            user_id (int): Уникальный идентификатор пользователя

        Raises:
            HTTPException: 404 NOT FOUND — Если у пользователя нет заказов

        Returns:
            list[OrderRead]: Список заказов пользователя
        """
        orders = await self.repo_order.get_all_by_field(
            field="user_id",
            value=user_id,
        )

        if not orders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="У пользователя нет заказов",
            )
        return [OrderRead.model_validate(order) for order in orders]

    async def get_all_orders(self) -> list[OrderRead]:
        """
        Получает все заказы в системе.

        Возвращает полный список заказов без фильтрации.

        Используется в админ-панели для модерации и аналитики.

        Raises:
            HTTPException: 404 NOT FOUND — Если в системе нет ни одного заказа

        Returns:
            list[OrderRead]: Список всех заказов
        """
        orders = await self.repo_order.get_all()

        if not orders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Нет заказов",
            )
        return [OrderRead.model_validate(order) for order in orders]

    async def update_order_status(
        self,
        order_id: int,
        order_update: OrderUpdate,
    ) -> OrderRead:
        """
        Обновляет статус заказа по его ID.

        При обновлении проверяется существование заказа. Если заказ не найден —
        возвращается ошибка 404. Поддерживает переход между статусами:
        `pending` → `paid` → `processing` → `ready` → `completed`.

        Используется в админ-панели и вебхуках (например, при подтверждении оплаты).

        Args:
            order_id (int): Уникальный идентификатор заказа
            order_update (OrderUpdate): Схема с новым статусом заказа

        Raises:
            HTTPException: 404 NOT FOUND - Если заказ с указанным `order_id` не найден

        Returns:
            OrderRead: Обновлённая модель заказа с актуальным статусом
        """
        order = await self.repo_order.get_by_id(instance_id=order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Заказ не найден",
            )

        updated_order = await self.repo_order.update(
            instance=order,
            data=order_update,
        )
        log.info("Updated order with id: %r", order_id)
        return OrderRead.model_validate(updated_order)
