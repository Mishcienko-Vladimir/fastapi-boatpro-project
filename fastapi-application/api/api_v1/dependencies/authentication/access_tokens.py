from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from core.dependencies import get_db_session
from core.models import AccessToken

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_token_db(
    session: Annotated["AsyncSession", Depends(get_db_session)],
):
    yield AccessToken.get_db(
        session=session,
    )
