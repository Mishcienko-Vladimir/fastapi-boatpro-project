from typing import Optional

from fastapi import APIRouter, Request, Depends

from core.dependencies.fastapi_users import optional_user
from core.config import settings
from core.models import User

from utils.templates import templates


router = APIRouter(
    prefix=settings.view.password_reset,
)


@router.get(
    "/",
    name="password_reset",
    include_in_schema=False,
)
def password_reset(
    request: Request,
    user: Optional[User] = Depends(optional_user),
):
    return templates.TemplateResponse(
        request=request,
        name="auth/reset-password.html",
        context={
            "user": user,
        },
    )
