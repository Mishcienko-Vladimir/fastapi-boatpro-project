from typing import Annotated
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.routers.favorites import get_favorites

from core.repositories.authentication.fastapi_users import current_active_user
from core.config import settings
from core.models import User, db_helper

from utils.templates import templates


router = APIRouter(
    prefix=settings.view.favorites,
)


@router.get(
    "/",
    name="favorites",
    include_in_schema=False,
)
async def favorites(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: User = Depends(current_active_user),
):
    if not user.is_verified:
        return templates.TemplateResponse(
            name="please-log.html",
            context={"request": request, "user": user},
        )

    favorites_list = await get_favorites(session=session, user_id=user.id)
    return templates.TemplateResponse(
        name="favorites.html",
        context={
            "request": request,
            "user": user,
            "favorites_list": favorites_list,
        },
    )
