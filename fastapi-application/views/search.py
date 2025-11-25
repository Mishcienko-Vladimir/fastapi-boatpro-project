from typing import Annotated, Optional
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.routers.search import search_products

from core.dependencies import get_db_session
from core.dependencies.fastapi_users import optional_user

from core.config import settings
from core.models import User

from utils.templates import templates


router = APIRouter(prefix=settings.view.search)


@router.get(
    "/",
    name="search",
    include_in_schema=False,
)
async def search(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    query: str,
    user: Optional[User] = Depends(optional_user),
):
    products_list = await search_products(session=session, query=query)
    return templates.TemplateResponse(
        request=request,
        name="search.html",
        context={
            "user": user,
            "products_list": products_list,
            "query": query,
        },
    )
