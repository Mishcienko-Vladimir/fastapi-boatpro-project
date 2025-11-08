from typing import Optional, Annotated

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.routers.products.outboard_motors import (
    get_outboard_motors_summary,
    get_outboard_motor_by_name,
)

from core.dependencies import get_db_session
from core.repositories.authentication.fastapi_users import optional_user
from core.config import settings
from core.models import User

from utils.templates import templates


router = APIRouter(
    prefix=settings.view.outboard_motors,
)


@router.get(
    path="/",
    name="outboard_motors",
    include_in_schema=False,
    response_model=None,
)
async def outboard_motors(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Optional[User] = Depends(optional_user),
):
    outboard_motors_list = await get_outboard_motors_summary(session=session)
    return templates.TemplateResponse(
        name="products/outboard-motors.html",
        context={
            "request": request,
            "outboard_motors_list": outboard_motors_list,
            "user": user,
        },
    )


@router.get(
    path=f"/{{outboard_motor_name}}",
    name="outboard_motor_detail",
    include_in_schema=False,
    response_model=None,
)
async def outboard_motor_detail(
    request: Request,
    outboard_motor_name: str,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Optional[User] = Depends(optional_user),
):
    outboard_motor = await get_outboard_motor_by_name(
        session=session, outboard_motor_name=outboard_motor_name
    )
    return templates.TemplateResponse(
        name="products/outboard-motor-detail.html",
        context={
            "request": request,
            "outboard_motor": outboard_motor,
            "user": user,
        },
    )
