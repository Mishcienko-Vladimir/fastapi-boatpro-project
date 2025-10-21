from typing import Annotated
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.routers.products.boats import (
    get_boats,
    create_boat,
    update_boat_data_by_id,
    update_boat_images_by_id,
    delete_boat_by_id,
)

from core.repositories.authentication.fastapi_users import current_active_superuser
from core.config import settings
from core.models import User, db_helper

from utils.templates import templates


router = APIRouter(
    prefix=settings.view.admin,
)


@router.get(
    "/",
    name="admin",
    include_in_schema=False,
    response_model=None,
)
def admin(
    request: Request,
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
):
    return templates.TemplateResponse(
        name="admin/admin-base.html",
        context={
            "request": request,
            "user": user,
        },
    )


@router.get(
    path=settings.view.boats,
    name="admin_boats",
    include_in_schema=False,
    response_model=None,
)
async def admin_boats(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
):
    boats_list = await get_boats(session=session)
    return templates.TemplateResponse(
        name="admin/boats.html",
        context={
            "request": request,
            "user": user,
            "boats_list": boats_list,
        },
    )
