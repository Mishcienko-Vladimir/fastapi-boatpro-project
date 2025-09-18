from typing import Optional

from fastapi import APIRouter, Request, Depends

from core.repositories.authentication.fastapi_users import optional_user
from core.config import settings
from core.models import User

from utils.templates import templates


router = APIRouter(
    prefix=settings.view.verify_email,
)


@router.get(
    "/",
    name="verify_email",
    include_in_schema=False,
)
def verify_email(
    request: Request,
    user: Optional[User] = Depends(optional_user),
):
    return templates.TemplateResponse(
        name="verification.html",
        context={
            "request": request,
            "user": user,
        },
    )
