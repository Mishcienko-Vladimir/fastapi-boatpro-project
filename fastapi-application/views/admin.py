from typing import Annotated

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
    boat_id: int = Form(...),
):
    try:
        await delete_boat_by_id(session=session, boat_id=boat_id)
        message = f"Катер с ID {boat_id} успешно удален"
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
        message = "Катер с именем {name} уже существует"
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
