from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.products import CategoryService

from core.schemas.products import CategoryCreate, CategoryRead
from core.models import db_helper


router = APIRouter(tags=["Каталог"])


@router.post("/", status_code=201, response_model=CategoryRead)
async def create_category(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    category_data: CategoryCreate,
) -> CategoryRead:
    _service = CategoryService(session)
    return await _service.create_category(category_data)


@router.get("/{name_category}", status_code=200, response_model=CategoryRead)
async def get_category_by_name(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    name_category: str,
) -> CategoryRead:
    _service = CategoryService(session)
    return await _service.get_category_by_name(name_category)


@router.get("/{category_id}", status_code=200, response_model=CategoryRead)
async def get_category_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    category_id: int,
) -> CategoryRead:
    _service = CategoryService(session)
    return await _service.get_category_by_id(category_id)
