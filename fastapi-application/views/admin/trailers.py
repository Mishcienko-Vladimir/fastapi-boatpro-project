from typing import Annotated, Optional

from fastapi import Form, HTTPException, File, UploadFile
from fastapi import APIRouter, Request, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.routers.products.trailers import (
    get_trailers,
    create_trailer,
    update_trailer_data_by_id,
    update_trailer_images_by_id,
    delete_trailer_by_id,
)

from core.repositories.authentication.fastapi_users import current_active_superuser
from core.config import settings
from core.models import User, db_helper
from core.schemas.products.trailer import TrailerUpdate

from utils.templates import templates


router = APIRouter(prefix=settings.view.trailers)


@router.get(
    path="/",
    name="admin_trailers",
    include_in_schema=False,
    response_model=None,
)
async def admin_trailers(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
):
    trailers_list = await get_trailers(session=session)
    return templates.TemplateResponse(
        name="admin/trailers.html",
        context={
            "request": request,
            "user": user,
            "trailers_list": trailers_list,
        },
    )
