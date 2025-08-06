from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import ImagePathCreate, ImagePathRead
from core.models import db_helper
from core.config import settings

from api.api_v1.services.image_path import ImagePathService


router = APIRouter(
    prefix=settings.api.v1.images,
    tags=["Изображения"],
)


@router.post("/", status_code=201, response_model=ImagePathRead)
async def create_image_path(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    image_path: ImagePathCreate,
) -> ImagePathRead:
    _service = ImagePathService(session)
    return await _service.create_image_path(image_path)


#
#
# @router.get("/", status_code=200, response_model=ProductTypeRead)
# async def get_product_type_by_name(
#     session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
#     name_product_type: str,
# ) -> ProductTypeRead:
#     _service = ProductTypeService(session)
#     return await _service.get_product_type_by_name(name_product_type)
