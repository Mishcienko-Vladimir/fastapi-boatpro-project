from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, Form, File, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from api.api_v1.services.products import ProductsService
from api.api_v1.dependencies.create_multipart_form_data import (
    create_multipart_form_data,
)

from core.config import settings
from core.dependencies import get_db_session
from core.models.products import Boat
from core.schemas.products import (
    BoatCreate,
    BoatUpdate,
    BoatRead,
    BoatSummarySchema,
)

from utils.key_builder import (
    universal_list_key_builder,
    get_by_name_key_builder,
    get_by_id_key_builder,
)


router = APIRouter(
    prefix=settings.api.v1.boats,
    tags=["Катера 🚢"],
)


@router.post(
    path="/",
    response_model=BoatRead,
    status_code=status.HTTP_201_CREATED,
    operation_id="create_boat",
    summary="Создание нового катера",
    responses={
        201: {"model": BoatRead},
        400: {"description": "Имя уже занято или данные некорректны."},
        422: {"description": "Ошибка валидации входных данных."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def create_boat(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    boat_data: Annotated[
        BoatCreate,
        Depends(create_multipart_form_data(BoatCreate)),
    ],
    images: Annotated[
        list[UploadFile],
        File(..., description="Изображения товара"),
    ],
) -> BoatRead:
    """
    ## Создание нового катера.

    **Описание:**
    Используется для создания нового катера в админ-панели.

    **Принимает поля:**
    - `category_id`: ID категории товара (int, id > 0).
    - `name`: Название модели (str, 1–255 символов, уникальное).
    - `price`: Цена в рублях (int, цена > 0).
    - `company_name`: Название производителя (str, 1–100 символов).
    - `description`: Описание товара (str, может быть пустым).
    - `is_active`: Наличие товара (bool).
    - `length_hull`: Длина катера в см (int, 30000 > длинна > 0).
    - `width_hull`: Ширина катера в см (int, 10000 > ширина > 0).
    - `weight`: Вес катера в кг (int, 32767 > вес > 0).
    - `capacity`: Максимальная вместимость (человек) (int, 100 > человек > 0).
    - 'maximum_load': Максимальная грузоподъемность (кг) (int, 5000 > грузоподъемность > 0).
    - 'hull_material': Материал корпуса (str, 1–50 символов).
    - 'thickness_side_sheet': Толщина бортового листа (мм) (необязательный параметр, int, 1000 > толщина > 0).
    - 'bottom_sheet_thickness': Толщина днищевого листа (мм) (необязательный параметр, int, 1000 > толщина > 0).
    - 'fuel_capacity': Объем топливного бака (л) (необязательный параметр, int, 1000 > объем > 0).
    - `maximum_engine_power`: Максимальная мощность двигателя (л.с.) (необязательный параметр, int, 10000 > мощность > 0).
    - 'height_side_midship': Высота борта на миделе (мм) (необязательный параметр, int, 10000 > высота > 0).
    - 'transom_height': Высота транца (мм) (необязательный параметр, int, 1000 > высота > 0).
    - `images`: Список изображений товара (множественная загрузка, формат: image/*).

    **Ответы:**
    - `201 Created` — катер успешно создан. Возвращает созданный катер.
    - `400 Bad Request` — имя занято или данные некорректны.
    - `422 Unprocessable Entity` — ошибка валидации входных данных.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = ProductsService(session=session, product_db=Boat)
    new_boat = await _service.create_product(
        product_data=boat_data,
        images=images,
    )
    await FastAPICache.clear(namespace=settings.cache.namespace.boats_list)
    await FastAPICache.clear(namespace=settings.cache.namespace.boat)
    return BoatRead.model_validate(new_boat)


@router.get(
    path="/boat-name/{boat_name}",
    response_model=BoatRead,
    status_code=status.HTTP_200_OK,
    operation_id="get_boat_by_name",
    summary="Получение катера по названию",
    responses={
        200: {"model": BoatRead},
        404: {"description": "Катер не найден."},
        422: {"description": "Некорректный формат названия катера"},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
@cache(
    expire=300,
    key_builder=get_by_name_key_builder,  # type: ignore
    namespace=settings.cache.namespace.boat,
)
async def get_boat_by_name(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    boat_name: str,
) -> BoatRead:
    """
    ## Получение катера по названию.

    **Описание:**
    Используется для получения катера по его названию в админ-панели и на сайте.

    **Принимает поле:**
    - `boat_name`: Название катера (str, 1–255 символов).

    **Ответы:**
    - `200 OK` — катер успешно найден. Возвращает объект катера.
    - `404 Not Found` — катер не найден.
    - `422 Unprocessable Entity` — некорректный формат имени.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = ProductsService(session=session, product_db=Boat)
    boat = await _service.get_product_by_name(product_name=boat_name)
    return BoatRead.model_validate(boat)


@router.get(
    path="/boat-id/{boat_id}",
    response_model=BoatRead,
    status_code=status.HTTP_200_OK,
    operation_id="get_boat_by_id",
    summary="Получение катера по id",
    responses={
        200: {"model": BoatRead},
        404: {"description": "Катер не найден."},
        422: {"description": "Некорректный формат id"},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
@cache(
    expire=300,
    key_builder=get_by_id_key_builder,  # type: ignore
    namespace=settings.cache.namespace.boat,
)
async def get_boat_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    boat_id: int,
) -> BoatRead:
    """
    ## Получение катера по id.

    **Описание:**
    Используется для получения катера по его ID в админ-панели и на сайте.

    **Принимает поле:**
    - `boat_id`: ID катера (int, целое число).

    **Ответы:**
    - `200 OK` — катер успешно найден. Возвращает объект катера.
    - `404 Not Found` — катер не найден.
    - `422 Unprocessable Entity` — некорректный формат ID.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = ProductsService(session=session, product_db=Boat)
    boat = await _service.get_product_by_id(product_id=boat_id)
    return BoatRead.model_validate(boat)


@router.get(
    path="/",
    response_model=list[BoatRead],
    status_code=status.HTTP_200_OK,
    operation_id="get_boats",
    summary="Получение всех катеров",
    responses={
        200: {"model": list[BoatRead]},
        404: {"description": "Список пуст."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
@cache(
    expire=300,
    key_builder=universal_list_key_builder,  # type: ignore
    namespace=settings.cache.namespace.boats_list,
)
async def get_boats(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[BoatRead]:
    """
    ## Получение всех катеров.

    **Описание:**
    Используется для получения всех катеров в админ-панели и на сайте.

    **Ответы:**
    - `200 OK` — список найден. Возвращает список катеров.
    - `404 Not Found` — список пуст.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = ProductsService(session=session, product_db=Boat)
    all_boats = await _service.get_products()
    return [BoatRead.model_validate(boat) for boat in all_boats]


@router.get(
    path="/summary",
    response_model=list[BoatSummarySchema],
    status_code=status.HTTP_200_OK,
    operation_id="get_boats_summary",
    summary="Получение краткой информации о всех катерах",
    responses={
        200: {"model": list[BoatSummarySchema]},
        404: {"description": "Список пуст."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
@cache(
    expire=300,
    key_builder=universal_list_key_builder,  # type: ignore
    namespace=settings.cache.namespace.boats_list,
)
async def get_boats_summary(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[BoatSummarySchema]:
    """
    ## Получение краткой информации о всех катерах.

    **Описание:**
    Используется для отображения списка катеров на главной или в каталоге.
    В данных только одно изображение для каждого катера.

    **Ответы:**
    - `200 OK` — список найден. Возвращает краткие объекты катеров.
    - `404 Not Found` — список пуст.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = ProductsService(session=session, product_db=Boat)
    all_boats = await _service.get_products()
    return [
        BoatSummarySchema.model_validate(
            {
                **boat.__dict__,
                "image": boat.images[0] if boat.images else None,
            }
        )
        for boat in all_boats
    ]


@router.patch(
    path="/{boat_id}",
    response_model=BoatRead,
    status_code=status.HTTP_200_OK,
    operation_id="update_boat_data_by_id",
    summary="Частичное обновление данных катера по id",
    responses={
        200: {"model": BoatRead},
        400: {"description": "Имя уже занято или данные некорректны."},
        404: {"description": "Катер с таким id не найден."},
        422: {"description": "Ошибка валидации входных данных."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def update_boat_data_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    boat_id: int,
    boat_data: BoatUpdate,
) -> BoatRead:
    """
    ## Частичное обновление данных катера, кроме изображений.

    **Описание:**
    Используется для частичного обновления данных катера в админ-панели.

    **Принимает поля:**
    - `boat_id`: ID катера (int, целое число), для изменения.
    - `name`: Название модели (str, 1–255 символов, уникальное). Если не указано, не изменяется.
    - `price`: Цена в рублях (int, цена > 0). Если не указано, не изменяется.
    - `company_name`: Название производителя (str, 1–100 символов). Если не указано, не изменяется.
    - `description`: Описание товара (str, может быть пустым). Если не указано, не изменяется.
    - `is_active`: Наличие товара (bool). Если не указано, не изменяется.
    - `length_hull`: Длина катера в см (int, 30000 > длинна > 0). Если не указано, не изменяется.
    - `width_hull`: Ширина катера в см (int, 10000 > ширина > 0). Если не указано, не изменяется.
    - `weight`: Вес катера в кг (int, 32767 > вес > 0). Если не указано, не изменяется.
    - `capacity`: Максимальная вместимость (человек) (int, 100 > человек > 0). Если не указано, не изменяется.
    - 'maximum_load': Максимальная грузоподъемность (кг) (int, 5000 > грузоподъемность > 0). Если не указано, не изменяется.
    - 'hull_material': Материал корпуса (str, 1–50 символов). Если не указано, не изменяется.
    - 'thickness_side_sheet': Толщина бортового листа (мм) (int, 1000 > толщина > 0). Если не указано, не изменяется.
    - 'bottom_sheet_thickness': Толщина днищевого листа (мм) (int, 1000 > толщина > 0). Если не указано, не изменяется.
    - 'fuel_capacity': Объем топливного бака (л) (int, 1000 > объем > 0). Если не указано, не изменяется.
    - `maximum_engine_power`: Максимальная мощность двигателя (л.с.) (int, 10000 > мощность > 0). Если не указано, не изменяется.
    - 'height_side_midship': Высота борта на миделе (мм) (int, 10000 > высота > 0). Если не указано, не изменяется.
    - 'transom_height': Высота транца (мм) (int, 1000 > высота > 0). Если не указано, не изменяется.

    **Ответы:**
    - `200 OK` — катер успешно обновлён. Возвращает обновлённый катер.
    - `400 Bad Request` — имя занято или данные некорректны.
    - `404 Not Found` — катер не найден.
    - `422 Unprocessable Entity` — ошибка валидации.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = ProductsService(session=session, product_db=Boat)
    boat = await _service.update_product_data_by_id(
        product_id=boat_id,
        product_data=boat_data,
    )
    await FastAPICache.clear(namespace=settings.cache.namespace.boats_list)
    await FastAPICache.clear(namespace=settings.cache.namespace.boat)
    return BoatRead.model_validate(boat)


@router.patch(
    path="/images/{boat_id}",
    response_model=BoatRead,
    status_code=status.HTTP_200_OK,
    operation_id="update_boat_images_by_id",
    summary="Обновление изображений катера по id",
    responses={
        200: {"model": BoatRead},
        404: {"description": "Катер или изображения не найдены."},
        422: {"description": "Некорректный формат ID изображений."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def update_boat_images_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    boat_id: int,
    remove_images: str | None = Form(
        None,
        description="Список id изображений для удаления (через запятую, без пробелов)",
    ),
    add_images: list[UploadFile] = File(
        ...,
        description="Новые изображения для товара",
    ),
) -> BoatRead:
    """
    ## Обновление изображений катера.

    **Описание:**
    Используется для обновления изображений катера в админ-панели.

    **Принимает поля:**
    - `boat_id`: ID катера (int, целое число), у которого изменяются изображения.
    - `remove_images`: Строка с ID изображений (через запятую, без пробелов), которые нужно удалить (может быть пустой).
    - `add_images`: Список новых изображений (множественная загрузка, зажимая shift и выбирая фото, формат: image/*).

    **Ответы:**
    - `200 OK` — успешно обновлено. Возвращает обновлённый катер.
    - `404 Not Found` — катер или изображения не найдены.
    - `422 Unprocessable Entity` — некорректный формат ID изображений.
    - `500 Internal Server Error` — внутренняя ошибка сервера (например, файл не найден).
    """
    _service = ProductsService(session=session, product_db=Boat)
    boat = await _service.update_product_images_by_id(
        product_id=boat_id,
        remove_images=remove_images,
        add_images=add_images,
    )
    await FastAPICache.clear(namespace=settings.cache.namespace.boats_list)
    await FastAPICache.clear(namespace=settings.cache.namespace.boat)
    return BoatRead.model_validate(boat)


@router.delete(
    path="/{boat_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="delete_boat_by_id",
    summary="Удаление катера по id",
    responses={
        204: {"description": "Катер успешно удалён, ответ пуст."},
        404: {"description": "Катер не найден."},
        422: {"description": "Некорректный формат ID."},
        500: {"description": "Внутренняя ошибка сервера (например, файлы не найдены)."},
    },
)
async def delete_boat_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    boat_id: int,
) -> None:
    """
    ## Удаление катера по id.

    **Описание:**
    Используется для удаления катера в админ-панели.

    **Принимает поле:**
    - `boat_id`: ID катера (int, целое число), для удаления.

    **Ответы:**
    - `204 No Content` — катер успешно удалён. Ничего не возвращается.
    - `404 Not Found` — катер не найден.
    - `422 Unprocessable Entity` — некорректный ID.
    - `500 Internal Server Error` — внутренняя ошибка сервера (например, файлы не найдены).
    """
    _service = ProductsService(session=session, product_db=Boat)
    delete_boat = await _service.delete_product_by_id(product_id=boat_id)
    await FastAPICache.clear(namespace=settings.cache.namespace.boats_list)
    await FastAPICache.clear(namespace=settings.cache.namespace.boat)
    return delete_boat
