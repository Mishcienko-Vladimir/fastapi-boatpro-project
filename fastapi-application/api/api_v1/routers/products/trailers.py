from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, Form, File

from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.products import ProductsService

from core.config import settings
from core.models import db_helper
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
    """
    Создание нового прицепа.
    """
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
    _service = ProductsService(session, Trailer)
    new_trailer = await _service.create_product(trailer_data, images)
    await FastAPICache.clear(
        namespace=settings.cache.namespace.trailers_list,
    )
    await FastAPICache.clear(
        namespace=settings.cache.namespace.trailer,
    )
    return TrailerRead.model_validate(new_trailer)


@router.get("/trailer-name/{trailer_name}", status_code=200, response_model=TrailerRead)
@cache(
    expire=300,
    key_builder=get_by_name_key_builder,
    namespace=settings.cache.namespace.trailer,
)
async def get_trailer_by_name(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    trailer_name: str,
) -> TrailerRead:
    """
    Получение прицепа по названию.
    """
    _service = ProductsService(session, Trailer)
    trailer = await _service.get_product_by_name(trailer_name)
    return TrailerRead.model_validate(trailer)


@router.get("/trailer-id/{trailer_id}", status_code=200, response_model=TrailerRead)
@cache(
    expire=300,
    key_builder=get_by_id_key_builder,
    namespace=settings.cache.namespace.trailer,
)
async def get_trailer_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    trailer_id: int,
) -> TrailerRead:
    """
    Получение прицепа по id.
    """
    _service = ProductsService(session, Trailer)
    trailer = await _service.get_product_by_id(trailer_id)
    return TrailerRead.model_validate(trailer)


@router.get("/", status_code=200, response_model=list[TrailerRead])
@cache(
    expire=300,
    key_builder=universal_list_key_builder,
    namespace=settings.cache.namespace.trailers_list,
)
async def get_trailers(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[TrailerRead]:
    """
    Получение всех прицепов.
    """
    _service = ProductsService(session, Trailer)
    all_trailers = await _service.get_products()
    return [TrailerRead.model_validate(trailer) for trailer in all_trailers]


@router.get("/summary", status_code=200, response_model=list[TrailerSummarySchema])
@cache(
    expire=300,
    key_builder=universal_list_key_builder,
    namespace=settings.cache.namespace.trailers_list,
)
async def get_trailers_summary(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[TrailerSummarySchema]:
    """
    Получает краткую информацию о всех прицепах.
    В данных только одно изображение для каждого прицепа.
    """

    _service = ProductsService(session, Trailer)
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


@router.patch("/{trailer_id}", status_code=200, response_model=TrailerRead)
async def update_trailer_data_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    trailer_id: int,
    trailer_data: TrailerUpdate,
) -> TrailerRead:
    """
    Обновление данных прицепа по id (кроме изображений).
    """
    _service = ProductsService(session, Trailer)
    trailer = await _service.update_product_data_by_id(trailer_id, trailer_data)
    await FastAPICache.clear(
        namespace=settings.cache.namespace.trailers_list,
    )
    await FastAPICache.clear(
        namespace=settings.cache.namespace.trailer,
    )
    return TrailerRead.model_validate(trailer)


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
    """
    Обновление изображений прицепа по id.
    """
    _service = ProductsService(session, Trailer)
    trailer = await _service.update_product_images_by_id(
        trailer_id,
        remove_images,
        add_images,
    )
    await FastAPICache.clear(
        namespace=settings.cache.namespace.trailers_list,
    )
    await FastAPICache.clear(
        namespace=settings.cache.namespace.trailer,
    )
    return TrailerRead.model_validate(trailer)


@router.delete("/{trailer_id}", status_code=204)
async def delete_trailer_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    trailer_id: int,
) -> None:
    """
    Удаление прицепа по id.
    """
    _service = ProductsService(session, Trailer)
    delete_trailer = await _service.delete_product_by_id(trailer_id)
    await FastAPICache.clear(
        namespace=settings.cache.namespace.trailers_list,
    )
    await FastAPICache.clear(
        namespace=settings.cache.namespace.trailer,
    )
    return delete_trailer
