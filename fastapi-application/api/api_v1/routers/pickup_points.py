from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from api.api_v1.services.pickup_points_service import PickupPointsService
from utils.key_builder import universal_list_key_builder

from core.config import settings
from core.dependencies import get_db_session
from core.schemas.pickup_point import (
    PickupPointCreate,
    PickupPointUpdate,
    PickupPointRead,
)


router = APIRouter(
    prefix=settings.api.v1.pickup_points,
    tags=["Пункты выдачи 📍"],
)


@router.post(
    path="/",
    response_model=PickupPointRead,
    status_code=status.HTTP_201_CREATED,
    operation_id="create_pickup_point",
    summary="Создание нового пункта выдачи",
    responses={
        201: {"model": PickupPointRead},
        400: {"description": "Имя уже занято или данные некорректны."},
        422: {"description": "Ошибка валидации входных данных."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def create_pickup_point(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    pickup_point_data: PickupPointCreate,
) -> PickupPointRead:
    """
    ## Создание нового пункта выдачи.

    **Описание:**
    Используется для создания нового пункта выдачи в админ-панели.

    **Принимает поля:**
    - `name`: Название (уникальное, str, 1–100 символов).
    - `address`: Полный адрес (str, минимум 1 символ).
    - `work_hours`: Время работы (str, 1–100 символов), например: Пн-Пт 9:00-18:00.

    **Ответы:**
    - `201 Created` — успешно создан. Возвращает созданный объект.
    - `400 Bad Request` — имя занято или данные некорректны.
    - `422 Unprocessable Entity` — ошибка валидации.
    - `500 Internal Server Error` — внутренняя ошибка
    """
    _service = PickupPointsService(session=session)
    new_pickup_point = await _service.create_pickup_point(
        pickup_point_data=pickup_point_data
    )
    await FastAPICache.clear(namespace=settings.cache.namespace.pickup_points_list)
    return new_pickup_point


@router.get(
    path="/pickup-point-name/{pickup_point_name}/",
    response_model=PickupPointRead,
    status_code=status.HTTP_200_OK,
    operation_id="get_pickup_point_by_name",
    summary="Получение пункта выдачи по имени",
    responses={
        200: {"model": PickupPointRead},
        404: {"description": "Пункт выдачи не найден."},
        422: {"description": "Некорректный формат имени."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def get_pickup_point_by_name(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    pickup_point_name: str,
) -> PickupPointRead:
    """
    ## Получение пункта выдачи по имени.

    **Описание:**
    Используется для получения пункта выдачи по его имени в админ-панели.

    **Принимает поле:**
    - `pickup_point_name`: Название пункта выдачи (уникальное, str, 1–100 символов).

    **Ответы:**
    - `200 OK` — успешно найден. Возвращает объект пункта выдачи.
    - `404 Not Found` — не найден.
    - `422 Unprocessable Entity` — некорректный формат имени.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = PickupPointsService(session=session)
    return await _service.get_pickup_point_by_name(pickup_point_name=pickup_point_name)


@router.get(
    path="/pickup-point-id/{pickup_point_id}/",
    response_model=PickupPointRead,
    status_code=status.HTTP_200_OK,
    operation_id="get_pickup_point_by_id",
    summary="Получение пункта выдачи по id",
    responses={
        200: {"model": PickupPointRead},
        404: {"description": "Пункт выдачи не найден."},
        422: {"description": "Некорректный формат ID."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def get_pickup_point_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    pickup_point_id: int,
) -> PickupPointRead:
    """
    ## Получение пункта выдачи по id.

    **Описание:**
    Используется для получения пункта выдачи по его ID в админ-панели.

    **Принимает поле:**
    - `pickup_point_id`: ID пункта выдачи (int, целое число).

    **Ответы:**
    - `200 OK` — успешно найден. Возвращает объект пункта выдачи.
    - `404 Not Found` — не найден.
    - `422 Unprocessable Entity` — некорректный формат ID.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = PickupPointsService(session=session)
    pickup_point = await _service.get_pickup_point_by_id(pickup_point_id)
    return PickupPointRead.model_validate(pickup_point)


@router.get(
    path="/",
    response_model=list[PickupPointRead],
    status_code=status.HTTP_200_OK,
    operation_id="get_all_pickup_points",
    summary="Получение всех пунктов выдачи",
    responses={
        200: {"model": list[PickupPointRead]},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
@cache(
    expire=300,
    key_builder=universal_list_key_builder,  # type: ignore
    namespace=settings.cache.namespace.pickup_points_list,
)
async def get_all_pickup_points(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[PickupPointRead]:
    """
    ## Получение всех пунктов выдачи.

    **Описание:**
    Используется для получения всех пунктов выдачи в оформлении заказа и в админ-панели.

    **Ответы:**
    - `200 OK` — список найден. Возвращает список пунктов выдачи.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = PickupPointsService(session=session)
    return await _service.get_pickup_points()


@router.patch(
    path="/{pickup_point_id}/",
    response_model=PickupPointRead,
    status_code=status.HTTP_200_OK,
    operation_id="update_pickup_point_by_id",
    summary="Частичное обновление пункта выдачи",
    responses={
        200: {"model": PickupPointRead},
        400: {"description": "Имя уже занято или данные некорректны."},
        404: {"description": "Пункт выдачи не найден."},
        422: {"description": "Ошибка валидации входных данных."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def update_pickup_point_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    pickup_point_id: int,
    pickup_point_data: PickupPointUpdate,
) -> PickupPointRead:
    """
    ## Частичное обновление пункта выдачи.

    **Описание:**
    Используется для частичного обновления пункта выдачи в админ-панели.

    **Принимает поля:**
    - `pickup_point_id`: ID пункта выдачи (int, целое число), для изменения.
    - `name`: Название (уникальное, Optional[str], 1–100 символов). Если не указано, не изменяется.
    - `address`: Полный адрес (Optional[str], минимум 1 символ). Если не указано, не изменяется.
    - `work_hours`: Время работы (Optional[str], 1–100 символов), пример: Пн-Пт 9:00-18:00. Если не указано, не изменяется.

    **Ответы:**
    - `200 OK` — успешно обновлён. Возвращает обновлённый объект.
    - `400 Bad Request` — имя занято или данные некорректны.
    - `404 Not Found` — пункт выдачи не найден.
    - `422 Unprocessable Entity` — ошибка валидации.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = PickupPointsService(session=session)
    update_pickup = await _service.update_pickup_point_by_id(
        pickup_point_id=pickup_point_id,
        pickup_point_data=pickup_point_data,
    )
    await FastAPICache.clear(namespace=settings.cache.namespace.pickup_points_list)
    return update_pickup


@router.delete(
    path="/{pickup_point_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="delete_pickup_point_by_id",
    summary="Удаление пункта выдачи",
    responses={
        204: {"description": "Пункт выдачи успешно удалён, ответ пуст."},
        404: {"description": "Пункт выдачи не найден."},
        422: {"description": "Некорректный формат ID."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def delete_pickup_point_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    pickup_point_id: int,
) -> None:
    """
    ## Удаление пункта выдачи по id.

    **Описание:**
    Используется для удаления пункта выдачи в админ-панели.

    **Принимает поле:**
    - `pickup_point_id`: ID пункта выдачи (int, целое число), для удаления.

    **Ответы:**
    - `204 No Content` — успешно удалён. Ничего не возвращается.
    - `404 Not Found` — пункт выдачи не найден.
    - `422 Unprocessable Entity` — некорректный ID.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = PickupPointsService(session=session)
    delete_pickup_point = await _service.delete_pickup_point_by_id(
        pickup_point_id=pickup_point_id
    )
    await FastAPICache.clear(namespace=settings.cache.namespace.pickup_points_list)
    return delete_pickup_point
