import logging
from typing import Optional, TYPE_CHECKING

from fastapi_users import BaseUserManager, IntegerIDMixin

from core.models.user import User
from core.config import settings
from core.types.user_id import UserIdType
from utils.webhooks.user import send_new_user_notification

if TYPE_CHECKING:
    from fastapi import Request

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def on_after_register(self, user: User, request: Optional["Request"] = None):
        log.warning("User %r has registered.", user.id)
        # отправка сообщения на сторонний сервис и вывод информации о том, что пользователь создан
        # await send_new_user_notification(user)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional["Request"] = None
    ):
        log.warning(
            "User %r has forgot their password. Reset token: %r", user.id, token
        )

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional["Request"] = None
    ):
        log.warning(
            "Verification requested for user %r. Verification token: %r", user.id, token
        )
