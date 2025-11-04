from typing import Optional

from fastapi import APIRouter, Request, Depends

from core.repositories.authentication.fastapi_users import optional_user
from core.config import settings
from core.models import User

from utils.limiter import limiter
from utils.templates import templates


router = APIRouter(
    prefix=settings.view.limit_exceeded,
)


@router.get(
    "/",
    name="limit_exceeded",
    include_in_schema=False,
    response_model=None,
)
@limiter.exempt
def limit_exceeded(
    request: Request,
    user: Optional[User] = Depends(optional_user),
):
    return templates.TemplateResponse(
        name="limit-exceeded.html",
        context={
            "request": request,
            "user": user,
        },
    )
