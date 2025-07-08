from fastapi_users import FastAPIUsers

from api.dependencies.user_manager import get_user_manager
from api.dependencies.backend import authentication_backend
from core.models.user import User
from core.types.user_id import UserIdType

fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [authentication_backend],
)
