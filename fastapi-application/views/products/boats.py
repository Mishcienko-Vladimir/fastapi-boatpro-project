from typing import Optional, Annotated

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.routers.products.boats import get_boats_summary, get_boat_by_name

from core.dependencies import get_db_session, optional_user
from core.config import settings
from core.models import User

from utils.templates import templates


router = APIRouter(
    prefix=settings.view.boats,
)


@router.get(
    path="/",
    name="boats",
    include_in_schema=False,
    response_model=None,
)
async def boats(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Optional[User] = Depends(optional_user),
):
    boats_list = await get_boats_summary(session=session)
    return templates.TemplateResponse(
        request=request,
        name="products/boats.html",
        context={
            "boats_list": boats_list,
            "user": user,
        },
    )


@router.get(
    path=f"/{{boat_name}}",
    name="boat_detail",
    include_in_schema=False,
    response_model=None,
)
async def boat_detail(
    request: Request,
    boat_name: str,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Optional[User] = Depends(optional_user),
):
    boat = await get_boat_by_name(session=session, boat_name=boat_name)
    return templates.TemplateResponse(
        request=request,
        name="products/boat-detail.html",
        context={
            "boat": boat,
            "user": user,
        },
    )
