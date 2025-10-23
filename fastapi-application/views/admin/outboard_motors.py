from typing import Annotated, Optional

from fastapi import Form, HTTPException, File, UploadFile
from fastapi import APIRouter, Request, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.routers.products.outboard_motors import (
    get_outboard_motors,
    create_outboard_motor,
    update_outboard_motor_data_by_id,
    update_outboard_motor_images_by_id,
    delete_outboard_motor_by_id,
)

from core.repositories.authentication.fastapi_users import current_active_superuser
from core.config import settings
from core.models import User, db_helper
from core.schemas.products.outboard_motor import (
    EngineType,
    ControlType,
    StarterType,
    OutboardMotorUpdate,
)

from utils.templates import templates


router = APIRouter(prefix=settings.view.outboard_motors)


@router.get(
    path="/",
    name="admin_outboard_motors",
    include_in_schema=False,
    response_model=None,
)
async def admin_outboard_motors(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
):
    outboard_motors_list = await get_outboard_motors(session=session)
    return templates.TemplateResponse(
        name="admin/outboard_motors.html",
        context={
            "request": request,
            "user": user,
            "outboard_motors_list": outboard_motors_list,
        },
    )
