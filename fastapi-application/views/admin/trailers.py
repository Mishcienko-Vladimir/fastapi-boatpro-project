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
from api.api_v1.dependencies.parser_forms_create import parse_trailer_create

from core.dependencies import get_db_session
from core.dependencies.fastapi_users import current_active_superuser

from core.config import settings
from core.models import User
from core.schemas.products.trailer import TrailerUpdate, TrailerCreate

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
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
):
    trailers_list = await get_trailers(session=session)
    return templates.TemplateResponse(
        request=request,
        name="admin/trailers.html",
        context={
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
    session: Annotated[AsyncSession, Depends(get_db_session)],
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
        request=request,
        name="admin/trailers.html",
        context={
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
    session: Annotated[AsyncSession, Depends(get_db_session)],
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
        message = f"Ошибка при создании прицепа: {str(exc)}"

    return templates.TemplateResponse(
        request=request,
        name="admin/trailers.html",
        context={
            "user": user,
            "trailers_list": await get_trailers(session=session),
            "message": message,
        },
    )


@router.post(
    path="/update-trailer",
    name="admin_update_trailer",
    include_in_schema=False,
    response_model=None,
)
async def admin_update_trailer(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    trailer_id_up: int = Form(...),
    name: Optional[str] = Form(None),
    price: Optional[str] = Form(None),
    company_name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(None),
    full_mass: Optional[str] = Form(None),
    load_capacity: Optional[str] = Form(None),
    trailer_length: Optional[str] = Form(None),
    max_ship_length: Optional[str] = Form(None),
):
    try:
        update_data = {}
        for key, value in locals().items():
            if (
                key not in ["request", "session", "user", "trailer_id_up"]
                and value is not None
            ):
                if isinstance(value, str) and value.strip() == "":
                    continue
                try:
                    numeric_value = int(value)
                    update_data[key] = numeric_value
                except (ValueError, TypeError):
                    update_data[key] = value

        if not update_data:
            message = "Нет данных для обновления"

        trailer_update = TrailerUpdate(**update_data)
        updated_trailer = await update_trailer_data_by_id(
            session=session,
            trailer_id=trailer_id_up,
            trailer_data=trailer_update,
        )
        message = f"Прицеп с ID {trailer_id_up} успешно обновлен"
    except HTTPException as exc:
        message = f"Прицеп с ID {trailer_id_up} не найден"
    except Exception as exc:
        message = f"Ошибка при обновлении прицепа: {str(exc)}"

    return templates.TemplateResponse(
        request=request,
        name="admin/trailers.html",
        context={
            "user": user,
            "trailers_list": await get_trailers(session=session),
            "message": message,
        },
    )


@router.post(
    path="/update-images",
    name="admin_update_trailer_images",
    include_in_schema=False,
    response_model=None,
)
async def admin_update_trailer_images(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    trailer_id_img: int = Form(...),
    remove_images: str | None = Form(None),
    add_images: list[UploadFile] = File(...),
):
    try:
        await update_trailer_images_by_id(
            session=session,
            trailer_id=trailer_id_img,
            remove_images=remove_images,
            add_images=add_images,
        )
        message = f"Фото прицепа с ID {trailer_id_img} успешно обновлены"
    except HTTPException as exc:
        message = exc.detail
    except Exception as exc:
        message = f"Ошибка при обновлении фото: {str(exc)}"

    return templates.TemplateResponse(
        request=request,
        name="admin/trailers.html",
        context={
            "user": user,
            "trailers_list": await get_trailers(session=session),
            "message": message,
        },
    )
