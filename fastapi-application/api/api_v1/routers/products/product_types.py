from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.products import ProductTypeCreate, ProductTypeRead
from core.models import db_helper

from api.api_v1.services.products.product_type import ProductTypeService


router = APIRouter(tags=["Каталог"])

@router.post("/", status_code=201, response_model=ProductTypeRead)
async def create_product_type(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    product_data: ProductTypeCreate,
) -> ProductTypeRead:
    _service = ProductTypeService(session)
    return await _service.create_product_type(product_data)


@router.get("/")
def get_product_types():
    return {"message": "Hello, World!"}
