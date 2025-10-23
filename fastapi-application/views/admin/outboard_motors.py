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
        name="admin/outboard-motors.html",
        context={
            "request": request,
            "user": user,
            "outboard_motors_list": outboard_motors_list,
        },
    )


@router.post(
    path="/delete-outboard-motor",
    name="admin_delete_outboard_motor",
    include_in_schema=False,
    response_model=None,
)
async def admin_delete_outboard_motor(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    outboard_motor_id_del: int = Form(...),
):
    try:
        await delete_outboard_motor_by_id(
            session=session,
            outboard_motor_id=outboard_motor_id_del,
        )
        message = f"Лодочный мотор с ID {outboard_motor_id_del} успешно удален"
    except HTTPException as exc:
        message = exc.detail

    return templates.TemplateResponse(
        name="admin/outboard-motors.html",
        context={
            "request": request,
            "user": user,
            "outboard_motors_list": await get_outboard_motors(session=session),
            "message": message,
        },
    )


@router.post(
    path="/create-outboard-motor",
    name="admin_create_outboard_motor",
    include_in_schema=False,
    response_model=None,
)
async def admin_create_outboard_motor(
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
    engine_power: int = Form(...),
    engine_type: EngineType = Form(...),
    weight: int = Form(...),
    number_cylinders: int = Form(...),
    engine_displacement: int = Form(...),
    control_type: ControlType = Form(...),
    starter_type: StarterType = Form(...),
    images: list[UploadFile] = File(...),
):
    try:
        new_outboard_motor = await create_outboard_motor(
            session=session,
            category_id=category_id,
            name=name,
            price=price,
            company_name=company_name,
            description=description,
            is_active=is_active,
            engine_power=engine_power,
            engine_type=engine_type,
            weight=weight,
            number_cylinders=number_cylinders,
            engine_displacement=engine_displacement,
            control_type=control_type,
            starter_type=starter_type,
            images=images,
        )
        message = f"Прицеп с ID {new_outboard_motor.id} успешно создан"
    except HTTPException as exc:
        message = f"Прицеп с именем {name} уже существует"
    except Exception as exc:
        message = "Ошибка при создании прицепа"

    return templates.TemplateResponse(
        name="admin/outboard-motors.html",
        context={
            "request": request,
            "user": user,
            "outboard_motors_list": await get_outboard_motors(session=session),
            "message": message,
        },
    )


@router.post(
    path="/update-outboard-motor",
    name="admin_update_outboard_motor",
    include_in_schema=False,
    response_model=None,
)
async def admin_update_outboard_motor(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    outboard_motor_id_up: int = Form(...),
    name: Optional[str] = Form(None),
    price: Optional[str] = Form(None),
    company_name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(None),
    engine_power: Optional[str] = Form(None),
    engine_type: Optional[EngineType] = Form(None),
    weight: Optional[str] = Form(None),
    number_cylinders: Optional[str] = Form(None),
    engine_displacement: Optional[str] = Form(None),
    control_type: Optional[ControlType] = Form(None),
    starter_type: Optional[StarterType] = Form(None),
):
    try:
        update_data = {}
        for key, value in locals().items():
            if (
                key not in ["request", "session", "user", "outboard_motor_id_up"]
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

        outboard_motor_update = OutboardMotorUpdate(**update_data)
        updated_outboard_motor = await update_outboard_motor_data_by_id(
            session=session,
            outboard_motor_id=outboard_motor_id_up,
            outboard_motor_data=outboard_motor_update,
        )
        message = f"Лодочный мотор с ID {outboard_motor_id_up} успешно обновлен"
    except HTTPException as exc:
        message = f"Лодочный мотор с ID {outboard_motor_id_up} не найден"
    except Exception as exc:
        message = "Ошибка при обновлении лодочного мотора"

    return templates.TemplateResponse(
        name="admin/outboard-motors.html",
        context={
            "request": request,
            "user": user,
            "outboard_motors_list": await get_outboard_motors(session=session),
            "message": message,
        },
    )


@router.post(
    path="/update-images",
    name="admin_update_outboard_motor_images",
    include_in_schema=False,
    response_model=None,
)
async def admin_update_outboard_motor_images(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    outboard_motor_id_img: int = Form(...),
    remove_images: str | None = Form(None),
    add_images: list[UploadFile] = File(...),
):
    try:
        await update_outboard_motor_images_by_id(
            session=session,
            outboard_motor_id=outboard_motor_id_img,
            remove_images=remove_images,
            add_images=add_images,
        )
        message = (
            f"Фото лодочного мотора с ID {outboard_motor_id_img} успешно обновлены"
        )
    except HTTPException as exc:
        message = exc.detail
    except Exception as exc:
        message = "Ошибка при обновлении фото"

    return templates.TemplateResponse(
        name="admin/outboard-motors.html",
        context={
            "request": request,
            "user": user,
            "outboard_motors_list": await get_outboard_motors(session=session),
            "message": message,
        },
    )
