from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, Form, File, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from api.api_v1.dependencies.create_multipart_form_data import (
    create_multipart_form_data,
)
from api.api_v1.services.products import ProductsService

from core.config import settings
from core.dependencies import get_db_session
from core.models.products import Trailer
from core.schemas.products import (
    TrailerRead,
    TrailerUpdate,
    TrailerCreate,
    TrailerSummarySchema,
)

from utils.key_builder import (
    universal_list_key_builder,
    get_by_name_key_builder,
    get_by_id_key_builder,
)


router = APIRouter(
    prefix=settings.api.v1.trailers,
    tags=["Прицепы 🚛"],
)


@router.post(
    path="/",
    response_model=TrailerRead,
    status_code=status.HTTP_201_CREATED,
    operation_id="create_trailer",
    summary="Создание нового прицепа",
    responses={
        201: {"model": TrailerRead},
        400: {"description": "Имя уже занято или данные некорректны."},
        422: {"description": "Ошибка валидации входных данных."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def create_trailer(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    trailer_data: Annotated[
        TrailerCreate,
        Depends(create_multipart_form_data(TrailerCreate)),
    ],
    images: Annotated[
        list[UploadFile],
        File(..., description="Изображения товара"),
    ],
) -> TrailerRead:
    """
    ## Создание нового прицепа.

    **Описание:**
    Используется для создания нового прицепа в админ-панели.

    **Принимает поля:**
    - `category_id`: ID категории товара (int, id > 0).
    - `name`: Название модели (str, 1–255 символов, уникальное).
    - `price`: Цена в рублях (int, цена > 0).
    - `company_name`: Название производителя (str, 1–100 символов).
    - `description`: Описание товара (str, может быть пустым).
    - `is_active`: Наличие товара (bool).
    - `full_mass`: Полный вес прицепа в кг (int, 32767 > вес > 0).
    - `load_capacity`: Грузоподъемность в кг (int, 32767 > грузоподъемность > 0).
    - `trailer_length`: Длина прицепа в см (int, 32767 > длина > 0).
    - `max_ship_length`: Максимальная длина перевозимого судна в см (int, 32767 > длина > 0).
    - `images`: Список изображений товара (множественная загрузка, формат: image/*).

    **Ответы:**
    - `201 Created` — прицеп успешно создан. Возвращает созданный прицеп.
    - `400 Bad Request` — имя занято или данные некорректны.
    - `422 Unprocessable Entity` — ошибка валидации входных данных.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = ProductsService(session=session, product_db=Trailer)
    new_trailer = await _service.create_product(
        product_data=trailer_data,
        images=images,
    )
    await FastAPICache.clear(namespace=settings.cache.namespace.trailers_list)
    await FastAPICache.clear(namespace=settings.cache.namespace.trailer)
    return TrailerRead.model_validate(new_trailer)


@router.get(
    path="/trailer-name/{trailer_name}",
    response_model=TrailerRead,
    status_code=status.HTTP_200_OK,
    operation_id="get_trailer_by_name",
    summary="Получение прицепа по названию",
    responses={
        200: {"model": TrailerRead},
        404: {"description": "Прицеп не найден."},
        422: {"description": "Некорректный формат названия прицепа"},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
@cache(
    expire=300,
    key_builder=get_by_name_key_builder,  # type: ignore
    namespace=settings.cache.namespace.trailer,
)
async def get_trailer_by_name(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    trailer_name: str,
) -> TrailerRead:
    """
    ## Получение прицепа по названию.

    **Описание:**
    Используется для получения прицепа по его названию в админ-панели и на сайте.

    **Принимает поле:**
    - `trailer_name`: Название прицепа (str, 1–255 символов).

    **Ответы:**
    - `200 OK` — прицеп успешно найден. Возвращает объект прицепа.
    - `404 Not Found` — прицеп не найден.
    - `422 Unprocessable Entity` — некорректный формат имени.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = ProductsService(session=session, product_db=Trailer)
    trailer = await _service.get_product_by_name(product_name=trailer_name)
    return TrailerRead.model_validate(trailer)


@router.get(
    path="/trailer-id/{trailer_id}",
    response_model=TrailerRead,
    status_code=status.HTTP_200_OK,
    operation_id="get_trailer_by_id",
    summary="Получение прицепа по id",
    responses={
        200: {"model": TrailerRead},
        404: {"description": "Прицеп не найден."},
        422: {"description": "Некорректный формат id"},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
@cache(
    expire=300,
    key_builder=get_by_id_key_builder,  # type: ignore
    namespace=settings.cache.namespace.trailer,
)
async def get_trailer_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    trailer_id: int,
) -> TrailerRead:
    """
    ## Получение прицепа по id.

    **Описание:**
    Используется для получения прицепа по его ID в админ-панели и на сайте.

    **Принимает поле:**
    - `trailer_id`: ID прицепа (int, целое число).

    **Ответы:**
    - `200 OK` — прицеп успешно найден. Возвращает объект прицепа.
    - `404 Not Found` — прицеп не найден.
    - `422 Unprocessable Entity` — некорректный формат ID.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = ProductsService(session=session, product_db=Trailer)
    trailer = await _service.get_product_by_id(product_id=trailer_id)
    return TrailerRead.model_validate(trailer)


@router.get(
    path="/",
    response_model=list[TrailerRead],
    status_code=status.HTTP_200_OK,
    operation_id="get_trailers",
    summary="Получение всех прицепов",
    responses={
        200: {"model": list[TrailerRead]},
        404: {"description": "Список пуст."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
@cache(
    expire=300,
    key_builder=universal_list_key_builder,  # type: ignore
    namespace=settings.cache.namespace.trailers_list,
)
async def get_trailers(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[TrailerRead]:
    """
    ## Получение всех прицепов.

    **Описание:**
    Используется для получения всех прицепов в админ-панели и на сайте.

    **Ответы:**
    - `200 OK` — список найден. Возвращает список прицепов.
    - `404 Not Found` — список пуст.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = ProductsService(session=session, product_db=Trailer)
    all_trailers = await _service.get_products()
    return [TrailerRead.model_validate(trailer) for trailer in all_trailers]


@router.get(
    path="/summary",
    response_model=list[TrailerSummarySchema],
    status_code=status.HTTP_200_OK,
    operation_id="get_trailers_summary",
    summary="Получение краткой информации о всех прицепах",
    responses={
        200: {"model": list[TrailerSummarySchema]},
        404: {"description": "Список пуст."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
@cache(
    expire=300,
    key_builder=universal_list_key_builder,  # type: ignore
    namespace=settings.cache.namespace.trailers_list,
)
async def get_trailers_summary(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[TrailerSummarySchema]:
    """
    ## Получение краткой информации о всех прицепах.

    **Описание:**
    Используется для отображения списка прицепов на главной или в каталоге.
    В данных только одно изображение для каждого прицепа.

    **Ответы:**
    - `200 OK` — список найден. Возвращает краткие объекты прицепов.
    - `404 Not Found` — список пуст.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = ProductsService(session=session, product_db=Trailer)
    all_trailers = await _service.get_products()
    return [
        TrailerSummarySchema.model_validate(
            {
                **trailer.__dict__,
                "image": trailer.images[0] if trailer.images else None,
            }
        )
        for trailer in all_trailers
    ]


@router.patch(
    path="/{trailer_id}",
    response_model=TrailerRead,
    status_code=status.HTTP_200_OK,
    operation_id="update_trailer_data_by_id",
    summary="Частичное обновление данных прицепа по id",
    responses={
        200: {"model": TrailerRead},
        400: {"description": "Имя уже занято или данные некорректны."},
        404: {"description": "Прицеп с таким id не найден."},
        422: {"description": "Ошибка валидации входных данных."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def update_trailer_data_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    trailer_id: int,
    trailer_data: TrailerUpdate,
) -> TrailerRead:
    """
    ## Частичное обновление данных прицепа, кроме изображений.

    **Описание:**
    Используется для частичного обновления данных прицепа в админ-панели.

    **Принимает поля:**
    - `trailer_id`: ID прицепа (int, целое число), для изменения.
    - `name`: Название модели (str, 1–255 символов, уникальное). Если не указано, не изменяется.
    - `price`: Цена в рублях (int, цена > 0). Если не указано, не изменяется.
    - `company_name`: Название производителя (str, 1–100 символов). Если не указано, не изменяется.
    - `description`: Описание товара (str, может быть пустым). Если не указано, не изменяется.
    - `is_active`: Наличие товара (bool). Если не указано, не изменяется.
    - `full_mass`: Полный вес прицепа в кг (int, 32767 > вес > 0). Если не указано, не изменяется.
    - `load_capacity`: Грузоподъемность в кг (int, 32767 > грузоподъемность > 0). Если не указано, не изменяется.
    - `trailer_length`: Длина прицепа в см (int, 32767 > длина > 0). Если не указано, не изменяется.
    - `max_ship_length`: Максимальная длина перевозимого судна в см (int, 32767 > длина > 0). Если не указано, не изменяется.

    **Ответы:**
    - `200 OK` — прицеп успешно обновлён. Возвращает обновлённый прицеп.
    - `400 Bad Request` — имя занято или данные некорректны.
    - `404 Not Found` — прицеп не найден.
    - `422 Unprocessable Entity` — ошибка валидации.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = ProductsService(session=session, product_db=Trailer)
    trailer = await _service.update_product_data_by_id(
        product_id=trailer_id,
        product_data=trailer_data,
    )
    await FastAPICache.clear(namespace=settings.cache.namespace.trailers_list)
    await FastAPICache.clear(namespace=settings.cache.namespace.trailer)
    return TrailerRead.model_validate(trailer)


@router.patch(
    path="/images/{trailer_id}",
    response_model=TrailerRead,
    status_code=status.HTTP_200_OK,
    operation_id="update_trailer_images_by_id",
    summary="Обновление изображений прицепа по id",
    responses={
        200: {"model": TrailerRead},
        404: {"description": "Прицеп или изображения не найдены."},
        422: {"description": "Некорректный формат ID изображений."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def update_trailer_images_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    trailer_id: int,
    remove_images: str | None = Form(
        None,
        description="Список id изображений для удаления (через запятую, без пробелов)",
    ),
    add_images: list[UploadFile] = File(
        ...,
        description="Новые изображения для товара",
    ),
) -> TrailerRead:
    """
    ## Обновление изображений прицепа.

    **Описание:**
    Используется для обновления изображений прицепа в админ-панели.

    **Принимает поля:**
    - `trailer_id`: ID прицепа (int, целое число), у которого изменяются изображения.
    - `remove_images`: Строка с ID изображений (через запятую, без пробелов), которые нужно удалить (может быть пустой).
    - `add_images`: Список новых изображений (множественная загрузка (зажимая shift и выбирая фото), формат: image/*).

    **Ответы:**
    - `200 OK` — успешно обновлено. Возвращает обновлённый прицеп.
    - `404 Not Found` — прицеп или изображения не найдены.
    - `422 Unprocessable Entity` — некорректный формат ID изображений.
    - `500 Internal Server Error` — внутренняя ошибка сервера (например, файл не найден).
    """
    _service = ProductsService(session=session, product_db=Trailer)
    trailer = await _service.update_product_images_by_id(
        product_id=trailer_id,
        remove_images=remove_images,
        add_images=add_images,
    )
    await FastAPICache.clear(namespace=settings.cache.namespace.trailers_list)
    await FastAPICache.clear(namespace=settings.cache.namespace.trailer)
    return TrailerRead.model_validate(trailer)


@router.delete(
    path="/{trailer_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="delete_trailer_by_id",
    summary="Удаление прицепа по id",
    responses={
        204: {"description": "Прицеп успешно удалён, ответ пуст."},
        404: {"description": "Прицеп не найден."},
        422: {"description": "Некорректный формат ID."},
        500: {"description": "Внутренняя ошибка сервера (например, файлы не найдены)."},
    },
)
async def delete_trailer_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    trailer_id: int,
) -> None:
    """
    ## Удаление прицепа по id.

    **Описание:**
    Используется для удаления прицепа в админ-панели.

    **Принимает поле:**
    - `trailer_id`: ID прицепа (int, целое число), для удаления.

    **Ответы:**
    - `204 No Content` — прицеп успешно удалён. Ничего не возвращается.
    - `404 Not Found` — прицеп не найден.
    - `422 Unprocessable Entity` — некорректный ID.
    - `500 Internal Server Error` — внутренняя ошибка сервера (например, файлы не найдены).
    """
    _service = ProductsService(session=session, product_db=Trailer)
    delete_trailer = await _service.delete_product_by_id(product_id=trailer_id)
    await FastAPICache.clear(namespace=settings.cache.namespace.trailers_list)
    await FastAPICache.clear(namespace=settings.cache.namespace.trailer)
    return delete_trailer
