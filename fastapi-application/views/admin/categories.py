from typing import Annotated, Optional

from fastapi import Form, HTTPException
from fastapi import APIRouter, Request, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.routers.products.categories import (
    get_categories,
    create_category,
    update_category_by_id,
    delete_category_by_id,
)

from core.dependencies import get_db_session
from core.dependencies.fastapi_users import current_active_superuser

from core.config import settings
from core.models import User
from core.schemas.products.category import CategoryUpdate, CategoryCreate

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
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
):
    categories_list = await get_categories(session=session)
    return templates.TemplateResponse(
        request=request,
        name="admin/categories.html",
        context={
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
    session: Annotated[AsyncSession, Depends(get_db_session)],
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
        request=request,
        name="admin/categories.html",
        context={
            "user": user,
            "categories_list": await get_categories(session=session),
            "message": message,
        },
    )


@router.post(
    path="/update-category",
    name="admin_update_category",
    include_in_schema=False,
    response_model=None,
)
async def admin_update_category(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    category_id_up: int = Form(...),
    new_name: Optional[str] = Form(None),
    new_description: Optional[str] = Form(None),
):
    try:
        update_data = {}
        if new_name is not None and new_name.strip() != "":
            update_data["name"] = new_name
        if new_description is not None and new_description.strip() != "":
            update_data["description"] = new_description

        if not update_data:
            message = "Нет данных для обновления."
        else:
            category_data = CategoryUpdate(**update_data)
            await update_category_by_id(
                session=session,
                category_id=category_id_up,
                category_data=category_data,
            )
            message = f"Категория с ID {category_id_up} успешно обновлена."

    except Exception as exc:
        message = f"Ошибка при обновлении категории: {str(exc)}"

    return templates.TemplateResponse(
        request=request,
        name="admin/categories.html",
        context={
            "user": user,
            "categories_list": await get_categories(session=session),
            "message": message,
        },
    )


@router.post(
    path="/delete-category",
    name="admin_delete_category",
    include_in_schema=False,
    response_model=None,
)
async def admin_delete_category(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    category_id_del: int = Form(...),
):
    try:
        await delete_category_by_id(session=session, category_id=category_id_del)
        message = f"Категория с ID {category_id_del} успешно удалена."
    except Exception as exc:
        message = f"Ошибка при удалении категории: {str(exc)}"

    return templates.TemplateResponse(
        request=request,
        name="admin/categories.html",
        context={
            "user": user,
            "categories_list": await get_categories(session=session),
            "message": message,
        },
    )
