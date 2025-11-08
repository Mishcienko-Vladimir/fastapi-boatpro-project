from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from core.dependencies import get_db_session
from core.models import User

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession  # noqa


async def get_users_db(
    session: Annotated[
        "AsyncSession",
        Depends(get_db_session),
    ],
):
    yield User.get_db(session=session)
