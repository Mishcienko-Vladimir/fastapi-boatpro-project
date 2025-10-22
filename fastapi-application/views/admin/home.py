from typing import Annotated

from fastapi import APIRouter, Request, Depends

from core.repositories.authentication.fastapi_users import current_active_superuser
from core.config import settings
from core.models import User

from utils.templates import templates


router = APIRouter(prefix=settings.view.home)


@router.get(
    "/",
    name="admin_home",
    include_in_schema=False,
    response_model=None,
)
def admin_home(
    request: Request,
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
):
    return templates.TemplateResponse(
        name="admin/home.html",
        context={
            "request": request,
            "user": user,
        },
    )
