from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.products import CategoryService

from core.schemas.products import CategoryCreate, CategoryRead, CategoryUpdate
from core.dependencies import get_db_session


router = APIRouter(tags=["Каталог 📋"])


@router.post("/", status_code=201, response_model=CategoryRead)
async def create_category(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    category_data: CategoryCreate,
) -> CategoryRead:
    _service = CategoryService(session)
    return await _service.create_category(category_data)


@router.get(
    "/category-name/{name_category}", status_code=200, response_model=CategoryRead
)
async def get_category_by_name(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    name_category: str,
) -> CategoryRead:
    _service = CategoryService(session)
    return await _service.get_category_by_name(name_category)


@router.get("/category-id/{category_id}", status_code=200, response_model=CategoryRead)
async def get_category_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    category_id: int,
) -> CategoryRead:
    _service = CategoryService(session)
    return await _service.get_category_by_id(category_id)


@router.get("/", status_code=200, response_model=list[CategoryRead])
async def get_categories(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[CategoryRead]:
    _service = CategoryService(session)
    return await _service.get_categories()


@router.patch("/{category_id}", status_code=200, response_model=CategoryRead)
async def update_category_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    category_id: int,
    category_data: CategoryUpdate,
) -> CategoryRead:
    _service = CategoryService(session)
    return await _service.update_category_by_id(category_id, category_data)


@router.delete("/{category_id}", status_code=204)
async def delete_category_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    category_id: int,
) -> None:
    _service = CategoryService(session)
    return await _service.delete_category_by_id(category_id)
