from fastapi_users import FastAPIUsers

from api.api_v1.dependencies.authentication import get_user_manager
from api.api_v1.dependencies.authentication import authentication_backend

from core.models.user import User
from core.types.user_id import UserIdType


fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [authentication_backend],
)

optional_user = fastapi_users.current_user(optional=True)
current_active_user = fastapi_users.current_user(active=True)
# current_active_verified_user = fastapi_users.current_user(active=True, verified=True)
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)
