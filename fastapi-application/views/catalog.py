from typing import Optional

from fastapi import APIRouter, Request, Depends

from core.repositories.authentication.fastapi_users import optional_user
from core.config import settings
from core.models import User

from utils.templates import templates


router = APIRouter(
    prefix=settings.view.catalog,
)


@router.get(
    "/",
    name="catalog",
    include_in_schema=False,
    response_model=None,
)
def catalog(
    request: Request,
    user: Optional[User] = Depends(optional_user),
):
    return templates.TemplateResponse(
        name="catalog.html",
        context={
            "request": request,
            "user": user,
        },
    )
