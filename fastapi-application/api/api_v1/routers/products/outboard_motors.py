from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, Form, File
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.products import ProductsService

from core.config import settings
from core.models import db_helper
from core.models.products import OutboardMotor
from core.schemas.products import (
    EngineType,
    OutboardMotorRead,
    OutboardMotorUpdate,
    OutboardMotorCreate,
    OutboardMotorSummarySchema,
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
    images: list[UploadFile] = File(
        ...,
        description="Изображения товара",
    ),
) -> OutboardMotorRead:
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
    }
    outboard_motor_data = OutboardMotorCreate(**outboard_motor_data_json)
    _service = ProductsService(session, OutboardMotor)
    new_outboard_motor = await _service.create_product(outboard_motor_data, images)
    return OutboardMotorRead.model_validate(new_outboard_motor)


@router.get(
    "/outboard-motor-name/{outboard_motor_name}",
    status_code=200,
    response_model=OutboardMotorRead,
)
async def get_outboard_motor_by_name(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    outboard_motor_name: str,
) -> OutboardMotorRead:
    _service = ProductsService(session, OutboardMotor)
    outboard_motor = await _service.get_product_by_name(outboard_motor_name)
    return OutboardMotorRead.model_validate(outboard_motor)


@router.get(
    "/outboard-motor-id/{outboard_motor_id}",
    status_code=200,
    response_model=OutboardMotorRead,
)
async def get_outboard_motor_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    outboard_motor_id: int,
) -> OutboardMotorRead:
    _service = ProductsService(session, OutboardMotor)
    outboard_motor = await _service.get_product_by_id(outboard_motor_id)
    return OutboardMotorRead.model_validate(outboard_motor)


@router.get(
    "/",
    status_code=200,
    response_model=list[OutboardMotorRead],
)
async def get_outboard_motors(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[OutboardMotorRead]:
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
    _service = ProductsService(session, OutboardMotor)
    outboard_motor = await _service.update_product_data_by_id(
        outboard_motor_id, outboard_motor_data
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
    _service = ProductsService(session, OutboardMotor)
    outboard_motor = await _service.update_product_images_by_id(
        outboard_motor_id,
        remove_images,
        add_images,
    )
    return OutboardMotorRead.model_validate(outboard_motor)


@router.delete("/{outboard_motor_id}", status_code=204)
async def delete_outboard_motor_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    outboard_motor_id: int,
) -> None:
    _service = ProductsService(session, OutboardMotor)
    return await _service.delete_product_by_id(outboard_motor_id)
