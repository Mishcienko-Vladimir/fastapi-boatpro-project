from typing import Annotated

from fastapi import Form
from fastapi import APIRouter, Request, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.repositories.authentication.fastapi_users import current_active_superuser
from core.repositories.user_manager_crud import UserManagerCrud
from core.config import settings
from core.models import User, db_helper
from core.schemas.user import UserRead

from utils.templates import templates


router = APIRouter(prefix=settings.view.users)


@router.get(
    path="/",
    name="admin_users",
    include_in_schema=False,
    response_model=None,
)
async def admin_users(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
):
    users = await UserManagerCrud(session=session).get_all_users()
    users_list = [UserRead.model_validate(user) for user in users]
    number_verified = sum(1 for user in users_list if user.is_verified)
    number_superuser = sum(1 for user in users_list if user.is_superuser)
    return templates.TemplateResponse(
        name="admin/users.html",
        context={
            "request": request,
            "user": user,
            "users_list": users_list,
            "number_verified": number_verified,
            "number_superuser": number_superuser,
        },
    )


@router.post(
    path="/delete-user",
    name="admin_delete_user",
    include_in_schema=False,
    response_model=None,
)
async def admin_delete_user(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    user_id_del: int = Form(...),
):
    user_manager = UserManagerCrud(session=session)
    user_delete = await user_manager.delete_user(user_id_del)
    if not user_delete:
        message = f"Пользователь с ID: {user_id_del} не найден."
    else:
        message = f"Пользователь с ID {user_id_del} успешно удалён."

    users = await user_manager.get_all_users()
    users_list = [UserRead.model_validate(u) for u in users]
    number_verified = sum(1 for u in users_list if u.is_verified)
    number_superuser = sum(1 for u in users_list if u.is_superuser)

    return templates.TemplateResponse(
        "admin/users.html",
        {
            "request": request,
            "user": user,
            "users_list": users_list,
            "number_verified": number_verified,
            "number_superuser": number_superuser,
            "message": message,
        },
    )
