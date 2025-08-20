from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, Form, File
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.products import ProductsService

from core.config import settings
from core.models import db_helper
from core.models.products import Boat
from core.schemas.products import BoatCreate, BoatUpdate, BoatRead


router = APIRouter(prefix=settings.api.v1.boats, tags=["Катера"])


@router.post("/", status_code=201, response_model=BoatRead)
async def create_boat(
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
    length_hull: int = Form(
        ...,
        gt=0,
        lt=30000,
        description="Длина корпуса в см",
    ),
    width_hull: int = Form(
        ...,
        gt=0,
        lt=10000,
        description="Ширина корпуса в см",
    ),
    weight: int = Form(
        ...,
        gt=0,
        lt=32767,
        description="Вес катера в кг",
    ),
    capacity: int = Form(
        ...,
        gt=0,
        lt=100,
        description="Количество мест",
    ),
    maximum_load: int = Form(
        ...,
        gt=0,
        lt=5000,
        description="Максимальная нагрузка в кг",
    ),
    hull_material: str = Form(
        ...,
        min_length=1,
        max_length=50,
        description="Материал корпуса",
    ),
    thickness_side_sheet: int | None = Form(
        ge=0,
        lt=1000,
        description="Толщина бортового листа в мм",
    ),
    bottom_sheet_thickness: int | None = Form(
        ge=0,
        lt=1000,
        description="Толщина днищевой листа в мм",
    ),
    fuel_capacity: int | None = Form(
        ge=0,
        lt=1000,
        description="Объём топливного бака в литрах",
    ),
    maximum_engine_power: int | None = Form(
        ge=0,
        lt=10000,
        description="Максимальная мощность двигателя в л.с.",
    ),
    height_side_midship: int | None = Form(
        ge=0,
        lt=10000,
        description="Высота борта на миделе в мм",
    ),
    transom_height: int | None = Form(
        ge=0,
        lt=1000,
        description="Высота транца в мм",
    ),
    images: list[UploadFile] = File(
        ...,
        description="Изображения товара",
    ),
) -> BoatRead:
    boat_data_json = {
        "category_id": category_id,
        "name": name,
        "price": price,
        "company_name": company_name,
        "description": description,
        "is_active": is_active,
        "length_hull": length_hull,
        "width_hull": width_hull,
        "weight": weight,
        "capacity": capacity,
        "maximum_load": maximum_load,
        "hull_material": hull_material,
        "thickness_side_sheet": thickness_side_sheet,
        "bottom_sheet_thickness": bottom_sheet_thickness,
        "fuel_capacity": fuel_capacity,
        "maximum_engine_power": maximum_engine_power,
        "height_side_midship": height_side_midship,
        "transom_height": transom_height,
    }
    boat_data = BoatCreate(**boat_data_json)
    _service = ProductsService(session, Boat)
    new_boat = await _service.create_product(boat_data, images)
    return BoatRead.model_validate(new_boat)


@router.get("/boat-name/{boat_name}", status_code=200, response_model=BoatRead)
async def get_boat_by_name(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    boat_name: str,
) -> BoatRead:
    _service = ProductsService(session, Boat)
    boat = await _service.get_product_by_name(boat_name)
    return BoatRead.model_validate(boat)
