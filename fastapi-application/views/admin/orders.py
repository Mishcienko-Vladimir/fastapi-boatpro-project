from typing import Annotated, Optional

from fastapi import Form, HTTPException, File, UploadFile
from fastapi import APIRouter, Request, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.routers.orders import get_all_orders, update_order_status

from core.dependencies import get_db_session
from core.dependencies.fastapi_users import current_active_superuser

from core.config import settings
from core.models import User
from core.models.orders.order import OrderStatus
from core.schemas.order import OrderUpdate

from utils.templates import templates


router = APIRouter(prefix=settings.view.orders)


@router.get(
    path="/",
    name="admin_orders",
    include_in_schema=False,
    response_model=None,
)
async def admin_orders(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
):
    orders_list = await get_all_orders(session=session)
    return templates.TemplateResponse(
        request=request,
        name="admin/orders.html",
        context={
            "user": user,
            "orders_list": orders_list,
        },
    )


@router.post(
    path="/update-order",
    name="admin_update_order",
    include_in_schema=False,
    response_model=None,
)
async def admin_update_order(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    order_id_up: int = Form(...),
    status: OrderStatus = Form(...),
):
    try:
        order_update = OrderUpdate(status=status)
        await update_order_status(
            session=session,
            order_id=order_id_up,
            order_update=order_update,
        )
        message = f"Заказ с ID {order_id_up} успешно обновлен"
    except HTTPException as exc:
        message = f"Заказ с ID {order_id_up} не найден"
    except Exception as exc:
        message = f"Ошибка при обновлении заказа: {str(exc)}"

    return templates.TemplateResponse(
        request=request,
        name="admin/orders.html",
        context={
            "user": user,
            "orders_list": await get_all_orders(session=session),
            "message": message,
        },
    )
