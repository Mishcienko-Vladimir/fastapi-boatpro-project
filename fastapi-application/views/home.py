from typing import Optional

from fastapi import APIRouter, Request, Depends

from core.dependencies.fastapi_users import optional_user
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
    response_model=None,
)
def home(
    request: Request,
    user: Optional[User] = Depends(optional_user),
):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "user": user,
        },
    )
