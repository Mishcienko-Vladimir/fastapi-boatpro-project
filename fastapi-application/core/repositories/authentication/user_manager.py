import logging
from typing import Optional, TYPE_CHECKING

from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.db import BaseUserDatabase
from fastapi_cache import FastAPICache

from core.models.user import User
from core.config import settings
from core.types.user_id import UserIdType

from mailing import (
    send_verification_email,
    send_email_confirmed,
    send_reset_password,
)
from utils.webhooks.user import send_new_user_notification  # noqa

if TYPE_CHECKING:
    from fastapi import Request, BackgroundTasks  # noqa
    from fastapi_users.password import PasswordHelperProtocol  # noqa


log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, UserIdType]):
    """
    Класс для управления жизненным циклом пользователя: регистрация, сброс пароля, подтверждение почты и т.д.
    Добавляет пользовательские действия после ключевых событий.

    :reset_password_token_secret: Секретный токен для создания токена сброса пароля.
    :verification_token_secret: Секретный токен для создания токена подтверждения почты.

    :methods:
        - on_after_register: Вызывается после успешной регистрации пользователя.
        - on_after_forgot_password: Вызывается после запроса на сброс пароля.
        - on_after_request_verify: Вызывается после запроса на подтверждение почты.
        - on_after_verify: Вызывается после успешного подтверждения почты.
    """

    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    def __init__(
        self,
        user_db: BaseUserDatabase[User, UserIdType],
        password_helper: Optional["PasswordHelperProtocol"] = None,
        background_tasks: Optional["BackgroundTasks"] = None,
    ):
        """
        Инициализация UserManager.

        :param user_db: База данных пользователей.
        :param password_helper: Вспомогательный инструмент для работы с паролями.
        :param background_tasks: Объект для выполнения фоновых задач (например, отправка писем).
        """

        super().__init__(user_db, password_helper)
        self.background_tasks = background_tasks

    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        """
        Вызывается после успешной регистрации пользователя.

        :param user: Объект пользователя, который зарегистрировался.
        :param request: HTTP-запрос, который инициировал регистрацию (опционально).
        :return: - сброс кэша.
        """

        if self.background_tasks:
            self.background_tasks.add_task(
                FastAPICache.clear,
                namespace=settings.cache.namespace.users_list,
            )
        else:
            await FastAPICache.clear(
                namespace=settings.cache.namespace.users_list,
            )

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
        """
        Вызывается после запроса на сброс пароля.

        :param user: Объект пользователя, который запрашивает сброс пароля.
        :param token: Токен для сброса пароля.
        :param request: HTTP-запрос, который инициировал сброс (опционально).
        :return: Отправляет письмо со ссылкой для сброса пароля.
        """

        log.warning(
            "User %r has forgot their password. Reset token: %r",
            user.id,
            token,
        )

        reset_password_link = request.url_for("password_reset").replace_query_params(
            token=token
        )

        self.background_tasks.add_task(
            send_reset_password,
            user=user,
            reset_password_link=str(reset_password_link),
        )

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        """
        Вызывается после запроса на подтверждение почты.

        Формирует ссылку для подтверждения и запускает фоновую задачу на отправку письма.

        :param user: Объект пользователя, который запрашивает подтверждение почты.
        :param token: Токен для подтверждения почты.
        :param request: HTTP-запрос, который инициировал подтверждение (опционально).
        :return: Отправляет письмо со ссылкой для подтверждения почты.
        """

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
        """
        Вызывается после успешного подтверждения почты.

        Логирует событие и запускает фоновую задачу на отправку уведомления о подтверждении.

        :param user: Объект пользователя, чья почта была подтверждена.
        :param request: HTTP-запрос, который инициировал подтверждение (опционально).
        :return: Отправляет письмо, о том что почта подтверждена.
        """

        log.warning(
            "User %r has been verified",
            user.id,
        )

        self.background_tasks.add_task(
            send_email_confirmed,
            user=user,
        )

        if self.background_tasks:
            self.background_tasks.add_task(
                FastAPICache.clear,
                namespace=settings.cache.namespace.users_list,
            )
            self.background_tasks.add_task(
                FastAPICache.clear,
                namespace=settings.cache.namespace.user,
            )
        else:
            await FastAPICache.clear(
                namespace=settings.cache.namespace.users_list,
            )
            await FastAPICache.clear(
                namespace=settings.cache.namespace.user,
            )
