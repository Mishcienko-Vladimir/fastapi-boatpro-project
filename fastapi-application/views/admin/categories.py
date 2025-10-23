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
