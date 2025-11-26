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
from core.models.products import OutboardMotor
from core.schemas.products import (
    OutboardMotorRead,
    OutboardMotorUpdate,
    OutboardMotorCreate,
    OutboardMotorSummarySchema,
)

from utils.key_builder import (
    universal_list_key_builder,
    get_by_name_key_builder,
    get_by_id_key_builder,
)


router = APIRouter(
    prefix=settings.api.v1.outboard_motors,
    tags=["Лодочные моторы 🔧"],
)


@router.post(
    path="/",
    response_model=OutboardMotorRead,
    status_code=status.HTTP_201_CREATED,
    operation_id="create_outboard_motor",
    summary="Создание нового лодочного мотора",
    responses={
        201: {"model": OutboardMotorRead},
        400: {"description": "Имя уже занято или данные некорректны."},
        422: {"description": "Ошибка валидации входных данных."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def create_outboard_motor(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    outboard_motor_data: Annotated[
        OutboardMotorCreate,
        Depends(create_multipart_form_data(OutboardMotorCreate)),
    ],
    images: Annotated[
        list[UploadFile],
        File(..., description="Изображения товара"),
    ],
) -> OutboardMotorRead:
    """
    ## Создание нового лодочного мотора.

    **Описание:**
    Используется для создания нового лодочного мотора в админ-панели.

    **Принимает поля:**
    - `category_id`: ID категории товара (int, id > 0).
    - `name`: Название модели (str, 1–255 символов, уникальное).
    - `price`: Цена в рублях (int, цена > 0).
    - `company_name`: Название производителя (str, 1–100 символов).
    - `description`: Описание товара (str, может быть пустым).
    - `is_active`: Наличие товара (bool).
    - `engine_power`: Мощность двигателя в л.с. (int, 1000 > мощность > 0).
    - `engine_type`: Тип двигателя (двухтактный / четырехтактный).
    - `weight`: Вес мотора в (кг) (int, 1000 > вес > 0).
    - `number_cylinders`: Количество цилиндров (int, 100 > цилиндров > 0).
    - `engine_displacement`: Объем двигателя в (куб.см) (int, 10000 > объем > 0).
    - `control_type`: Тип управления (румпельное / дистанционное).
    - `starter_type`: Тип стартера (ручной / электрический).
    - `images`: Список изображений товара (множественная загрузка, формат: image/*).

    **Ответы:**
    - `201 Created` — мотор успешно создан. Возвращает созданный мотор.
    - `400 Bad Request` — имя занято или данные некорректны.
    - `422 Unprocessable Entity` — ошибка валидации входных данных.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = ProductsService(session=session, product_db=OutboardMotor)
    new_outboard_motor = await _service.create_product(
        product_data=outboard_motor_data,
        images=images,
    )
    await FastAPICache.clear(namespace=settings.cache.namespace.outboard_motors_list)
    await FastAPICache.clear(namespace=settings.cache.namespace.outboard_motor)
    return OutboardMotorRead.model_validate(new_outboard_motor)


@router.get(
    path="/outboard-motor-name/{outboard_motor_name}",
    response_model=OutboardMotorRead,
    status_code=status.HTTP_200_OK,
    operation_id="get_outboard_motor_by_name",
    summary="Получение лодочного мотора по названию",
    responses={
        200: {"model": OutboardMotorRead},
        404: {"description": "Мотор не найден."},
        422: {"description": "Некорректный формат названия мотора"},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
@cache(
    expire=300,
    key_builder=get_by_name_key_builder,  # type: ignore
    namespace=settings.cache.namespace.outboard_motor,
)
async def get_outboard_motor_by_name(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    outboard_motor_name: str,
) -> OutboardMotorRead:
    """
    ## Получение лодочного мотора по названию.

    **Описание:**
    Используется для получения мотора по его названию в админ-панели и на сайте.

    **Принимает поле:**
    - `outboard_motor_name`: Название мотора (str, 1–255 символов).

    **Ответы:**
    - `200 OK` — мотор успешно найден. Возвращает объект мотора.
    - `404 Not Found` — мотор не найден.
    - `422 Unprocessable Entity` — некорректный формат имени.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = ProductsService(session=session, product_db=OutboardMotor)
    outboard_motor = await _service.get_product_by_name(
        product_name=outboard_motor_name,
    )
    return OutboardMotorRead.model_validate(outboard_motor)


@router.get(
    path="/outboard-motor-id/{outboard_motor_id}",
    response_model=OutboardMotorRead,
    status_code=status.HTTP_200_OK,
    operation_id="get_outboard_motor_by_id",
    summary="Получение лодочного мотора по id",
    responses={
        200: {"model": OutboardMotorRead},
        404: {"description": "Мотор не найден."},
        422: {"description": "Некорректный формат id"},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
@cache(
    expire=300,
    key_builder=get_by_id_key_builder,  # type: ignore
    namespace=settings.cache.namespace.outboard_motor,
)
async def get_outboard_motor_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    outboard_motor_id: int,
) -> OutboardMotorRead:
    """
    ## Получение лодочного мотора по id.

    **Описание:**
    Используется для получения мотора по его ID в админ-панели и на сайте.

    **Принимает поле:**
    - `outboard_motor_id`: ID мотора (int, целое число).

    **Ответы:**
    - `200 OK` — мотор успешно найден. Возвращает объект мотора.
    - `404 Not Found` — мотор не найден.
    - `422 Unprocessable Entity` — некорректный формат ID.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = ProductsService(session=session, product_db=OutboardMotor)
    outboard_motor = await _service.get_product_by_id(product_id=outboard_motor_id)
    return OutboardMotorRead.model_validate(outboard_motor)


@router.get(
    path="/",
    response_model=list[OutboardMotorRead],
    status_code=status.HTTP_200_OK,
    operation_id="get_outboard_motors",
    summary="Получение всех лодочных моторов",
    responses={
        200: {"model": list[OutboardMotorRead]},
        404: {"description": "Список пуст."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
@cache(
    expire=300,
    key_builder=universal_list_key_builder,  # type: ignore
    namespace=settings.cache.namespace.outboard_motors_list,
)
async def get_outboard_motors(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[OutboardMotorRead]:
    """
    ## Получение всех лодочных моторов.

    **Описание:**
    Используется для получения всех моторов в админ-панели и на сайте.

    **Ответы:**
    - `200 OK` — список найден. Возвращает список моторов.
    - `404 Not Found` — список пуст.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = ProductsService(session=session, product_db=OutboardMotor)
    all_outboard_motors = await _service.get_products()
    return [OutboardMotorRead.model_validate(motor) for motor in all_outboard_motors]


@router.get(
    path="/summary",
    response_model=list[OutboardMotorSummarySchema],
    status_code=status.HTTP_200_OK,
    operation_id="get_outboard_motors_summary",
    summary="Получение краткой информации о всех лодочных моторах",
    responses={
        200: {"model": list[OutboardMotorSummarySchema]},
        404: {"description": "Список пуст."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
@cache(
    expire=300,
    key_builder=universal_list_key_builder,  # type: ignore
    namespace=settings.cache.namespace.outboard_motors_list,
)
async def get_outboard_motors_summary(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[OutboardMotorSummarySchema]:
    """
    ## Получение краткой информации о всех лодочных моторах.

    **Описание:**
    Используется для отображения списка моторов на главной или в каталоге.
    В данных только одно изображение для каждого мотора.

    **Ответы:**
    - `200 OK` — список найден. Возвращает краткие объекты моторов.
    - `404 Not Found` — список пуст.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = ProductsService(session=session, product_db=OutboardMotor)
    all_outboard_motors = await _service.get_products()
    return [
        OutboardMotorSummarySchema.model_validate(
            {
                **outboard_motor.__dict__,
                "image": outboard_motor.images[0] if outboard_motor.images else None,
            }
        )
        for outboard_motor in all_outboard_motors
    ]


@router.patch(
    path="/{outboard_motor_id}",
    response_model=OutboardMotorRead,
    status_code=status.HTTP_200_OK,
    operation_id="update_outboard_motor_data_by_id",
    summary="Частичное обновление данных лодочного мотора по id",
    responses={
        200: {"model": OutboardMotorRead},
        400: {"description": "Имя уже занято или данные некорректны."},
        404: {"description": "Мотор с таким id не найден."},
        422: {"description": "Ошибка валидации входных данных."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def update_outboard_motor_data_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    outboard_motor_id: int,
    outboard_motor_data: OutboardMotorUpdate,
) -> OutboardMotorRead:
    """
    ## Частичное обновление данных лодочного мотора, кроме изображений.

    **Описание:**
    Используется для частичного обновления данных мотора в админ-панели.

    **Принимает поля:**
    - `outboard_motor_id`: ID мотора (int, целое число), для изменения.
    - `name`: Название модели (str, 1–255 символов, уникальное). Если не указано, не изменяется.
    - `price`: Цена в рублях (int, цена > 0). Если не указано, не изменяется.
    - `company_name`: Название производителя (str, 1–100 символов). Если не указано, не изменяется.
    - `description`: Описание товара (str, может быть пустым). Если не указано, не изменяется.
    - `is_active`: Наличие товара (bool). Если не указано, не изменяется.
    - `engine_power`: Мощность двигателя в л.с. (int, 1000 > мощность > 0). Если не указано, не изменяется.
    - `engine_type`: Тип двигателя. Если не указано, не изменяется.
    - `weight`: Вес мотора в кг (int, 1000 > вес > 0). Если не указано, не изменяется.
    - `number_cylinders`: Количество цилиндров (int, 100 > цилиндров > 0). Если не указано, не изменяется.
    - `engine_displacement`: Объем двигателя в куб.см (int, 10000 > объем > 0). Если не указано, не изменяется.
    - `control_type`: Тип управления. Если не указано, не изменяется.
    - `starter_type`: Тип стартера. Если не указано, не изменяется.

    **Ответы:**
    - `200 OK` — мотор успешно обновлён. Возвращает обновлённый мотор.
    - `400 Bad Request` — имя занято или данные некорректны.
    - `404 Not Found` — мотор не найден.
    - `422 Unprocessable Entity` — ошибка валидации.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = ProductsService(session=session, product_db=OutboardMotor)
    outboard_motor = await _service.update_product_data_by_id(
        product_id=outboard_motor_id,
        product_data=outboard_motor_data,
    )
    await FastAPICache.clear(namespace=settings.cache.namespace.outboard_motors_list)
    await FastAPICache.clear(namespace=settings.cache.namespace.outboard_motor)
    return OutboardMotorRead.model_validate(outboard_motor)


@router.patch(
    path="/images/{outboard_motor_id}",
    response_model=OutboardMotorRead,
    status_code=status.HTTP_200_OK,
    operation_id="update_outboard_motor_images_by_id",
    summary="Обновление изображений лодочного мотора по id",
    responses={
        200: {"model": OutboardMotorRead},
        404: {"description": "Мотор или изображения не найдены."},
        422: {"description": "Некорректный формат ID изображений."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def update_outboard_motor_images_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    outboard_motor_id: int,
    remove_images: str | None = Form(
        None,
        description="Список id изображений для удаления (через запятую, без пробелов)",
    ),
    add_images: list[UploadFile] = File(
        ...,
        description="Новые изображения для товара",
    ),
) -> OutboardMotorRead:
    """
    ## Обновление изображений лодочного мотора.

    **Описание:**
    Используется для обновления изображений мотора в админ-панели.

    **Принимает поля:**
    - `outboard_motor_id`: ID мотора (int, целое число), у которого изменяются изображения.
    - `remove_images`: Строка с ID изображений (через запятую, без пробелов), которые нужно удалить (может быть пустой).
    - `add_images`: Список новых изображений (множественная загрузка (зажав shift, выбрать фото) , формат: image/*).

    **Ответы:**
    - `200 OK` — успешно обновлено. Возвращает обновлённый мотор.
    - `404 Not Found` — мотор или изображения не найдены.
    - `422 Unprocessable Entity` — некорректный формат ID изображений.
    - `500 Internal Server Error` — внутренняя ошибка сервера (например, файл не найден).
    """
    _service = ProductsService(session=session, product_db=OutboardMotor)
    outboard_motor = await _service.update_product_images_by_id(
        product_id=outboard_motor_id,
        remove_images=remove_images,
        add_images=add_images,
    )
    await FastAPICache.clear(namespace=settings.cache.namespace.outboard_motors_list)
    await FastAPICache.clear(namespace=settings.cache.namespace.outboard_motor)
    return OutboardMotorRead.model_validate(outboard_motor)


@router.delete(
    path="/{outboard_motor_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="delete_outboard_motor_by_id",
    summary="Удаление лодочного мотора по id",
    responses={
        204: {"description": "Мотор успешно удалён, ответ пуст."},
        404: {"description": "Мотор не найден."},
        422: {"description": "Некорректный формат ID."},
        500: {"description": "Внутренняя ошибка сервера (например, файлы не найдены)."},
    },
)
async def delete_outboard_motor_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    outboard_motor_id: int,
) -> None:
    """
    ## Удаление лодочного мотора по id.

    **Описание:**
    Используется для удаления мотора в админ-панели.

    **Принимает поле:**
    - `outboard_motor_id`: ID мотора (int, целое число), для удаления.

    **Ответы:**
    - `204 No Content` — мотор успешно удалён. Ничего не возвращается.
    - `404 Not Found` — мотор не найден.
    - `422 Unprocessable Entity` — некорректный ID.
    - `500 Internal Server Error` — внутренняя ошибка сервера (например, файлы не найдены).
    """
    _service = ProductsService(session=session, product_db=OutboardMotor)
    delete_motor = await _service.delete_product_by_id(product_id=outboard_motor_id)
    await FastAPICache.clear(namespace=settings.cache.namespace.outboard_motors_list)
    await FastAPICache.clear(namespace=settings.cache.namespace.outboard_motor)
    return delete_motor
