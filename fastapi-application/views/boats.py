from typing import Optional, Annotated

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.routers.products.boats import get_boats_summary

from core.repositories.authentication.fastapi_users import optional_user
from core.config import settings
from core.models import User, db_helper

from utils.templates import templates


router = APIRouter(
    prefix=settings.view.boats,
)


@router.get(
    path=settings.view.catalog,
    name="boats",
    include_in_schema=False,
    response_model=None,
)
async def boats(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Optional[User] = Depends(optional_user),
):
    boats_list = await get_boats_summary(session=session)
    return templates.TemplateResponse(
        name="boats.html",
        context={
            "request": request,
            "boats_list": boats_list,
            "user": user,
        },
    )
