from typing import Optional, Annotated

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.routers.products.trailers import (
    get_trailers_summary,
    get_trailer_by_name,
)

from core.repositories.authentication.fastapi_users import optional_user
from core.config import settings
from core.models import User, db_helper

from utils.templates import templates


router = APIRouter(
    prefix=settings.view.trailers,
)


@router.get(
    path=settings.view.catalog,
    name="trailers",
    include_in_schema=False,
    response_model=None,
)
async def trailers(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Optional[User] = Depends(optional_user),
):
    trailers_list = await get_trailers_summary(session=session)
    return templates.TemplateResponse(
        name="products/trailers.html",
        context={
            "request": request,
            "trailers_list": trailers_list,
            "user": user,
        },
    )


@router.get(
    path=f"{settings.view.catalog}{settings.view.trailers}/{{trailer_name}}",
    name="trailer_detail",
    include_in_schema=False,
    response_model=None,
)
async def trailer_detail(
    request: Request,
    trailer_name: str,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Optional[User] = Depends(optional_user),
):
    trailer = await get_trailer_by_name(session=session, trailer_name=trailer_name)
    return templates.TemplateResponse(
        name="products/trailer-detail.html",
        context={
            "request": request,
            "trailer": trailer,
            "user": user,
        },
    )
