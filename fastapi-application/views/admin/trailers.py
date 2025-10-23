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


@router.post(
    path="/delete-trailer",
    name="admin_delete_trailer",
    include_in_schema=False,
    response_model=None,
)
async def admin_delete_trailer(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    trailer_id_del: int = Form(...),
):
    try:
        await delete_trailer_by_id(session=session, trailer_id=trailer_id_del)
        message = f"Прицеп с ID {trailer_id_del} успешно удален"
    except HTTPException as exc:
        message = exc.detail

    return templates.TemplateResponse(
        name="admin/trailers.html",
        context={
            "request": request,
            "user": user,
            "trailers_list": await get_trailers(session=session),
            "message": message,
        },
    )


@router.post(
    path="/create-trailer",
    name="admin_create_trailer",
    include_in_schema=False,
    response_model=None,
)
async def admin_create_trailer(
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
    full_mass: int = Form(...),
    load_capacity: int = Form(...),
    trailer_length: int = Form(...),
    max_ship_length: int = Form(...),
    images: list[UploadFile] = File(...),
):
    try:
        new_trailer = await create_trailer(
            session=session,
            category_id=category_id,
            name=name,
            price=price,
            company_name=company_name,
            description=description,
            is_active=is_active,
            full_mass=full_mass,
            load_capacity=load_capacity,
            trailer_length=trailer_length,
            max_ship_length=max_ship_length,
            images=images,
        )
        message = f"Прицеп с ID {new_trailer.id} успешно создан"
    except HTTPException as exc:
        message = f"Прицеп с именем {name} уже существует"
    except Exception as exc:
        message = "Ошибка при создании прицепа"

    return templates.TemplateResponse(
        name="admin/trailers.html",
        context={
            "request": request,
            "user": user,
            "trailers_list": await get_trailers(session=session),
            "message": message,
        },
    )
