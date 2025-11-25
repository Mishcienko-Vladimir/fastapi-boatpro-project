from fastapi_users import FastAPIUsers

from api.api_v1.dependencies.authentication.user_manager import get_user_manager
from api.api_v1.dependencies.authentication.backend import authentication_backend

from core.models.user import User
from core.types.user_id import UserIdType


fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [authentication_backend],
)

# Получение текущего пользователя, если он не зарегистрирован то None
optional_user = fastapi_users.current_user(optional=True)

# Получение текущего активного пользователя (если пользователь не зарегистрирован то ошибка)
current_active_user = fastapi_users.current_user(active=True)

# Получение текущего активного пользователя, который подтвердил свой email (если нет, то ошибка)
current_active_verified_user = fastapi_users.current_user(active=True, verified=True)

# Получение текущего активного суперпользователя (если нет, то ошибка)
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)
