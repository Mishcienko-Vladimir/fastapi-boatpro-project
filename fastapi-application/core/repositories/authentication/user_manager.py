import logging
from typing import Optional, TYPE_CHECKING

from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.db import BaseUserDatabase

from core.models.user import User
from core.config import settings
from core.types.user_id import UserIdType

from mailing import send_verification_email, send_email_confirmed
from utils.webhooks.user import send_new_user_notification  # noqa

if TYPE_CHECKING:
    from fastapi import Request, BackgroundTasks  # noqa
    from fastapi_users.password import PasswordHelperProtocol  # noqa


log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    def __init__(
        self,
        user_db: BaseUserDatabase[User, UserIdType],
        password_helper: Optional["PasswordHelperProtocol"] = None,
        background_tasks: Optional["BackgroundTasks"] = None,
    ):
        super().__init__(user_db, password_helper)
        self.background_tasks = background_tasks

    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "User %r has registered.",
            user.id,
        )
        # отправка сообщения на сторонний сервис и вывод информации о том, что пользователь создан
        # await send_new_user_notification(user)

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "User %r has forgot their password. Reset token: %r",
            user.id,
            token,
        )

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "Verification requested for user %r. Verification token: %r",
            user.id,
            token,
        )
        verification_link = request.url_for("verify_email").replace_query_params(
            token=token
        )

        self.background_tasks.add_task(
            send_verification_email,
            user=user,
            verification_link=str(verification_link),
        )

    async def on_after_verify(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "User %r has been verified",
            user.id,
        )

        self.background_tasks.add_task(
            send_email_confirmed,
            user=user,
        )
