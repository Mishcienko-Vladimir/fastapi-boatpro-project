from typing import Annotated, Optional
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.routers.favorites import get_favorites

from core.dependencies import get_db_session
from core.repositories.authentication.fastapi_users import optional_user
from core.config import settings
from core.models import User

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
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Optional[User] = Depends(optional_user),
):
    if not user:
        return templates.TemplateResponse(
            request=request,
            name="favorites_and_orders/please-log.html",
            context={
                "user": user,
            },
        )

    favorites_list = await get_favorites(session=session, user_id=user.id)
    return templates.TemplateResponse(
        request=request,
        name="favorites_and_orders/favorites.html",
        context={
            "user": user,
            "favorites_list": favorites_list,
        },
    )
