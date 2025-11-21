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
    operation_id="create_order",
    summary="Создание нового заказа",
    responses={
        201: {"model": OrderRead},
        400: {"description": "Товар недоступен или данные некорректны"},
        404: {"description": "Пункт самовывоза или товар не найден"},
        422: {"description": "Ошибка валидации входных данных"},
        500: {"description": "Внутренняя ошибка сервера"},
    },
)
async def create_order(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[User, Depends(current_active_user)],
    order_data: OrderCreate,
) -> OrderRead:
    """
    ## Создание нового заказа.

    **Принимает поля:**
    - `product_id`: ID товара
    - `pickup_point_id`: ID пункта самовывоза

    **Логика:**
    - Проверяет наличие пункта самовывоза и товара
    - Создаёт заказ со статусом `pending`
    - Генерирует ссылку на оплату через YooKassa
    """
    _service = OrdersService(session=session)
    return await _service.create_order(user_id=user.id, order_data=order_data)


@router.get(
    path="/",
    response_model=list[OrderRead],
    status_code=status.HTTP_200_OK,
    operation_id="get_user_orders",
    summary="Получение всех заказов пользователя",
    responses={
        200: {"model": list[OrderRead]},
        401: {"description": "Пользователь не авторизован"},
        404: {"description": "Заказы не найдены"},
        500: {"description": "Внутренняя ошибка сервера"},
    },
)
async def get_user_orders(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[User, Depends(current_active_user)],
) -> list[OrderRead]:
    """
    ## Получение всех заказов текущего пользователя.
    """
    service = OrdersService(session=session)
    return await service.get_orders_by_user(user_id=user.id)


@router.get(
    path="/all-orders",
    response_model=list[OrderRead],
    status_code=status.HTTP_200_OK,
    operation_id="get_all_orders",
    summary="Получение всех заказов",
    responses={
        200: {"model": list[OrderRead]},
        404: {"description": "Заказы отсутствуют."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def get_all_orders(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[OrderRead]:
    """
    ## Получение всех заказов.
    """
    service = OrdersService(session=session)
    return await service.get_all_orders()


@router.patch(
    path="/{order_id}/",
    response_model=OrderRead,
    status_code=status.HTTP_200_OK,
    operation_id="update_order_status",
    summary="Обновление статуса заказа",
    responses={
        200: {"model": OrderRead},
        404: {"description": "Заказ не найден."},
        422: {"description": "Ошибка валидации входных данных."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def update_order_status(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    order_id: int,
    order_update: OrderUpdate,
) -> OrderRead:
    """
    ## Обновление статуса заказа

    ### Доступные статусы:
    - `pending` — ожидает оплаты
    - `paid` — оплачен
    - `processing` — в обработке
    - `ready` — готов к выдаче
    - `completed` — завершён
    - `cancelled` — отменён
    """
    service = OrdersService(session=session)
    return await service.update_order_status(
        order_id=order_id,
        order_update=order_update,
    )
