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

from core.repositories.authentication.fastapi_users import current_active_superuser
from core.config import settings
from core.models import User, db_helper
from core.schemas.products.boat import BoatUpdate

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


@router.post(
    path=f"{settings.view.boats}/delete-boat",
    name="admin_delete_boat",
    include_in_schema=False,
    response_model=None,
)
async def admin_delete_boat(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
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
        name="admin/boats.html",
        context={
            "request": request,
            "user": user,
            "boats_list": await get_boats(session=session),
            "message": message,
        },
    )


@router.post(
    path=f"{settings.view.boats}/create-boat",
    name="admin_create_boat",
    include_in_schema=False,
    response_model=None,
)
async def admin_create_boat(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    category_id: int = Form(...),
    name: str = Form(...),
    price: int = Form(...),
    company_name: str = Form(...),
    description: str = Form(...),
    is_active: bool = Form(...),
    length_hull: int = Form(...),
    width_hull: int = Form(...),
    weight: int = Form(...),
    capacity: int = Form(...),
    maximum_load: int = Form(...),
    hull_material: str = Form(...),
    thickness_side_sheet: int | None = Form(0),
    bottom_sheet_thickness: int | None = Form(0),
    fuel_capacity: int | None = Form(0),
    maximum_engine_power: int | None = Form(0),
    height_side_midship: int | None = Form(0),
    transom_height: int | None = Form(0),
    images: list[UploadFile] = File(...),
):
    try:
        new_boat = await create_boat(
            session=session,
            category_id=category_id,
            name=name,
            price=price,
            company_name=company_name,
            description=description,
            is_active=is_active,
            length_hull=length_hull,
            width_hull=width_hull,
            weight=weight,
            capacity=capacity,
            maximum_load=maximum_load,
            hull_material=hull_material,
            thickness_side_sheet=thickness_side_sheet,
            bottom_sheet_thickness=bottom_sheet_thickness,
            fuel_capacity=fuel_capacity,
            maximum_engine_power=maximum_engine_power,
            height_side_midship=height_side_midship,
            transom_height=transom_height,
            images=images,
        )
        message = f"Катер с ID {new_boat.id} успешно создан"
    except HTTPException as exc:
        message = f"Катер с именем {name} уже существует"
    except Exception as exc:
        message = "Ошибка при создании катера"

    return templates.TemplateResponse(
        name="admin/boats.html",
        context={
            "request": request,
            "user": user,
            "boats_list": await get_boats(session=session),
            "message": message,
        },
    )


@router.post(
    path=f"{settings.view.boats}/update-boat",
    name="admin_update_boat",
    include_in_schema=False,
    response_model=None,
)
async def admin_update_boat(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
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
        message = "Ошибка при обновлении катера"

    return templates.TemplateResponse(
        name="admin/boats.html",
        context={
            "request": request,
            "user": user,
            "boats_list": await get_boats(session=session),
            "message": message,
        },
    )


@router.post(
    path=f"{settings.view.boats}/update-images",
    name="admin_update_boat_images",
    include_in_schema=False,
    response_model=None,
)
async def admin_update_boat_images(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
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
        message = "Ошибка при обновлении фото"

    return templates.TemplateResponse(
        name="admin/boats.html",
        context={
            "request": request,
            "user": user,
            "boats_list": await get_boats(session=session),
            "message": message,
        },
    )
