from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.orders_service import OrdersService

from core.config import settings
from core.dependencies import get_db_session
from core.models import User
from core.repositories.authentication.fastapi_users import current_active_user
from core.schemas.order import OrderCreate, OrderRead, OrderUpdate


router = APIRouter(
    prefix=settings.api.v1.orders,
    tags=["Заказы 📋"],
)


@router.post(
    path="/",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создание нового заказа",
)
async def create_order(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[User, Depends(current_active_user)],
    order_data: OrderCreate,
) -> OrderRead:
    """
    Создание нового заказа.
    """
    _service = OrdersService(session=session)
    return await _service.create_order(user_id=user.id, order_data=order_data)


@router.get(
    path="/",
    response_model=list[OrderRead],
    status_code=status.HTTP_200_OK,
    summary="Получение всех заказов пользователя",
)
async def get_user_orders(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[User, Depends(current_active_user)],
) -> list[OrderRead]:
    """
    Получение всех заказов текущего пользователя.
    """
    service = OrdersService(session=session)
    return await service.get_orders_by_user(user_id=user.id)


@router.get(
    path="/all-orders",
    response_model=list[OrderRead],
    status_code=status.HTTP_200_OK,
    summary="Получение всех заказов",
)
async def get_all_orders(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[OrderRead]:
    """
    Получение всех заказов.
    """
    service = OrdersService(session=session)
    return await service.get_all_orders()


# TODO: Добавить определенный выбор статуса
@router.patch(
    path="/{order_id}/",
    response_model=OrderRead,
    status_code=status.HTTP_200_OK,
    summary="Обновление статуса заказа",
    description="Только для администратора. Позволяет изменить статус заказа.",
)
async def update_order_status(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    order_id: int,
    order_update: OrderUpdate,
) -> OrderRead:
    """
    Обновление статуса заказа.
    Только для суперпользователя (админа).
    """
    service = OrdersService(session=session)
    return await service.update_order_status(
        order_id=order_id,
        order_update=order_update,
    )
