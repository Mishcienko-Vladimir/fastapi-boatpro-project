from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, Form, File
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.products import TrailerService

from core.config import settings
from core.schemas.products import TrailerRead, TrailerUpdate, TrailerCreate
from core.models import db_helper


router = APIRouter(prefix=settings.api.v1.trailers, tags=["Прицепы"])


@router.post("/", status_code=201, response_model=TrailerRead)
async def create_trailer(
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
    full_mass: int = Form(
        ...,
        gt=0,
        lt=32767,
        description="Полный вес прицепа в кг",
    ),
    load_capacity: int = Form(
        ...,
        gt=0,
        lt=32767,
        description="Грузоподъемность в кг",
    ),
    trailer_length: int = Form(
        ...,
        gt=0,
        lt=32767,
        description="Длина прицепа в см",
    ),
    max_ship_length: int = Form(
        ...,
        gt=0,
        lt=32767,
        description="Максимальная длина перевозимого судна в см",
    ),
    images: list[UploadFile] = File(
        ...,
        description="Изображения товара",
    ),
) -> TrailerRead:
    trailer_data_json = {
        "category_id": category_id,
        "name": name,
        "price": price,
        "company_name": company_name,
        "description": description,
        "is_active": is_active,
        "full_mass": full_mass,
        "load_capacity": load_capacity,
        "trailer_length": trailer_length,
        "max_ship_length": max_ship_length,
    }
    trailer_data = TrailerCreate(**trailer_data_json)
    _service = TrailerService(session)
    return await _service.create_trailer(trailer_data, images)


@router.get("/trailer-name/{name_trailer}", status_code=200, response_model=TrailerRead)
async def get_trailer_by_name(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    name_trailer: str,
) -> TrailerRead:
    _service = TrailerService(session)
    return await _service.get_trailer_by_name(name_trailer)


@router.get("/trailer-id/{trailer_id}", status_code=200, response_model=TrailerRead)
async def get_trailer_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    trailer_id: int,
) -> TrailerRead:
    _service = TrailerService(session)
    return await _service.get_trailer_by_id(trailer_id)


@router.get("/", status_code=200, response_model=list[TrailerRead])
async def get_trailers(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[TrailerRead]:
    _service = TrailerService(session)
    return await _service.get_trailers()


@router.patch("/{trailer_id}", status_code=200, response_model=TrailerRead)
async def update_trailer_data_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    trailer_id: int,
    trailer_data: TrailerUpdate,
) -> TrailerRead:
    _service = TrailerService(session)
    return await _service.update_trailer_data_by_id(trailer_id, trailer_data)


@router.patch("/images/{trailer_id}", status_code=200, response_model=TrailerRead)
async def update_trailer_images_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
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
    _service = TrailerService(session)
    return await _service.update_trailer_images_by_id(
        trailer_id, remove_images, add_images
    )


@router.delete("/{trailer_id}", status_code=204)
async def delete_trailer_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    trailer_id: int,
) -> None:
    _service = TrailerService(session)
    return await _service.delete_trailer_by_id(trailer_id)
