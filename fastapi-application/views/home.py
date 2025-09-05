from typing import Annotated

from fastapi import APIRouter, Request, Depends

from core.repositories.authentication.fastapi_users import current_active_user
from core.config import settings
from core.models import User
from utils.templates import templates


router = APIRouter(
    prefix=settings.view.home,
)


@router.get(
"/",
    name="home",
    include_in_schema=False,
)
def home(
    request: Request,
    user: Annotated[User, Depends(current_active_user)],
):
    return templates.TemplateResponse(
        name="index.html",
        context={
            "request": request,
            "user": user,
        },
    )
