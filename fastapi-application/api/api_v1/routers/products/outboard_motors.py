from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, Form, File

from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.products import ProductsService

from core.config import settings
from core.models import db_helper
from core.models.products import OutboardMotor
from core.schemas.products import (
    EngineType,
    ControlType,
    StarterType,
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


router = APIRouter(prefix=settings.api.v1.outboard_motors, tags=["Лодочные моторы"])


@router.post("/", status_code=201, response_model=OutboardMotorRead)
async def create_outboard_motor(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    category_id: int = Form(
        ...,
        description="ID категории товара",
    ),
    name: str = Form(
        ...,
        min_length=1,
        max_length=255,
        description="Название модели",
    ),
    price: int = Form(
        ...,
        gt=0,
        description="Цена в рублях",
    ),
    company_name: str = Form(
        ...,
        min_length=1,
        max_length=100,
        description="Название производителя",
    ),
    description: str = Form(
        ...,
        min_length=0,
        description="Описание",
    ),
    is_active: bool = Form(
        ...,
        description="Наличие товара",
    ),
    engine_power: int = Form(
        ...,
        gt=0,
        lt=1000,
        description="Мощность двигателя в л.с.",
    ),
    engine_type: EngineType = Form(
        ...,
        description="Тип двигателя",
    ),
    weight: int = Form(
        ...,
        gt=0,
        lt=1000,
        description="Вес мотора в кг",
    ),
    number_cylinders: int = Form(
        ...,
        gt=0,
        lt=100,
        description="Количество цилиндров в двигателе",
    ),
    engine_displacement: int = Form(
        ...,
        gt=0,
        lt=10000,
        description="Объем двигателя в куб.см",
    ),
    control_type: ControlType = Form(
        ...,
        description="Тип управления",
    ),
    starter_type: StarterType = Form(
        ...,
        description="Тип стартера",
    ),
    images: list[UploadFile] = File(
        ...,
        description="Изображения товара",
    ),
) -> OutboardMotorRead:
    """
    Создание нового лодочного мотора.
    """
    outboard_motor_data_json = {
        "category_id": category_id,
        "name": name,
        "price": price,
        "company_name": company_name,
        "description": description,
        "is_active": is_active,
        "engine_power": engine_power,
        "engine_type": engine_type,
        "weight": weight,
        "number_cylinders": number_cylinders,
        "engine_displacement": engine_displacement,
        "control_type": control_type,
        "starter_type": starter_type,
    }
    outboard_motor_data = OutboardMotorCreate(**outboard_motor_data_json)
    _service = ProductsService(session, OutboardMotor)
    new_outboard_motor = await _service.create_product(outboard_motor_data, images)
    await FastAPICache.clear(
        namespace=settings.cache.namespace.outboard_motors_list,
    )
    await FastAPICache.clear(
        namespace=settings.cache.namespace.outboard_motor,
    )
    return OutboardMotorRead.model_validate(new_outboard_motor)


@router.get(
    "/outboard-motor-name/{outboard_motor_name}",
    status_code=200,
    response_model=OutboardMotorRead,
)
@cache(
    expire=300,
    key_builder=get_by_name_key_builder,
    namespace=settings.cache.namespace.outboard_motor,
)
async def get_outboard_motor_by_name(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    outboard_motor_name: str,
) -> OutboardMotorRead:
    """
    Получение лодочного мотора по названию.
    """
    _service = ProductsService(session, OutboardMotor)
    outboard_motor = await _service.get_product_by_name(outboard_motor_name)
    return OutboardMotorRead.model_validate(outboard_motor)


@router.get(
    "/outboard-motor-id/{outboard_motor_id}",
    status_code=200,
    response_model=OutboardMotorRead,
)
@cache(
    expire=300,
    key_builder=get_by_id_key_builder,
    namespace=settings.cache.namespace.outboard_motor,
)
async def get_outboard_motor_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    outboard_motor_id: int,
) -> OutboardMotorRead:
    """
    Получение лодочного мотора по id.
    """
    _service = ProductsService(session, OutboardMotor)
    outboard_motor = await _service.get_product_by_id(outboard_motor_id)
    return OutboardMotorRead.model_validate(outboard_motor)


@router.get(
    "/",
    status_code=200,
    response_model=list[OutboardMotorRead],
)
@cache(
    expire=300,
    key_builder=universal_list_key_builder,
    namespace=settings.cache.namespace.outboard_motors_list,
)
async def get_outboard_motors(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[OutboardMotorRead]:
    """
    Получение всех лодочных моторов.
    """
    _service = ProductsService(session, OutboardMotor)
    all_outboard_motors = await _service.get_products()
    return [
        OutboardMotorRead.model_validate(outboard_motor)
        for outboard_motor in all_outboard_motors
    ]


@router.get(
    "/summary",
    status_code=200,
    response_model=list[OutboardMotorSummarySchema],
)
@cache(
    expire=300,
    key_builder=universal_list_key_builder,
    namespace=settings.cache.namespace.outboard_motors_list,
)
async def get_outboard_motors_summary(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[OutboardMotorSummarySchema]:
    """
    Получает краткую информацию о всех лодочных моторов.
    В данных только одно изображение для каждого мотора.
    """

    _service = ProductsService(session, OutboardMotor)
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
    "/{outboard_motor_id}",
    status_code=200,
    response_model=OutboardMotorRead,
)
async def update_outboard_motor_data_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    outboard_motor_id: int,
    outboard_motor_data: OutboardMotorUpdate,
) -> OutboardMotorRead:
    """
    Обновление данных лодочного мотора по id (кроме изображений).
    """
    _service = ProductsService(session, OutboardMotor)
    outboard_motor = await _service.update_product_data_by_id(
        outboard_motor_id, outboard_motor_data
    )
    await FastAPICache.clear(
        namespace=settings.cache.namespace.outboard_motors_list,
    )
    await FastAPICache.clear(
        namespace=settings.cache.namespace.outboard_motor,
    )
    return OutboardMotorRead.model_validate(outboard_motor)


@router.patch(
    "/images/{outboard_motor_id}",
    status_code=200,
    response_model=OutboardMotorRead,
)
async def update_outboard_motor_images_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
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
    Обновление изображений лодочного мотора по id.
    """
    _service = ProductsService(session, OutboardMotor)
    outboard_motor = await _service.update_product_images_by_id(
        outboard_motor_id,
        remove_images,
        add_images,
    )
    await FastAPICache.clear(
        namespace=settings.cache.namespace.outboard_motors_list,
    )
    await FastAPICache.clear(
        namespace=settings.cache.namespace.outboard_motor,
    )
    return OutboardMotorRead.model_validate(outboard_motor)


@router.delete("/{outboard_motor_id}", status_code=204)
async def delete_outboard_motor_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    outboard_motor_id: int,
) -> None:
    """
    Удаление лодочного мотора по id.
    """
    _service = ProductsService(session, OutboardMotor)
    delete_outboard_motor = await _service.delete_product_by_id(outboard_motor_id)
    await FastAPICache.clear(
        namespace=settings.cache.namespace.outboard_motors_list,
    )
    await FastAPICache.clear(
        namespace=settings.cache.namespace.outboard_motor,
    )
    return delete_outboard_motor
