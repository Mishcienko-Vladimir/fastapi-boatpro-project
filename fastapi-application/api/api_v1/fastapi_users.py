from fastapi_users import FastAPIUsers

from api.dependencies.authentication import get_user_manager
from api.dependencies.authentication import authentication_backend

from core.models.user import User
from core.types.user_id import UserIdType


fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [authentication_backend],
)
