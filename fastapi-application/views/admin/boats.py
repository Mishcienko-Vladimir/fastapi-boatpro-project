from typing import Annotated, Optional

from fastapi import Form, HTTPException, File, UploadFile
from fastapi import APIRouter, Request, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.routers.products.boats import (
    get_boats,
    create_boat,
    update_boat_data_by_id,
    update_boat_images_by_id,
    delete_boat_by_id,
)
from api.api_v1.dependencies.create_multipart_form_data import (
    create_multipart_form_data,
)

from core.dependencies import get_db_session
from core.dependencies.fastapi_users import current_active_superuser

from core.config import settings
from core.models import User
from core.schemas.products.boat import BoatUpdate, BoatCreate

from utils.templates import templates


router = APIRouter(prefix=settings.view.boats)


@router.get(
    path="/",
    name="admin_boats",
    include_in_schema=False,
    response_model=None,
)
async def admin_boats(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
):
    boats_list = await get_boats(session=session)
    return templates.TemplateResponse(
        request=request,
        name="admin/boats.html",
        context={
            "user": user,
            "boats_list": boats_list,
        },
    )


@router.post(
    path="/delete-boat",
    name="admin_delete_boat",
    include_in_schema=False,
    response_model=None,
)
async def admin_delete_boat(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    boat_id_del: int = Form(...),
):
    try:
        await delete_boat_by_id(session=session, boat_id=boat_id_del)
        message = f"Катер с ID {boat_id_del} успешно удален"
    except HTTPException as exc:
        message = exc.detail

    return templates.TemplateResponse(
        request=request,
        name="admin/boats.html",
        context={
            "user": user,
            "boats_list": await get_boats(session=session),
            "message": message,
        },
    )


@router.post(
    path="/create-boat",
    name="admin_create_boat",
    include_in_schema=False,
    response_model=None,
)
async def admin_create_boat(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    boat_data: Annotated[
        "BoatCreate",
        Depends(create_multipart_form_data(BoatCreate)),
    ],
    images: Annotated[
        list[UploadFile],
        File(...),
    ],
):
    try:
        response = await create_boat(
            session=session,
            boat_data=boat_data,
            images=images,
        )
        message = f"Катер с ID {response.id} успешно создан"
    except HTTPException as exc:
        message = f"Катер с именем {boat_data.name} уже существует"
    except Exception as exc:
        message = f"Ошибка при создании катера: {str(exc)}"

    return templates.TemplateResponse(
        request=request,
        name="admin/boats.html",
        context={
            "user": user,
            "boats_list": await get_boats(session=session),
            "message": message,
        },
    )


@router.post(
    path="/update-boat",
    name="admin_update_boat",
    include_in_schema=False,
    response_model=None,
)
async def admin_update_boat(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    boat_id_up: int = Form(...),
    name: Optional[str] = Form(None),
    price: Optional[str] = Form(None),
    company_name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(None),
    length_hull: Optional[str] = Form(None),
    width_hull: Optional[str] = Form(None),
    weight: Optional[str] = Form(None),
    capacity: Optional[str] = Form(None),
    maximum_load: Optional[str] = Form(None),
    hull_material: Optional[str] = Form(None),
    thickness_side_sheet: Optional[str] = Form(None),
    bottom_sheet_thickness: Optional[str] = Form(None),
    fuel_capacity: Optional[str] = Form(None),
    maximum_engine_power: Optional[str] = Form(None),
    height_side_midship: Optional[str] = Form(None),
    transom_height: Optional[str] = Form(None),
):
    try:
        update_data = {}
        for key, value in locals().items():
            if (
                key not in ["request", "session", "user", "boat_id_up"]
                and value is not None
            ):
                # Пропускаем пустые строки
                if isinstance(value, str) and value.strip() == "":
                    continue
                try:
                    # Пытаемся конвертировать в int, если возможно
                    numeric_value = int(value)
                    update_data[key] = numeric_value
                except (ValueError, TypeError):
                    update_data[key] = value

        if not update_data:
            message = "Нет данных для обновления"

        boat_update = BoatUpdate(**update_data)
        updated_boat = await update_boat_data_by_id(
            session=session,
            boat_id=boat_id_up,
            boat_data=boat_update,
        )
        message = f"Катер с ID {boat_id_up} успешно обновлен"
    except HTTPException as exc:
        message = f"Катер с ID {boat_id_up} не найден"
    except Exception as exc:
        message = f"Ошибка при обновлении катера: {str(exc)}"

    return templates.TemplateResponse(
        request=request,
        name="admin/boats.html",
        context={
            "user": user,
            "boats_list": await get_boats(session=session),
            "message": message,
        },
    )


@router.post(
    path="/update-images",
    name="admin_update_boat_images",
    include_in_schema=False,
    response_model=None,
)
async def admin_update_boat_images(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    boat_id_img: int = Form(...),
    remove_images: str | None = Form(None),
    add_images: list[UploadFile] = File(...),
):
    try:
        await update_boat_images_by_id(
            session=session,
            boat_id=boat_id_img,
            remove_images=remove_images,
            add_images=add_images,
        )
        message = f"Фото катера с ID {boat_id_img} успешно обновлены"
    except HTTPException as exc:
        message = exc.detail
    except Exception as exc:
        message = f"Ошибка при обновлении фото: {str(exc)}"

    return templates.TemplateResponse(
        request=request,
        name="admin/boats.html",
        context={
            "user": user,
            "boats_list": await get_boats(session=session),
            "message": message,
        },
    )
