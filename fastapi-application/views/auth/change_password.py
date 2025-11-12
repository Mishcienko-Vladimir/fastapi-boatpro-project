from typing import Optional

from fastapi import APIRouter, Request, Depends

from core.repositories.authentication.fastapi_users import optional_user
from core.config import settings
from core.models import User

from utils.templates import templates


router = APIRouter(
    prefix=settings.view.change_password,
)


@router.get(
    "/",
    name="change_password",
    include_in_schema=False,
)
def change_password(
    request: Request,
    user: Optional[User] = Depends(optional_user),
):
    return templates.TemplateResponse(
        request=request,
        name="auth/forgot-password.html",
        context={
            "user": user,
        },
    )
