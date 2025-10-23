from typing import Annotated, Optional

from fastapi import Form, HTTPException, File, UploadFile
from fastapi import APIRouter, Request, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.routers.products.categories import (
    get_categories,
    create_category,
    update_category_by_id,
    delete_category_by_id,
)

from core.repositories.authentication.fastapi_users import current_active_superuser
from core.config import settings
from core.models import User, db_helper
from core.schemas.products.category import CategoryRead

from utils.templates import templates


router = APIRouter(prefix=settings.view.catalog)


@router.get(
    path="/",
    name="admin_categories",
    include_in_schema=False,
    response_model=None,
)
async def admin_categories(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
):
    categories_list = await get_categories(session=session)
    return templates.TemplateResponse(
        name="admin/categories.html",
        context={
            "request": request,
            "user": user,
            "categories_list": categories_list,
        },
    )


@router.post(
    path="/create-category",
    name="admin_create_category",
    include_in_schema=False,
    response_model=None,
)
async def admin_create_category(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    category_name: str = Form(...),
    category_description: Optional[str] = Form(None),
):
    try:
        category_data = CategoryCreate(
            name=category_name, description=category_description
        )
        new_category = await create_category(
            session=session, category_data=category_data
        )
        message = f"Категория '{new_category.name}' успешно создана."
    except HTTPException as exc:
        message = f"Категория с именем '{category_name}' уже существует."
    except Exception as e:
        message = f"Ошибка при создании категории: {str(e)}"

    return templates.TemplateResponse(
        "admin/categories.html",
        {
            "request": request,
            "user": user,
            "categories_list": await get_categories(session=session),
            "message": message,
        },
    )

