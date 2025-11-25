from typing import Optional

from fastapi import APIRouter, Request, Depends

from core.dependencies.fastapi_users import optional_user
from core.config import settings
from core.models import User

from utils.templates import templates


router = APIRouter(
    prefix=settings.view.page_missing,
)


@router.get(
    "/",
    name="page_missing",
    include_in_schema=False,
    response_model=None,
)
def page_missing(
    request: Request,
    user: Optional[User] = Depends(optional_user),
):
    return templates.TemplateResponse(
        request=request,
        name="page-missing.html",
        context={
            "user": user,
        },
    )
