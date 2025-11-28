from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from api.api_v1.services.orders_service import OrdersService
from utils.key_builder import user_orders_key_builder

from core.dependencies import get_db_session
from core.dependencies.fastapi_users import current_active_user

from core.config import settings
from core.models import User
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

    **Описание:**
    Используется для оформления заказа пользователем на сайте.

    **Принимает поля:**
    - `product_id`: ID товара (int, id > 0).
    - `pickup_point_id`: ID пункта самовывоза (int, id > 0).

    **Логика:**
    - Проверяет наличие пункта самовывоза.
    - Проверяет, что товар существует и `is_active=True`.
    - Создаёт заказ со статусом `pending`.
    - Генерирует ссылку на оплату через YooKassa.
    - Возвращает данные заказа с `payment_url`.

    **Ответы:**
    - `201 Created` — заказ успешно создан. Возвращает `OrderRead`.
    - `400 Bad Request` — товар неактивен.
    - `404 Not Found` — пункт самовывоза или товар не найден.
    - `422 Unprocessable Entity` — ошибка валидации.
    - `500 Internal Server Error` — внутренняя ошибка.
    """
    _service = OrdersService(session=session)
    new_order = await _service.create_order(
        user_id=user.id,
        order_data=order_data,
    )
    await FastAPICache.clear(namespace=settings.cache.namespace.orders_list)
    return new_order


@router.get(
    path="/",
    response_model=list[OrderRead],
    status_code=status.HTTP_200_OK,
    operation_id="get_user_orders",
    summary="Получение всех заказов пользователя",
    responses={
        200: {"model": list[OrderRead]},
        401: {"description": "Пользователь не авторизован"},
        500: {"description": "Внутренняя ошибка сервера"},
    },
)
@cache(
    expire=120,
    key_builder=user_orders_key_builder,  # type: ignore
    namespace=settings.cache.namespace.orders_list,
)
async def get_user_orders(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[User, Depends(current_active_user)],
) -> list[OrderRead]:
    """
    ## Получение всех заказов текущего пользователя.

    **Описание:**
    Используется в личном кабинете для отображения истории заказов.

    **Ответы:**
    - `200 OK` — возвращает список заказов.
    - `401 Unauthorized` — пользователь не авторизован.
    - `500 Internal Server Error` — внутренняя ошибка.
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
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def get_all_orders(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[OrderRead]:
    """
    ## Получение всех заказов в системе.

    **Описание:**
    Используется в админ-панели для аналитики и модерации.

    **Ответы:**
    - `200 OK` — возвращает список всех заказов.
    - `500 Internal Server Error` — внутренняя ошибка.
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

    **Описание:**
    Используется в админ-панели и вебхуках (например, при подтверждении оплаты).

    ### Доступные статусы:
    - `pending` — ожидает оплаты
    - `paid` — оплачен
    - `processing` — в обработке
    - `ready` — готов к выдаче
    - `completed` — завершён
    - `cancelled` — отменён

    **Ответы:**
    - `200 OK` — статус обновлён. Возвращает обновлённый заказ.
    - `404 Not Found` — заказ не найден.
    - `422 Unprocessable Entity` — ошибка валидации.
    - `500 Internal Server Error` — внутренняя ошибка.
    """
    service = OrdersService(session=session)
    updated_order = await service.update_order_status(
        order_id=order_id,
        order_update=order_update,
    )
    await FastAPICache.clear(namespace=settings.cache.namespace.orders_list)
    return updated_order
