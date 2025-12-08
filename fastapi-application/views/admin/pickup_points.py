from typing import Annotated, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Form, HTTPException
from fastapi import APIRouter, Request, Depends

from api.api_v1.routers.pickup_points import (
    create_pickup_point,
    get_all_pickup_points,
    update_pickup_point_by_id,
    delete_pickup_point_by_id,
)

from core.dependencies import get_db_session
from core.dependencies.fastapi_users import current_active_superuser

from core.config import settings
from core.models import User
from core.schemas.pickup_point import PickupPointCreate, PickupPointUpdate

from utils.templates import templates


router = APIRouter(prefix=settings.view.pickup_points)


@router.get(
    path="/",
    name="admin_pickup_points",
    include_in_schema=False,
    response_model=None,
)
async def admin_pickup_points(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
):
    pickup_points_list = await get_all_pickup_points(session=session)
    return templates.TemplateResponse(
        request=request,
        name="admin/pickup-points.html",
        context={
            "user": user,
            "pickup_points_list": pickup_points_list,
        },
    )


@router.post(
    path="/create-pickup-point",
    name="admin_create_pickup_point",
    include_in_schema=False,
    response_model=None,
)
async def admin_pickup_point(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    pickup_point_name: str = Form(...),
    address: str = Form(...),
    work_hours: str = Form(...),
):
    try:
        pickup_point_data = PickupPointCreate(
            name=pickup_point_name,
            address=address,
            work_hours=work_hours,
        )
        await create_pickup_point(
            session=session,
            pickup_point_data=pickup_point_data,
        )
        message = f"Пункт выдачи с именем '{pickup_point_name}' успешно создан."
    except HTTPException as exc:
        message = f"Пункт выдачи с именем '{pickup_point_name}' уже существует."
    except Exception as e:
        message = f"Ошибка при создании пункта выдачи: {str(e)}"

    return templates.TemplateResponse(
        request=request,
        name="admin/pickup-points.html",
        context={
            "user": user,
            "pickup_points_list": await get_all_pickup_points(session=session),
            "message": message,
        },
    )


@router.post(
    path="/update-pickup-point",
    name="admin_update_pickup_point",
    include_in_schema=False,
    response_model=None,
)
async def admin_update_pickup_point(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    pickup_point_id_up: int = Form(...),
    pickup_point_new_name: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    work_hours: Optional[str] = Form(None),
):
    try:
        update_data = {}
        if pickup_point_new_name is not None and pickup_point_new_name.strip() != "":
            update_data["name"] = pickup_point_new_name
        if address is not None and address.strip() != "":
            update_data["address"] = address
        if work_hours is not None and work_hours.strip() != "":
            update_data["work_hours"] = work_hours

        if not update_data:
            message = "Нет данных для обновления."
        else:
            pickup_point_data = PickupPointUpdate(**update_data)
            await update_pickup_point_by_id(
                session=session,
                pickup_point_id=pickup_point_id_up,
                pickup_point_data=pickup_point_data,
            )
            message = f"Пункт выдачи с ID {pickup_point_id_up} успешно обновлена."

    except Exception as exc:
        message = f"Ошибка при обновлении пункта выдачи: {str(exc)}"

    return templates.TemplateResponse(
        request=request,
        name="admin/pickup-points.html",
        context={
            "user": user,
            "pickup_points_list": await get_all_pickup_points(session=session),
            "message": message,
        },
    )


@router.post(
    path="/delete-pickup-point",
    name="admin_delete_pickup_point",
    include_in_schema=False,
    response_model=None,
)
async def admin_delete_pickup_point(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    pickup_point_id_del: int = Form(...),
):
    try:
        await delete_pickup_point_by_id(
            session=session,
            pickup_point_id=pickup_point_id_del,
        )
        message = f"Пункт выдачи с ID {pickup_point_id_del} успешно удалена."
    except Exception as exc:
        message = f"Ошибка при удалении пункта выдачи: {str(exc)}"

    return templates.TemplateResponse(
        request=request,
        name="admin/pickup-points.html",
        context={
            "user": user,
            "pickup_points_list": await get_all_pickup_points(session=session),
            "message": message,
        },
    )
