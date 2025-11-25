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

    Обеспечивает расширенную логику поверх стандартного `BaseUserManager` из `fastapi-users`,
    позволяя выполнять фоновые задачи (например, отправку писем) и сброс кэша при изменениях.

    Attributes:
        reset_password_token_secret (str): Секретный ключ для генерации токена сброса пароля.
        verification_token_secret (str): Секретный ключ для генерации токена подтверждения email.
        background_tasks (BackgroundTasks | None): Объект для выполнения фоновых задач (например, отправка email).

    Args:
        user_db (BaseUserDatabase[User, UserIdType]): База данных пользователей.
        password_helper (PasswordHelperProtocol | None): Вспомогательный инструмент для хеширования паролей.
        background_tasks (BackgroundTasks | None): Объект для асинхронного выполнения задач (опционально).

    Methods:
        on_after_register: Вызывается после успешной регистрации.
        on_after_forgot_password: Вызывается при запросе сброса пароля.
        on_after_request_verify: Вызывается при запросе подтверждения email.
        on_after_verify: Вызывается после успешного подтверждения email.
        on_after_delete: Вызывается после удаления пользователя.
    """

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
        """
        Вызывается после успешной регистрации пользователя.

        Выполняет:
            - Сброс кэша списка пользователей (для актуализации в админке).
            - Логирование события.
            - (Опционально) Отправка уведомления о новом пользователе.

        Args:
            user (User): Объект зарегистрированного пользователя.
            request (Request | None): HTTP-запрос, инициировавший регистрацию.

        Side effects:
            - Очищает кэш: `namespace=settings.cache.namespace.users_list`
            - Логирует: "User {id} has registered."
            - (Закомментировано) Может отправить вебхук: `send_new_user_notification(user)`
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

        Генерирует ссылку для сброса и отправляет её на email пользователя.

        Args:
            user (User): Пользователь, запросивший сброс пароля.
            token (str): Сгенерированный токен для сброса.
            request (Request | None): HTTP-запрос, инициировавший сброс.

        Side effects:
            - Формирует ссылку: `{base_url}/password-reset?token={token}`
            - Добавляет в фоновую очередь: отправку email через `send_reset_password`
            - Логирует событие
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
        Вызывается после запроса подтверждения email.

        Генерирует ссылку для подтверждения и отправляет письмо с инструкциями.

        Args:
            user (User): Пользователь, запросивший подтверждение email.
            token (str): Токен для подтверждения.
            request (Request | None): HTTP-запрос, инициировавший запрос.

        Side effects:
            - Формирует ссылку: `{base_url}/verify-email?token={token}`
            - Добавляет в фоновую очередь: отправку письма через `send_verification_email`
            - Логирует событие
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
        Вызывается после успешного подтверждения email.

        Выполняет:
            - Отправку уведомления о подтверждении.
            - Сброс кэша списка пользователей.

        Args:
            user (User): Пользователь, подтвердивший email.
            request (Request | None): HTTP-запрос, инициировавший подтверждение.

        Side effects:
            - Добавляет в фоновую очередь: отправку письма `send_email_confirmed`
            - Сбрасывает кэш: `users_list`
            - Логирует событие
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
        else:
            await FastAPICache.clear(
                namespace=settings.cache.namespace.users_list,
            )

    async def on_after_delete(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        """
        Вызывается после успешного удаления пользователя.

        Выполняет:
            - Сброс кэша списка пользователей.
            - Логирование события.

        Args:
            user (User): Пользователь, который был удалён.
            request (Request | None): HTTP-запрос, инициировавший удаление.

        Side effects:
            - Сбрасывает кэш: `users_list`
            - Логирует: "User {id} has been deleted."
        """
        log.warning("User %r has been deleted.", user.id)

        if self.background_tasks:
            self.background_tasks.add_task(
                FastAPICache.clear,
                namespace=settings.cache.namespace.users_list,
            )
        else:
            await FastAPICache.clear(
                namespace=settings.cache.namespace.users_list,
            )
