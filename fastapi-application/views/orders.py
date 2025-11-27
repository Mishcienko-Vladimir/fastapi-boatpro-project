from typing import Annotated, Optional
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.routers.orders import get_user_orders

from core.dependencies import get_db_session
from core.dependencies.fastapi_users import optional_user

from core.config import settings
from core.models import User

from utils.templates import templates


router = APIRouter(
    prefix=settings.view.orders,
)


@router.get(
    "/",
    name="orders",
    include_in_schema=False,
)
async def orders(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Optional[User] = Depends(optional_user),
):
    if not user:
        return templates.TemplateResponse(
            request=request,
            name="favorites_and_orders/please-log.html",
            context={
                "user": user,
            },
        )

    orders_list = await get_user_orders(session=session, user=user)
    return templates.TemplateResponse(
        request=request,
        name="favorites_and_orders/orders.html",
        context={
            "user": user,
            "orders_list": orders_list,
        },
    )
