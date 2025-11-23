from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.pickup_points_service import PickupPointsService

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
    description=(
        "## Создание нового пункта выдачи.\n\n"
        "**Принимает поля:**\n"
        "- `name`: Название (уникальное, 1–100 символов).\n"
        "- `address`: Полный адрес (минимум 1 символ).\n"
        "- `work_hours`: Время работы (1–100 символов), например: Пн-Пт 9:00-18:00.\n\n"
        "**Ответы:**\n"
        "- `201 Created` — успешно создан.\n"
        "- `400 Bad Request` — имя занято или данные некорректны.\n"
        "- `422 Unprocessable Entity` — ошибка валидации.\n"
        "- `500 Internal Server Error` — внутренняя ошибка."
    ),
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
    Создание нового пункта выдачи.
    """
    _service = PickupPointsService(session=session)
    return await _service.create_pickup_point(pickup_point_data)


@router.get(
    path="/pickup-point-name/{pickup_point_name}/",
    response_model=PickupPointRead,
    status_code=status.HTTP_200_OK,
    operation_id="get_pickup_point_by_name",
    summary="Получение пункта выдачи по имени",
    description=(
        "## Получение пункта выдачи по имени.\n\n"
        "**Ответы:**\n"
        "- `200 OK` — успешно найден.\n"
        "- `404 Not Found` — не найден.\n"
        "- `422 Unprocessable Entity` — некорректный формат имени."
    ),
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
    Получение пункта выдачи по имени.
    """
    _service = PickupPointsService(session=session)
    return await _service.get_pickup_point_by_name(pickup_point_name=pickup_point_name)


@router.get(
    path="/pickup-point-id/{pickup_point_id}/",
    response_model=PickupPointRead,
    status_code=status.HTTP_200_OK,
    operation_id="get_pickup_point_by_id",
    summary="Получение пункта выдачи по id",
    description=(
        "## Получение пункта выдачи по ID.\n\n"
        "**Ответы:**\n"
        "- `200 OK` — успешно найден.\n"
        "- `404 Not Found` — не найден.\n"
        "- `422 Unprocessable Entity` — некорректный формат ID."
    ),
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
    Получение пункта выдачи по id.
    """
    _service = PickupPointsService(session=session)
    pickup_point = await _service.get_pickup_point_by_id(
        pickup_point_id=pickup_point_id
    )
    return PickupPointRead.model_validate(pickup_point)


@router.get(
    path="/",
    response_model=list[PickupPointRead],
    status_code=status.HTTP_200_OK,
    operation_id="get_all_pickup_points",
    summary="Получение всех пунктов выдачи",
    description=(
        "## Получение всех пунктов выдачи.\n\n"
        "**Ответы:**\n"
        "- `200 OK` — список найден.\n"
        "- `404 Not Found` — список пуст."
    ),
    responses={
        200: {"model": list[PickupPointRead]},
        404: {"description": "Пункты выдачи отсутствуют."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def get_all_pickup_points(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[PickupPointRead]:
    """
    Получение всех пунктов выдачи.
    """
    _service = PickupPointsService(session=session)
    return await _service.get_pickup_points()


@router.patch(
    path="/{pickup_point_id}/",
    response_model=PickupPointRead,
    status_code=status.HTTP_200_OK,
    operation_id="update_pickup_point_by_id",
    summary="Обновление пункта выдачи",
    description=(
        "## Частичное обновление пункта выдачи.\n"
        "### Можно обновить одно или несколько полей. Если поле не указано — оно не изменится.\n\n"
        "**Принимает поля:**\n"
        "- `name`: Название (уникальное, 1–100 символов).\n"
        "- `address`: Полный адрес (минимум 1 символ).\n"
        "- `work_hours`: Время работы (1–100 символов), например: Пн-Пт 9:00-18:00.\n\n"
        "**Ответы:**\n\n"
        "- `200 OK` — успешно обновлён.\n"
        "- `400 Bad Request` — имя занято.\n"
        "- `404 Not Found` — не найден.\n"
        "- `422 Unprocessable Entity` — ошибка валидации."
    ),
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
    Обновление пункта выдачи.
    """
    _service = PickupPointsService(session=session)
    return await _service.update_pickup_point_by_id(
        pickup_point_id=pickup_point_id,
        pickup_point_data=pickup_point_data,
    )


@router.delete(
    path="/{pickup_point_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="delete_pickup_point_by_id",
    summary="Удаление пункта выдачи",
    description=(
        "## Удаление пункта выдачи по ID.\n\n"
        "**Ответы:**\n"
        "- `204 No Content` — успешно удалён.\n"
        "- `404 Not Found` — не найден.\n"
        "- `422 Unprocessable Entity` — некорректный ID."
    ),
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
    Удаление пункта выдачи.
    """
    _service = PickupPointsService(session=session)
    return await _service.delete_pickup_point_by_id(pickup_point_id=pickup_point_id)
